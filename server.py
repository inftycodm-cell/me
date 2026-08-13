"""
سرور نمونه برای دریافت و ذخیره امن Session String
----------------------------------------------------
این سرور:
  1) initData ارسال‌شده از Mini App را با bot token تایید می‌کند
     (اطمینان از این‌که درخواست واقعاً از تلگرام و همان کاربر آمده)
  2) session string را رمزنگاری کرده و ذخیره می‌کند

این سرور هرگز شماره تلفن، کد تایید یا رمز دومرحله‌ای را دریافت
نمی‌کند — این‌ها فقط در مرورگر کاربر (سمت Mini App با GramJS) پردازش می‌شوند.

پیش‌نیاز:
    pip install flask cryptography
"""

import hashlib
import hmac
import json
import os
from urllib.parse import parse_qsl

from cryptography.fernet import Fernet
from flask import Flask, request, jsonify

# ---------------------------------------------------------------------------
# تنظیمات — این مقادیر را خودتان جایگزین کنید
# ---------------------------------------------------------------------------
BOT_TOKEN = "REPLACE_WITH_YOUR_BOT_TOKEN"          # از BotFather

# کلید رمزنگاری ذخیره‌سازی. یک‌بار این را تولید کنید و در جای امن (نه در کد) نگه دارید:
#   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_KEY = "REPLACE_WITH_YOUR_FERNET_KEY"

# فایل ساده برای ذخیره نمونه (در پروژه واقعی از دیتابیس واقعی استفاده کنید)
STORAGE_FILE = "sessions_store.json"

app = Flask(__name__)
fernet = Fernet(ENCRYPTION_KEY.encode())


# ---------------------------------------------------------------------------
# تایید initData ارسالی از Mini App (طبق مستندات رسمی تلگرام)
# https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
# ---------------------------------------------------------------------------
def verify_telegram_init_data(init_data: str, bot_token: str) -> dict | None:
    try:
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return None

    received_hash = parsed.pop("hash", None)
    if not received_hash:
        return None

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )

    secret_key = hmac.new(
        key=b"WebAppData", msg=bot_token.encode(), digestmod=hashlib.sha256
    ).digest()

    calculated_hash = hmac.new(
        key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        return None  # جعلی است یا دستکاری شده

    return parsed  # شامل user, auth_date و غیره


def load_store() -> dict:
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_store(store: dict) -> None:
    with open(STORAGE_FILE, "w") as f:
        json.dump(store, f)


# ---------------------------------------------------------------------------
# Endpoint: دریافت session string نهایی از Mini App
# ---------------------------------------------------------------------------
@app.route("/api/save-session", methods=["POST"])
def save_session():
    body = request.get_json(force=True)
    init_data = body.get("initData")
    session_string = body.get("sessionString")

    if not init_data or not session_string:
        return jsonify({"ok": False, "error": "missing fields"}), 400

    verified = verify_telegram_init_data(init_data, BOT_TOKEN)
    if not verified:
        return jsonify({"ok": False, "error": "invalid init data"}), 401

    user_info = json.loads(verified["user"])
    telegram_user_id = str(user_info["id"])

    encrypted = fernet.encrypt(session_string.encode()).decode()

    store = load_store()
    store[telegram_user_id] = encrypted
    save_store(store)

    return jsonify({"ok": True})


if __name__ == "__main__":
    # برای تست لوکال. در تولید واقعی پشت gunicorn/HTTPS واقعی اجرا کنید.
    app.run(host="0.0.0.0", port=5000, debug=True)
