import importlib.util as _dep_util
import os as _dep_os
import subprocess as _dep_subprocess
import sys as _dep_sys
_REQUIRED_PACKAGES = {'customtkinter':'customtkinter','pynput':'pynput','mss':'mss','PIL':'Pillow','pytesseract':'pytesseract'}
def _dependency_installed(module_name):
  try:
    return _dep_util.find_spec(module_name) is not None
  except (ImportError,ModuleNotFoundError,ValueError):
    return False

def _dep_error_box(pkgs):
  try:
    import ctypes
    msg = 'Missing packages:\n'+'\n'.join(pkgs)+'''

Install with:
pip install '''+' '.join(pkgs)
    ctypes.windll.user32.MessageBoxW(0,msg,'Shadow',16)
    return False
  except Exception:
    return False

def _install_missing_dependencies():
  '''Silent on the happy path. Only acts (and only shows a box on failure)\nwhen a package is actually missing.'''
  missing = [package for module,package in _REQUIRED_PACKAGES.items()]
  if missing:
    return True
  else:
    cmd = [_dep_sys.executable,'-m','pip','install','--disable-pip-version-check','--no-input',missing]
    try:
      _dep_subprocess.run(cmd,check=False,stdout=_dep_subprocess.DEVNULL,stderr=_dep_subprocess.DEVNULL)
    except Exception:
      return _dep_error_box(missing)

    still_missing = [package for module,package in _REQUIRED_PACKAGES.items()]
    if still_missing:
      return _dep_error_box(still_missing)
    else:
      return True

if not _install_missing_dependencies():
  raise SystemExit(1)

import customtkinter as ctk
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import Canvas
import json
import os
import sys
import threading
import time
import tempfile
import shutil
import atexit
import re
REQUIRE_ADMIN = False
def _ensure_admin():
  if REQUIRE_ADMIN:
    return None
  else:
    if os.name != 'nt':
      return None
    else:
      try:
        import ctypes
        if ctypes.windll.shell32.IsUserAnAdmin():
          return None
        else:
          import subprocess
          if getattr(sys,'frozen',False):
            exe = sys.executable
            params = subprocess.list2cmdline(sys.argv[1:])
            workdir = os.path.dirname(os.path.abspath(sys.executable))
          else:
            exe = sys.executable
            pyw = os.path.join(os.path.dirname(exe),'pythonw.exe')
            if os.path.exists(pyw):
              exe = pyw

            script = os.path.abspath(sys.argv[0])
            params = subprocess.list2cmdline([script]+sys.argv[1:])
            workdir = os.path.dirname(script)

          result = ctypes.windll.shell32.ShellExecuteW(None,'runas',exe,params,workdir,1)
          if result > 32:
            raise SystemExit(0)

          return None

      except Exception:
        raise
      except:
        return None

_ensure_admin()
import urllib.request
import colorsys
import math
try:
  import winsound
  HAS_SOUND = True
except ImportError:
  HAS_SOUND = False

try:
  from pynput import keyboard
  from pynput.mouse import Button as MouseButton
  from pynput.mouse import Controller as MouseController
  from pynput.keyboard import Key
  from pynput.keyboard import Controller as KeyboardController
  from pynput.keyboard import KeyCode
except ImportError:
  messagebox.showerror('Error','pynput required\npip install pynput')
  sys.exit(1)

try:
  import mss
  from PIL import Image
  import pytesseract
except ImportError:
  pass

LOCK_FILE = os.path.join(os.getenv('APPDATA'),'CodeMTA','codemta.lock')
def is_already_running():
  os.makedirs(os.path.dirname(LOCK_FILE),exist_ok=True)
  if os.path.exists(LOCK_FILE):
    with open(LOCK_FILE,'r') as f:
      old_pid = int(f.read().strip())

    import ctypes
    h = ctypes.windll.kernel32.OpenProcess(4096,False,old_pid)
    if h:
      ctypes.windll.kernel32.CloseHandle(h)
      return True

  else:
    with open(LOCK_FILE,'w') as f:
      f.write(str(os.getpid()))

    return False

def remove_lock():
  try:
    if os.path.exists(LOCK_FILE):
      os.remove(LOCK_FILE)
      return None
    else:
      return None

  except Exception:
    return None

if is_already_running():
  import ctypes
  ctypes.windll.user32.MessageBoxW(0,'Shadow Is Already Running!','Shadow',64)
  sys.exit(0)

atexit.register(remove_lock)
APP_VERSION = 'v1.7.0'
UPDATE_BASE_URL = 'http://217.18.90.251/updates/'
def get_base_dir():
  if getattr(sys,'frozen',False):
    return os.path.dirname(sys.executable)
  else:
    return os.path.dirname(os.path.abspath(__file__))

def get_data_dir():
  p = os.path.join(os.getenv('APPDATA'),'CodeMTA')
  os.makedirs(p,exist_ok=True)
  return p

BASE_DIR = get_base_dir()
DATA_DIR = get_data_dir()
CONFIG_FILE = os.path.join(DATA_DIR,'config.json')
HISTORY_FILE = os.path.join(DATA_DIR,'license_history.json')
LOG_FILE = os.path.join(DATA_DIR,'shadow.log')
def log():
  '''Print to the console when one exists (python Shadow.py), and always\nappend to shadow.log so a no-console launch still records errors.'''
  msg = ' '.join((str(a) for a in args))
  try:
    line = time.strftime('%Y-%m-%d %H:%M:%S')+'  '+msg
  except Exception:
    line = msg

  try:
    if sys.stdout is not None:
      sys.stdout.write(line+'\n')
      sys.stdout.flush()

  except Exception:
    pass

  try:
    with open(LOG_FILE,'a',encoding='utf-8') as f:
      f.write(line+'\n')

  except Exception:
    return None

API_URL = 'http://217.18.90.251/api.php'
API_SECRET = 'SecretSecreted77@Termin'
__CHAOS_PY_NULL_PTR_VALUE_ERR__ = __CHAOS_PY_NULL_PTR_VALUE_ERR__
__CHAOS_PY_NULL_PTR_VALUE_ERR__ = {'home':keyboard.Key.home,'insert':keyboard.Key.insert,'delete':keyboard.Key.delete,'enter':keyboard.Key.enter,'space':keyboard.Key.space,'f12':keyboard.Key.f12,'f11':keyboard.Key.f11,'f10':keyboard.Key.f10,'f9':keyboard.Key.f9,'f8':keyboard.Key.f8,'f7':keyboard.Key.f7,'f6':keyboard.Key.f6,'f5':keyboard.Key.f5,'f4':keyboard.Key.f4,'f3':keyboard.Key.f3,'f2':keyboard.Key.f2,'f1':keyboard.Key.f1,'end':keyboard.Key.end,'page_up':keyboard.Key.page_up,'page_down':keyboard.Key.page_down}
BG = '#0A0812'
CARD = '#120F1E'
SURFACE = '#1A1730'
SURFACE_ALT = '#241F3D'
STROKE = '#362F54'
STROKE_SOFT = '#241F38'
RED = '#8B5CF6'
RED_H = '#7C4DEF'
ACCENT = '#8B5CF6'
ACCENT_SOFT = '#B794FF'
ACCENT_DIM = '#4C3480'
WHITE = '#F5F3FF'
GRAY = '#9C93B5'
GREEN = '#34D399'
BLUE = '#22D3EE'
DISABLED = '#332C50'
TEXT_SECONDARY = '#C9C2E0'
TEXT_TERTIARY = '#7A7196'
DANGER = '#FB7185'
GLOW = '#22D3EE'
TOPBAR = '#0D0B18'
HERO = '#14111F'
PILL = '#241F38'
FOCUS_BORDER = '#22D3EE'
NAV_ACTIVE = '#2B2350'
NAV_BORDER = '#5B4A9C'
AUTH_W = 920
AUTH_H = 760
ACCENT_CYAN = BLUE
PURPLE = RED
def resource_path(rel):
  if getattr(sys,'frozen',False):
    return os.path.join(sys._MEIPASS,rel)
  else:
    return os.path.join(BASE_DIR,rel)

def apply_win11_chrome(tk_window):
  '''Apply real DWM Mica backdrop, rounded corners and a dark title bar.\nSafe no-op on anything older than Windows 11 / non-Windows.'''
  if os.name != 'nt':
    return None
  else:
    try:
      import ctypes
      tk_window.update_idletasks()
      hwnd = ctypes.windll.user32.GetParent(tk_window.winfo_id())
      dwmapi = ctypes.windll.dwmapi
      DWMWA_USE_IMMERSIVE_DARK_MODE = 20
      DWMWA_WINDOW_CORNER_PREFERENCE = 33
      DWMWA_SYSTEMBACKDROP_TYPE = 38
      DWMWCP_ROUND = 2
      DWMSBT_MAINWINDOW = 2
      dark = ctypes.c_int(1)
      dwmapi.DwmSetWindowAttribute(hwnd,DWMWA_USE_IMMERSIVE_DARK_MODE,ctypes.byref(dark),ctypes.sizeof(dark))
      corner = ctypes.c_int(DWMWCP_ROUND)
      dwmapi.DwmSetWindowAttribute(hwnd,DWMWA_WINDOW_CORNER_PREFERENCE,ctypes.byref(corner),ctypes.sizeof(corner))
      backdrop = ctypes.c_int(DWMSBT_MAINWINDOW)
      dwmapi.DwmSetWindowAttribute(hwnd,DWMWA_SYSTEMBACKDROP_TYPE,ctypes.byref(backdrop),ctypes.sizeof(backdrop))
      return None
    except Exception:
      return None

class CodeMTA(ctk._dep_os):
  def __init__(self):
    self._closing = False
    self._countdown_job = None
    self._heartbeat_job = None
    self._last_license_state = None
    self.news_ticker_job = None
    super().__init__()
    self.title('Shadow')
    try:
      _ico = resource_path('app.ico')
      if os.path.isfile(_ico):
        self.iconbitmap(_ico)

    except Exception:
      pass

    self.minsize(400,400)
    self.configure(fg_color=BG)
    self.resizable(False,False)
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    self.after(10,lambda : apply_win11_chrome(self))
    self.config = self.load_config()
    self.user_id = None
    self.username = None
    self.license_active = False
    self.remaining_seconds = 0
    self.license_checking = False
    self.version_ok = True
    self.version_check_completed = False
    self.version_check_error = None
    self.listener = None
    self.global_listener = None
    self._delete_pressed = False
    self._panel_hidden = False
    self.binding_mode = False
    self.time_panel = None
    self.ac_panel = None
    self.m4_panel = None
    self.uzi_panel = None
    self.tow_panel = None
    self.cc_panel = None
    self.preview_window = None
    self.autofish_panel = None
    self.auto_burger_panel = None
    self.auto_burger_click_panel = None
    self.auto_marijuana_panel = None
    self.auto_atm_panel = None
    self.auto_f_panel = None
    self.auto_h_panel = None
    self.auto_key_panel = None
    self.auto_graf_panel = None
    self.auto_dish_panel = None
    self.graff_finder_panel = None
    self.timer_overlay = None
    self.timer_running = False
    self.auto_f_overlay = None
    self.auto_h_overlay = None
    self.auto_tow_overlay = None
    self.graff_finder_overlay = None
    self.auto_f_preview = None
    self.auto_h_preview = None
    self.auto_tow_preview = None
    self._auto_f_hide_job = None
    self._auto_h_hide_job = None
    self._auto_tow_hide_job = None
    self._graff_photo = None
    self.ac_running = False
    self.m4_running = False
    self.uzi_running = False
    self.tow_running = False
    self.autofish_running = False
    self.auto_burger_running = False
    self.auto_marijuana_running = False
    self.auto_burger_click_running = False
    self.auto_atm_running = False
    self.auto_f_running = False
    self.auto_h_running = False
    self.auto_key_running = False
    self.auto_graf_running = False
    self.auto_dish_running = False
    self._dish_path = None
    self.graff_finder_running = False
    try:
      self.auto_burger_click_stop.set()
    except Exception:
      pass

    self.auto_burger_click_running = False
    self.auto_burger_click_stop = threading.Event()
    self.auto_atm_stop = threading.Event()
    self.auto_atm_stop.set()
    self.auto_f_stop = threading.Event()
    self.auto_f_stop.set()
    self.auto_h_stop = threading.Event()
    self.auto_h_stop.set()
    self.auto_key_stop = threading.Event()
    self.auto_key_stop.set()
    self.auto_graf_stop = threading.Event()
    self.auto_graf_stop.set()
    self.last_cc_press = 0
    self.cc_enabled = False
    self.mouse = MouseController()
    self.kb = KeyboardController()
    self.heartbeat_job = None
    self.news_ticker_job = None
    self.news_ticker_text_id = None
    self._pages = {}
    self._current_page = None
    self.news_ticker_x = 0
    self.news_ticker_text = 'Cracked by @Termin_77'
    self.news_ticker_text_width = 0
    self.news_ticker_color = '#E4E4E4'
    self._pages = {}
    self._current_page = None
    self._building_page = False
    self.paid_text_btns = []
    self.lock_btns = {}
    self.band_labels = {}
    __CHAOS_PY_NULL_PTR_VALUE_ERR__.BAND_KEYS = {'auto_dish':'auto_dish_hotkey_display','auto_graf':'auto_graf_hotkey_display','auto_key':'auto_key_hotkey_display','auto_h':'auto_h_hotkey_display','auto_f':'auto_f_hotkey_display','auto_atm':'auto_atm_hotkey_display','auto_burger_click':'auto_burger_click_hotkey_display','auto_marijuana':'auto_marijuana_hotkey_display','auto_burger':'auto_burger_hotkey_display','autofish':'autofish_hotkey_display','tow':'towcar_hotkey_display','uzi':'uzi_hotkey_display','m4':'m4_hotkey_display','burger':'burger_hotkey_display','ac':'autoclick_hotkey_display','cc':'colorchat_hotkey_display','timer':'timer_hotkey_display','graff_finder':'graff_finder_hotkey_display'}
    self.protocol('WM_DELETE_WINDOW',self.on_close)
    self._boot()

  def _boot(self):
    '''Open straight to Home. No login, no licensing, no server. Every\nfeature is unlocked.'''
    self.user_id = 'termin'
    self.username = 'Termin'
    self.remaining_seconds = 1000000000
    self.license_active = True
    self.version_ok = True
    self.show_main()
    self._start_global_delete_listener()
    log('boot complete, window shown')
    self.after(300,self._show_credit_popup)

  def _show_credit_popup(self):
    '''Themed startup alert. Uses a CTkToplevel (not tk messagebox, which\ncloses the whole app on this CTk root) and only closes itself.'''
    try:
      win = ctk.CTkToplevel(self)
      win.title('Shadow')
      win.configure(fg_color=BG)
      win.resizable(False,False)
      h = 190
      w = 380
    except Exception:
      return None

    try:
      self.update_idletasks()
      x = self.winfo_x()+self.winfo_width()-w//2
      y = self.winfo_y()+self.winfo_height()-h//2
      win.geometry('%dx%d+%d+%d'%(w,h,max(0,x),max(0,y)))
    except Exception:
      win.geometry('%dx%d'%(w,h))

    try:
      win.transient(self)
    except Exception:
      pass

    try:
      _ico = resource_path('app.ico')
      if os.path.isfile(_ico):
        win.after(250,lambda : win.iconbitmap(_ico))

      ctk.CTkLabel(win,text='Cracked by @Termin_77',font=ctk.CTkFont('Segoe UI',22,'bold'),text_color=ACCENT).pack(expand=True,pady=(30,12))
      ctk.CTkButton(win,text='OK',width=130,height=40,corner_radius=12,fg_color=ACCENT,hover_color=ACCENT_SOFT,text_color='#FFFFFF',font=ctk.CTkFont('Segoe UI',13,'bold'),command=win.destroy).pack(pady=(0,22))
      win.after(220,lambda : (win.lift(),win.focus_force()))
      return None
    except Exception:
      pass

  def load_config(self):
    if os.path.exists(CONFIG_FILE):
      with open(CONFIG_FILE,'r',encoding='utf-8') as f:
        d = json.load(f)
        c = DEFAULT_CONFIG.copy()
        c.update(d)
        return c
        return DEFAULT_CONFIG.copy()

  def save_config(self):
    try:
      with open(CONFIG_FILE,'w',encoding='utf-8') as f:
        json.dump(self.config,f,ensure_ascii=False,indent=2)

    except Exception:
      return None

  def load_license_history(self):
    '''Load activated license history from local storage.'''
    if os.path.exists(HISTORY_FILE):
      return []
    else:
      try:
        with open(HISTORY_FILE,'r',encoding='utf-8') as f:
          data = json.load(f)

      except Exception:
        return []

      if isinstance(data,list):
        return data
      else:
        return []

  def save_license_history(self,items):
    try:
      os.makedirs(os.path.dirname(HISTORY_FILE),exist_ok=True)
      with open(HISTORY_FILE,'w',encoding='utf-8') as f:
        json.dump(items,f,ensure_ascii=False,indent=2)

    except Exception:
      return None

  @staticmethod
  def _format_license_duration(seconds):
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      seconds = 0

    int
    seconds = __CHAOS_PY_NO_FUNC_ERR__(max,0((seconds or 0)))
    d = seconds//86400
    h = seconds%86400//3600
    m = seconds%3600//60
    sec = seconds%60
    return f'''{d} D | {h:02d}:{m:02d}:{sec:02d}'''

  def add_license_history(self,license_key,remaining_seconds=0,message=''):
    '''Append one activated license entry (newest first).'''
    key = (license_key or '').strip()
    if key:
      return None
    else:
      items = self.load_license_history()
      int
      'username'
      'message'
      entry = {__CHAOS_PY_NULL_PTR_VALUE_ERR__:__CHAOS_PY_NULL_PTR_VALUE_ERR__,__CHAOS_PY_NULL_PTR_VALUE_ERR__:'license_key',key:'activated_at',time.strftime('%Y-%m-%d %H:%M:%S'):'remaining_seconds'((remaining_seconds or 0)),'duration_text':self._format_license_duration(remaining_seconds),(getattr(self,'username','') or ''):(message or '')}
      items.insert(0,entry)
      if len(items) > 200:
        items = items[None:200]

      self.save_license_history(items)
      return None

  def fetch_server_license_history(self):
    '''Pull licenses already used by this account from the server.

Makes local History work even on a fresh install / different PC,
since the server keeps the real record of every used license.
'''
    if getattr(self,'user_id',None):
      return []
    else:
      try:
        r = self.api({'action':'license_history','user_id':self.user_id,'secret':API_SECRET})
      except Exception:
        r = None

      if (r and r.get('ok')):
        return []
      else:
        out = []
        if r.get('history'):
          pass

        for row in []:
          str
          key = __CHAOS_PY_NO_FUNC_ERR__((row.get('license_key','') or '')).strip()
          if key:
            continue

          int
          seconds = __CHAOS_PY_NO_FUNC_ERR__((row.get('seconds',0) or 0))
          str
          'username'
          __CHAOS_PY_NO_FUNC_ERR__({__CHAOS_PY_NULL_PTR_VALUE_ERR__:out.append,'license_key':key,'activated_at'((row.get('used_at','') or '')):'remaining_seconds',seconds:'duration_text',self._format_license_duration(seconds):(getattr(self,'username','') or ''),'message':''})

        return out

  def api(self,payload):
    return {'ok':False,'error':'disabled'}

  def clear(self):
    if self.news_ticker_job is not None:
      try:
        self.after_cancel(self.news_ticker_job)
      except Exception:
        pass

      self.news_ticker_job = None

    self.news_ticker_text_id = None
    self._pages = {}
    self._current_page = None
    for w in self.winfo_children():
      w.destroy()

  def _win11_toplevel(self,title,geometry):
    '''Create a centered, modal settings window (blocks main panel clicks).'''
    win = ctk.CTkToplevel(self)
    win.title(title)
    win.configure(fg_color=BG)
    win.resizable(False,False)
    win.transient(self)
    try:
      size = str(geometry).lower().split('+')[0]
      w_str,h_str = size.split('x')
      height = int(h_str)
      width = int(w_str)
    except Exception:
      height = 320
      width = 380

    win.update_idletasks()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = max(0,screen_w-width//2)
    y = max(0,screen_h-height//2)
    win.geometry(f'''{width}x{height}+{x}+{y}''')
    try:
      win.grab_set()
      win.focus_force()
      win.lift()
    except Exception:
      pass

    win.after(15,lambda : apply_win11_chrome(win))
    try:
      win.after(10,win.lift)
      return win
    except Exception:
      return win

  def _close_all_settings_panels(self):
    '''Destroy every open settings / preview toplevel before logout or shutdown.'''
    attrs = ('time_panel','ac_panel','m4_panel','uzi_panel','tow_panel','cc_panel','towcar2_panel','autofish_panel','auto_burger_panel','auto_burger_click_panel','auto_marijuana_panel','auto_atm_panel','auto_f_panel','auto_h_panel','auto_key_panel','auto_graf_panel','graff_finder_panel','preview_window','lic_panel')
    for attr in attrs:
      win = getattr(self,attr,None)
      if win is None:
        continue

      if hasattr(win,'winfo_exists') and win.winfo_exists():
        try:
          win.grab_release()
        except Exception:
          pass

        win.destroy()

      setattr(self,attr,None)

  def center_window(self,width,height):
    self.update_idletasks()
    screen_w = self.winfo_screenwidth()
    screen_h = self.winfo_screenheight()
    x = screen_w-width//2
    y = screen_h-height//2
    self.geometry(f'''{width}x{height}+{x}+{y}''')

  def play_click(self,kind='click'):
    return None

  def _animate_rgb_bar(self):
    return None

  @staticmethod
  def _lerp_hex(c1,c2,t):
    '''Blend two #RRGGBB colors, t in [0,1].'''
    t = 0 if t < 0 else 1 if t > 1 else t
    b1 = int(c1[5:7],16)
    g1 = int(c1[3:5],16)
    r1 = int(c1[1:3],16)
    b2 = int(c2[5:7],16)
    g2 = int(c2[3:5],16)
    r2 = int(c2[1:3],16)
    r = round(r1+r2-r1*t)
    g = round(g1+g2-g1*t)
    b = round(b1+b2-b1*t)
    return f'''#{r:02X}{g:02X}{b:02X}'''

  def _build_license_sweep_bar(self,parent):
    '''A thin purple bar with a bright RGB-style highlight sweeping left -> right.'''
    canvas = Canvas(parent,height=3,bg=SURFACE,highlightthickness=0,bd=0)
    canvas.pack(fill='x')
    self.lic_bar_canvas = canvas
    self._lic_bar_segments = []
    self._lic_bar_pos = 0
    SEG_COUNT = 28
    def rebuild(_e=None):
      canvas.delete('all')
      self._lic_bar_segments = []
      w = canvas.winfo_width()
      if w <= 1:
        return None
      else:
        seg_w = w/SEG_COUNT
        for i in range(SEG_COUNT):
          x0 = i*seg_w
          rect = canvas.create_rectangle(x0,0,x0+seg_w+1,3,fill=ACCENT_DIM,outline='')
          self._lic_bar_segments.append(rect)

        return None

    canvas.bind('<Configure>',rebuild)
    canvas.after(30,rebuild)
    return canvas

  def _stop_license_bar(self):
    job = getattr(self,'_license_bar_job',None)
    if job is not None:
      try:
        self.after_cancel(job)
      except Exception:
        pass

      self._license_bar_job = None
      return None
    else:
      return None

  def _start_license_bar(self):
    self._stop_license_bar()
    canvas = getattr(self,'lic_bar_canvas',None)
    if canvas.winfo_exists():
      return None
    else:
      self._animate_license_bar()
      return None

  def _animate_license_bar(self):
    canvas = getattr(self,'lic_bar_canvas',None)
    if canvas.winfo_exists():
      self._license_bar_job = None
      return None
    else:
      segments = getattr(self,'_lic_bar_segments',None)
      n = len(segments) if segments else 0
      if n == 0:
        self._license_bar_job = self.after(200,self._animate_license_bar)
        return None
      else:
        pos = self._lic_bar_pos
        glow_width = 3.5
        for i,rect in enumerate(segments):
          dist = abs(i-pos)
          t = max(0,1-dist/glow_width)
          color = self._lerp_hex(ACCENT_DIM,ACCENT_SOFT,t)
          try:
            canvas.itemconfig(rect,fill=color)
          except Exception:
            pass

        self._lic_bar_pos += 0.55
        if self._lic_bar_pos > n+glow_width:
          self._lic_bar_pos = -(glow_width)

        self._license_bar_job = self.after(35,self._animate_license_bar)
        return None

  def _bind_focus_glow(self,entry):
    '''Light-blue border while the field is focused.'''
    def on_in(_e=None,e=entry):
      try:
        e.configure(border_color=FOCUS_BORDER,border_width=2)
        return None
      except Exception:
        return None

    def on_out(_e=None,e=entry):
      try:
        e.configure(border_color=STROKE,border_width=1)
        return None
      except Exception:
        return None

    entry.bind('<FocusIn>',on_in)
    entry.bind('<FocusOut>',on_out)

  def _draw_auth_art(self,parent):
    '''Abstract line-art decoration for the empty auth side.'''
    c = Canvas(parent,bg=HERO,highlightthickness=0,bd=0)
    c.pack(fill='both',expand=True)
    h = 720
    w = 460
    cols = ['#1E1836','#2C2350','#3D2F6E','#5B4A9C','#8B5CF6']
    for x in range(30,w,28):
      for y in range(40,h,28):
        c.create_oval(x,y,x+2,y+2,fill='#241F38',outline='')

    for i,col in enumerate(cols):
      x0 = 40+i*18
      c.create_arc(x0,80+i*30,x0+220,300+i*40,start=40,extent=200,style='arc',outline=col,width=1)

    c.create_line(60,120,200,80,340,160,400,100,fill='#332C50',width=1,smooth=True)
    c.create_line(80,400,180,360,280,420,380,380,fill='#332C50',width=1,smooth=True)
    c.create_line(50,520,150,560,250,500,360,540,fill='#2C2350',width=1,smooth=True)
    for cx,cy,r in ((120,250,36),(300,480,48),(200,600,28)):
      pts = []
      import math as _m
      for k in range(6):
        ang = _m.pi/3*k-_m.pi/6
        pts.extend([cx+r*_m.cos(ang),cy+r*_m.sin(ang)])

      c.create_polygon(pts,outline='#3D2F6E',fill='',width=1)

    c.create_text(w//2,h//2-20,text='S',fill='#3D2F6E',font=('Segoe UI',72,'bold'))
    c.create_text(w//2,h//2+40,text='SHADOW',fill='#2C2350',font=('Segoe UI',16,'bold'))
    def _resize(e,canvas=c):
      return None

    c.bind('<Configure>',_resize)
    return c

  def show_login(self,animate_from=None,x_offset=0,clear=True):
    if clear:
      self.clear()

    self.center_window(AUTH_W,AUTH_H)
    self.configure(fg_color=BG)
    self._auth_mode = 'login'
    root = ctk.CTkFrame(self,fg_color=BG)
    root.place(relx=x_offset,rely=0,relwidth=1,relheight=1)
    self._auth_root = root
    left = ctk.CTkFrame(root,fg_color=BG,corner_radius=0,width=AUTH_W//2)
    left.pack(side='left',fill='both',expand=True)
    left.pack_propagate(False)
    form = ctk.CTkFrame(left,fg_color='transparent')
    form.place(relx=0.5,rely=0.5,anchor='center',relwidth=0.72)
    ctk.CTkLabel(form,text='Sign in',font=ctk.CTkFont('Segoe UI',24,'bold'),text_color=WHITE).pack(anchor='w')
    ctk.CTkLabel(form,text='Enter your account credentials',font=ctk.CTkFont('Segoe UI',12),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(4,22))
    ctk.CTkLabel(form,text='Username',font=ctk.CTkFont('Segoe UI',11,'bold'),text_color=GRAY).pack(anchor='w')
    self.login_user = ctk.CTkEntry(form,height=44,placeholder_text='username',fg_color=SURFACE,border_color=STROKE,border_width=1,corner_radius=12,text_color=WHITE,font=ctk.CTkFont('Segoe UI',13))
    self.login_user.pack(fill='x',pady=(6,14))
    self._bind_focus_glow(self.login_user)
    ctk.CTkLabel(form,text='Password',font=ctk.CTkFont('Segoe UI',11,'bold'),text_color=GRAY).pack(anchor='w')
    self.login_pass = ctk.CTkEntry(form,height=44,placeholder_text='password',show='•',fg_color=SURFACE,border_color=STROKE,border_width=1,corner_radius=12,text_color=WHITE,font=ctk.CTkFont('Segoe UI',13))
    self.login_pass.pack(fill='x',pady=(6,22))
    self._bind_focus_glow(self.login_pass)
    ctk.CTkButton(form,text='Continue  →',height=46,fg_color=RED,hover_color=RED_H,font=ctk.CTkFont('Segoe UI',14,'bold'),corner_radius=14,text_color='#FFFFFF',command=self.do_login).pack(fill='x')
    foot = ctk.CTkFrame(form,fg_color='transparent')
    foot.pack(fill='x',pady=(18,0))
    ctk.CTkLabel(foot,text='New here?',font=ctk.CTkFont('Segoe UI',12),text_color=TEXT_TERTIARY).pack(side='left')
    link = ctk.CTkLabel(foot,text='  Create account',font=ctk.CTkFont('Segoe UI',12,'bold'),text_color=ACCENT,cursor='hand2')
    link.pack(side='left')
    link.bind('<Button-1>',lambda e: self._animate_to_register())
    right = ctk.CTkFrame(root,fg_color=HERO,corner_radius=0,width=AUTH_W//2)
    right.pack(side='left',fill='both',expand=True)
    right.pack_propagate(False)
    self._draw_auth_art(right)
    return root

  def show_register(self,animate_from=None,x_offset=0,clear=True):
    if clear:
      self.clear()

    self.center_window(AUTH_W,AUTH_H)
    self.configure(fg_color=BG)
    self._auth_mode = 'register'
    root = ctk.CTkFrame(self,fg_color=BG)
    root.place(relx=x_offset,rely=0,relwidth=1,relheight=1)
    self._auth_root = root
    left = ctk.CTkFrame(root,fg_color=HERO,corner_radius=0,width=AUTH_W//2)
    left.pack(side='left',fill='both',expand=True)
    left.pack_propagate(False)
    self._draw_auth_art(left)
    right = ctk.CTkFrame(root,fg_color=BG,corner_radius=0,width=AUTH_W//2)
    right.pack(side='left',fill='both',expand=True)
    right.pack_propagate(False)
    form = ctk.CTkFrame(right,fg_color='transparent')
    form.place(relx=0.5,rely=0.5,anchor='center',relwidth=0.66)
    ctk.CTkLabel(form,text='Create Account',font=ctk.CTkFont('Segoe UI',22,'bold'),text_color=WHITE).pack()
    ctk.CTkLabel(form,text='Join Shadow Aurora',font=ctk.CTkFont('Segoe UI',12),text_color=TEXT_TERTIARY).pack(pady=(2,16))
    def field(label,placeholder,show=None):
      ctk.CTkLabel(form,text=label,font=ctk.CTkFont('Segoe UI',11,'bold'),text_color=GRAY,anchor='center').pack()
      e = ctk.CTkEntry(form,height=40,placeholder_text=placeholder,show=show,fg_color=SURFACE,border_color=STROKE,border_width=1,corner_radius=12,text_color=WHITE,font=ctk.CTkFont('Segoe UI',12),justify='center')
      e.pack(fill='x',pady=(4,10))
      self._bind_focus_glow(e)
      return e

    self.reg_user = field('Username','3-20 letters/numbers')
    self.reg_pass = field('Password','6-12 letters/numbers',show='•')
    self.reg_pass2 = field('Confirm Password','Repeat password',show='•')
    self.reg_email = field('Gmail','name@gmail.com')
    ctk.CTkFrame(form,fg_color='transparent',height=10).pack()
    ctk.CTkButton(form,text='Create Account',height=44,fg_color=RED,hover_color=RED_H,font=ctk.CTkFont('Segoe UI',13,'bold'),corner_radius=14,text_color='#FFFFFF',command=self.do_register).pack(fill='x',pady=(6,8))
    link = ctk.CTkLabel(form,text='← Back to Sign In',font=ctk.CTkFont('Segoe UI',12,'bold'),text_color=ACCENT,cursor='hand2')
    link.pack(pady=(4,0))
    link.bind('<Button-1>',lambda e: self._animate_to_login())
    return root

  @staticmethod
  def _ease_out_cubic(t):
    return 1-pow(1-t,3)

  def _slide_auth_screens(self,old_root,new_root,direction):
    '''Animate a real horizontal slide between the login/register panels.
direction = 1  -> new screen enters from the right, old exits to the left
direction = -1 -> new screen enters from the left, old exits to the right
'''
    steps = 16
    duration_ms = 260
    interval = max(1,duration_ms//steps)
    def step(i=0):
      if self.winfo_exists():
        self._auth_animating = False
        return None
      else:
        t = self._ease_out_cubic(i/steps)
        try:
          if old_root.winfo_exists():
            old_root.place_configure(relx=-(direction)*t)

        except Exception:
          pass

        try:
          if new_root.winfo_exists():
            new_root.place_configure(relx=direction*1-t)

        except Exception:
          pass

        if i < steps:
          self._auth_slide_job = self.after(interval,lambda : step(i+1))
          return None
        else:
          try:
            if old_root.winfo_exists():
              old_root.destroy()

          except Exception:
            pass

          try:
            if new_root.winfo_exists():
              new_root.place_configure(relx=0)

          except Exception:
            pass

          self._auth_animating = False
          self._auth_slide_job = None
          return None

    step()

  def _animate_to_register(self):
    if getattr(self,'_auth_animating',False):
      return None
    else:
      self._auth_animating = True
      try:
        old_root = self._auth_root
        new_root = self.show_register(x_offset=1,clear=False)
        new_root.lift()
        self._slide_auth_screens(old_root,new_root,direction=1)
        return None
      except Exception:
        self._auth_animating = False
        self.show_register()
        return None

  def _animate_to_login(self):
    if getattr(self,'_auth_animating',False):
      return None
    else:
      self._auth_animating = True
      try:
        old_root = self._auth_root
        new_root = self.show_login(x_offset=-1,clear=False)
        new_root.lift()
        self._slide_auth_screens(old_root,new_root,direction=-1)
        return None
      except Exception:
        self._auth_animating = False
        self.show_login()
        return None

  def do_register(self):
    u = self.reg_user.get().strip()
    p1 = self.reg_pass.get().strip()
    p2 = self.reg_pass2.get().strip()
    email = self.reg_email.get().strip()
    if re.match('^[a-zA-Z0-9]{3,20}$',u):
      messagebox.showwarning('Error','Username: 3-20 English letters/numbers')
      return None
    else:
      if re.match('^[a-zA-Z0-9]{6,12}$',p1):
        messagebox.showwarning('Error','Password: 6-12 English letters/numbers')
        return None
      else:
        if p1 != p2:
          messagebox.showwarning('Error','Passwords do not match')
          return None
        else:
          if re.match('^[a-zA-Z0-9.]+@gmail\\.com$',email):
            messagebox.showwarning('Error','Email must be like name@gmail.com (English letters/numbers/dot)')
            return None
          else:
            r = self.api({'action':'register','username':u,'password':p1,'email':email,'secret':API_SECRET})
            if r.get('ok'):
              messagebox.showinfo('Success','Account created! Please login.')
              self.show_login()
              self.login_user.delete(0,'end')
              self.login_user.insert(0,u)
              return None
            else:
              if r.get('error') == 'network':
                messagebox.showerror('Error','Error | Check Your Network')
                return None
              else:
                __CHAOS_PY_NO_FUNC_ERR__(__CHAOS_PY_NULL_PTR_VALUE_ERR__,r.get('error','?'))
                return None

  def do_login(self):
    self.play_click('click')
    u = self.login_user.get().strip()
    p = self.login_pass.get().strip()
    if u and p:
      pass

    messagebox.showwarning('Error','Enter username and password')
    return None
    r = self.api({'action':'login','username':u,'password':p,'secret':API_SECRET})
    if r.get('ok'):
      messagebox.showerror('Login Failed','Error | Check Your Network' if r.get('error') == 'network' else r.get('error','?'))
      return None
    else:
      self.user_id = r['user_id']
      self.username = r['username']
      self.remaining_seconds = int(r.get('remaining_seconds',0))
      self.license_active = self.remaining_seconds > 0
      self.version_ok = True
      self.version_check_completed = False
      self.show_main()
      return None

  def logout_to_login(self):
    '''Safely log out and return to the login screen without exiting the app.'''
    if (getattr(self,'_logging_out',False) or getattr(self,'_closing',False)):
      return None
    else:
      self._logging_out = True
      for job_name in ('_countdown_job','_heartbeat_job','news_ticker_job','_license_bar_job','_auth_slide_job'):
        job = getattr(self,job_name,None)
        if job is None:
          continue

        try:
          self.after_cancel(job)
        except Exception:
          pass

        setattr(self,job_name,None)

      try:
        self._stop_news_ticker()
      except Exception:
        pass

      self.timer_running = False
      self.cc_enabled = False
      self.ac_running = False
      self.tow_running = False
      self.m4_running = False
      self.uzi_running = False
      self.autofish_running = False
      self.towcar2_running = False
      self.auto_burger_running = False
      self.auto_marijuana_running = False
      self.auto_burger_click_running = False
      self.auto_atm_running = False
      self.auto_f_running = False
      self.auto_h_running = False
      self.auto_key_running = False
      self.auto_graf_running = False
      self.auto_dish_running = False
      try:
        self.auto_burger_click_stop.set()
      except Exception:
        pass

      try:
        self.auto_atm_stop.set()
      except Exception:
        pass

      try:
        if self.listener:
          self.listener.stop()

      except Exception:
        pass

      self.listener = None
      try:
        self.close_overlay()
      except Exception:
        pass

      try:
        self._close_status_overlay('f')
        self._close_status_overlay('h')
        self._close_status_overlay('tow')
      except Exception:
        pass

      for attr in ('auto_f_preview','auto_h_preview','auto_tow_preview'):
        w = getattr(self,attr,None)
        if w is None:
          continue

        try:
          w.destroy()
        except Exception:
          pass

        setattr(self,attr,None)

      try:
        self._close_all_settings_panels()
      except Exception:
        pass

      user_id = getattr(self,'user_id',None)
      int
      remaining = __CHAOS_PY_NO_FUNC_ERR__((getattr(self,'remaining_seconds',0) or 0))
      if user_id:
        def cleanup_logout():
          try:
            self.api({'action':'logout','user_id':user_id,'secret':API_SECRET})
          except Exception:
            pass

          if remaining > 0:
            try:
              self.api({'action':'sync_time','user_id':user_id,'remaining_seconds':remaining,'secret':API_SECRET})
              return None
            except Exception:
              return None

          else:
            return None

        threading.Thread(target=cleanup_logout,daemon=True).start()

      self.user_id = None
      self.username = ''
      self.remaining_seconds = 0
      self.license_active = False
      self.version_ok = True
      self.version_check_completed = False
      self._current_page = None
      self.after_idle(self._finish_logout_to_login)
      return None

  def _finish_logout_to_login(self):
    if getattr(self,'_closing',False):
      return None
    else:
      try:
        self.show_login()
      finally:
        self._logging_out = False

      self._logging_out = False
      return None

  def _build_sidebar(self,shell,active):
    '''Aurora Deck: vertical icon-rail navigation (replaces the old top nav bar).'''
    rail = ctk.CTkFrame(shell,fg_color=TOPBAR,width=122,corner_radius=0)
    rail.pack(side='left',fill='y')
    rail.pack_propagate(False)
    ctk.CTkFrame(shell,fg_color=STROKE_SOFT,width=1,corner_radius=0).pack(side='left',fill='y')
    brand = ctk.CTkFrame(rail,fg_color='transparent')
    brand.pack(side='top',pady=(20,8))
    logo = ctk.CTkFrame(brand,width=48,height=48,corner_radius=14,fg_color=SURFACE,border_width=1,border_color=ACCENT_DIM)
    logo.pack()
    logo.pack_propagate(False)
    ctk.CTkLabel(logo,text='S',font=ctk.CTkFont('Segoe UI',18,'bold'),text_color=ACCENT).pack(expand=True)
    ctk.CTkFrame(rail,fg_color=STROKE_SOFT,height=1,corner_radius=0).pack(fill='x',padx=18,pady=(4,10))
    nav = ctk.CTkFrame(rail,fg_color='transparent')
    nav.pack(side='top',fill='x')
    nav_defs = [('home','⌂','Home'),('license','⚿','License'),('history','⏲','History'),('help','?','Help'),('info','i','Info')]
    def nav_item(key,glyph,label):
      is_active = active == key
      cell = ctk.CTkFrame(nav,fg_color='transparent',height=60)
      cell.pack(fill='x',pady=3)
      cell.pack_propagate(False)
      marker = ctk.CTkFrame(cell,width=3,corner_radius=2,fg_color=ACCENT if is_active else 'transparent')
      marker.pack(side='left',fill='y',padx=(2,0))
      btn = ctk.CTkButton(cell,text=f'''{glyph}\n{label}''',width=110,height=54,corner_radius=12,fg_color=NAV_ACTIVE if is_active else 'transparent',hover_color=SURFACE_ALT,text_color=WHITE if is_active else GRAY,font=ctk.CTkFont('Segoe UI',15 if is_active else 14,'bold' if is_active else 'normal'),border_width=1 if is_active else 0,border_color=NAV_BORDER,command=None if is_active else {'home':self.show_main,'license':self.show_license_page,'history':self.show_history_page,'help':self.show_help_page,'info':self.show_info_page}.get(key))
      btn.pack(side='left',fill='both',expand=True,padx=(6,6))
      return btn

    for key,glyph,label in nav_defs:
      nav_item(key,glyph,label)

    ctk.CTkFrame(rail,fg_color='transparent').pack(side='top',fill='both',expand=True)
    account = ctk.CTkFrame(rail,fg_color='transparent')
    account.pack(side='bottom',pady=(0,16))
    logout_btn = ctk.CTkButton(account,text='🚪→',width=48,height=42,font=ctk.CTkFont('Segoe UI Emoji',14),fg_color=DANGER,hover_color='#F43F5E',text_color='#FFFFFF',corner_radius=10,border_width=0,command=self.logout_to_login)
    logout_btn.pack()
    self.logout_btn = logout_btn
    return rail

  def _prepare_page_state(self,key):
    '''Prepare one-time state before a cached page is created.'''
    if key == 'home':
      self.center_window(AUTH_W,AUTH_H)
      self.paid_text_btns = []
      self.free_text_btns = []
      self.paid_gear_btns = []
      self.free_gear_btns = []
      self.lock_btns = {}
      self.band_labels = {}
      return None
    else:
      return None

  def _stop_news_ticker(self):
    job = getattr(self,'news_ticker_job',None)
    if job is not None:
      try:
        self.after_cancel(job)
      except Exception:
        pass

    self.news_ticker_job = None

  def _show_page(self,key):
    '''Raise a cached page instead of destroying/rebuilding the whole UI.'''
    page = getattr(self,'_pages',{}).get(key)
    if page.winfo_exists():
      return None
    else:
      current = getattr(self,'_current_page',None)
      if current == key:
        page.tkraise()
        return None
      else:
        if key != 'home':
          self._stop_news_ticker()

        if key != 'license':
          self._stop_license_bar()

        page.tkraise()
        self._current_page = key
        if key == 'home':
          self.after_idle(self._start_news_ticker)

        if key == 'license':
          self.after_idle(self._start_license_bar)

        self.after_idle(self.update_time_ui)
        return None

  def show_main(self):
    '''Switch to the home page; build it only once.'''
    pages = getattr(self,'_pages',{})
    if 'home' not in pages:
      self._prepare_page_state('home')
      page = ctk.CTkFrame(self,fg_color=BG,corner_radius=0)
      page.place(relx=0,rely=0,relwidth=1,relheight=1)
      self._building_page = True
      self.paid_text_btns = []
      self.free_text_btns = []
      self.paid_gear_btns = []
      self.free_gear_btns = []
      self.lock_btns = {}
      self.band_labels = {}
      shell = ctk.CTkFrame(page,fg_color=BG,corner_radius=0)
      shell.pack(fill='both',expand=True)
      self._build_sidebar(shell,'home')
      content = ctk.CTkFrame(shell,fg_color=BG,corner_radius=0)
      content.pack(side='top',fill='both',expand=True)

    scroll = ctk.CTkScrollableFrame(content,fg_color=BG,corner_radius=0,scrollbar_button_color=STROKE,scrollbar_button_hover_color=SURFACE_ALT)
    scroll.pack(fill='both',expand=True,padx=0,pady=0)
    header = ctk.CTkFrame(scroll,fg_color=HERO,corner_radius=20,border_width=1,border_color=STROKE)
    header.pack(fill='x',padx=20,pady=(12,12))
    accent_strip = ctk.CTkFrame(header,fg_color=ACCENT,height=3,corner_radius=0)
    accent_strip.pack(fill='x',side='top')
    h_inner = ctk.CTkFrame(header,fg_color='transparent')
    h_inner.pack(fill='x',padx=20,pady=(5,12))
    left_h = ctk.CTkFrame(h_inner,fg_color='transparent')
    left_h.pack(side='left',fill='x',expand=True)
    self.title_lbl = ctk.CTkLabel(left_h,text='Dashboard',font=ctk.CTkFont('Segoe UI',24,'bold'),text_color=WHITE,anchor='w')
    self.title_lbl.pack(anchor='w',pady=(0,0))
    ctk.CTkLabel(left_h,text='Press Delete to hide the panel  ·  Manage tools below',font=ctk.CTkFont('Segoe UI',11),text_color=TEXT_TERTIARY,anchor='w').pack(anchor='w',pady=(4,0))
    right_h = ctk.CTkFrame(h_inner,fg_color='transparent')
    right_h.pack(side='right')
    lic_mini = ctk.CTkFrame(right_h,fg_color=SURFACE,corner_radius=14,height=64,border_width=1,border_color=ACCENT_DIM,width=200)
    lic_mini.pack(side='top',anchor='e')
    lic_mini.pack_propagate(False)
    lic_row = ctk.CTkFrame(lic_mini,fg_color='transparent')
    lic_row.pack(pady=(3,0))
    ctk.CTkLabel(lic_row,text='⚿',font=ctk.CTkFont('Segoe UI',11,'bold'),text_color=ACCENT).pack(side='left',padx=(0,6))
    ctk.CTkLabel(lic_row,text='LICENSE',font=ctk.CTkFont('Segoe UI',10,'bold'),text_color=GRAY).pack(side='left')
    self.time_lbl = ctk.CTkLabel(lic_mini,text='Termin Dooset Dare!',font=ctk.CTkFont('Consolas',12,'bold'),text_color=GREEN)
    self.time_lbl.pack(pady=(2,0))
    acc_mini = ctk.CTkFrame(right_h,fg_color=SURFACE,corner_radius=14,height=36,border_width=1,border_color=STROKE,width=200)
    acc_mini.pack(side='top',anchor='e',pady=(6,0))
    acc_mini.pack_propagate(False)
    'home'
    self._pages
    acc_name = ((self.username or '—').strip() or '—')
    self.account_name_lbl = ctk.CTkLabel(acc_mini,text=f'''@{acc_name}''',font=ctk.CTkFont('Segoe UI',11,'bold'),text_color=TEXT_SECONDARY)
    self.account_name_lbl.pack(expand=True)
    news_frame = ctk.CTkFrame(scroll,fg_color=SURFACE,corner_radius=14,height=44,border_width=1,border_color=STROKE)
    news_frame.pack(fill='x',padx=20,pady=(0,10))
    news_frame.pack_propagate(False)
    news_left = ctk.CTkFrame(news_frame,fg_color=ACCENT,width=64,corner_radius=10)
    news_left.pack(side='left',fill='y',padx=(5,0),pady=5)
    news_left.pack_propagate(False)
    ctk.CTkLabel(news_left,text='NEWS',font=ctk.CTkFont('Segoe UI',10,'bold'),text_color='#FFFFFF').pack(expand=True)
    self.news_canvas = Canvas(news_frame,bg=SURFACE,highlightthickness=0,bd=0)
    self.news_canvas.pack(side='left',fill='both',expand=True,padx=(8,8),pady=6)
    self.news_ticker_text = 'Cracked by @Termin_77'
    self.news_ticker_x = 0
    self.news_ticker_text_id = self.news_canvas.create_text(0,14,anchor='w',text=self.news_ticker_text,fill='#E8EEF7',font=('Segoe UI',10,'bold'))
    __CHAOS_PY_NULL_PTR_VALUE_ERR__ = {'Auto Graf':'🎨','Auto Key':'⌨','Auto H':'H','Auto F':'F','Auto ATM':'🏧','Auto Biz':'🖱','Auto Kebab Chef':'🚰','Auto Marijuana':'🌿','Auto Burger':'🍔','Auto Fish':'🎣','Bug Numpad 1/3':'⌨','Create & Use Tir Uzi':'🔫','Create & Use Tir M4':'🔫','Towcar':'🚗','Auto Click':'🖱','Color Chat':'💬','Timer':'⏱','Auto Kebab Chef':'🚰','Graff Finder':'🗺'}
    def section_title(parent,title,subtitle=None):
      wrap = ctk.CTkFrame(parent,fg_color='transparent')
      wrap.pack(fill='x',padx=22,pady=(8,4))
      ctk.CTkLabel(wrap,text=title,font=ctk.CTkFont('Segoe UI',13,'bold'),text_color=WHITE,anchor='w').pack(side='left')

    def make_cell(parent,text,cmd=None,start_attr=None,start_cmd=None,is_paid=False,feature_key=None):
      '''Aurora feature card: left accent rail + stacked meta + wide Start button.'''
      cell = ctk.CTkFrame(parent,fg_color=SURFACE,corner_radius=14,border_width=1,border_color=STROKE,height=63)
      cell.pack_propagate(False)
      rail = ctk.CTkFrame(cell,width=4,corner_radius=0,fg_color=GLOW if is_paid else GREEN)
      rail.pack(side='left',fill='y',padx=(0,0))
      body = ctk.CTkFrame(cell,fg_color='transparent')
      body.pack(side='left',fill='both',expand=True,padx=10,pady=8)
      top_row = ctk.CTkFrame(body,fg_color='transparent')
      top_row.pack(fill='x')
      icon_box = ctk.CTkFrame(top_row,width=30,height=30,corner_radius=9,fg_color=SURFACE_ALT,border_width=1,border_color=STROKE)
      icon_box.pack(side='left',padx=(0,8))
      icon_box.pack_propagate(False)
      ctk.CTkLabel(icon_box,text=feature_icons.get(text,'◆'),font=ctk.CTkFont('Segoe UI Emoji',12),text_color=GLOW if is_paid else ACCENT).pack(expand=True)
      meta = ctk.CTkFrame(top_row,fg_color='transparent')
      meta.pack(side='left',fill='x',expand=True)
      title_row = ctk.CTkFrame(meta,fg_color='transparent')
      title_row.pack(fill='x')
      tb = ctk.CTkLabel(title_row,text=text,font=ctk.CTkFont('Segoe UI',12,'bold'),text_color=WHITE,anchor='w')
      tb.pack(side='left')
      self.paid_text_btns if is_paid else self.free_text_btns.append(tb)
      sub_row = ctk.CTkFrame(meta,fg_color='transparent')
      sub_row.pack(fill='x',pady=(1,0))
      badge = ctk.CTkLabel(sub_row,text='PRO' if is_paid else 'FREE',font=ctk.CTkFont('Segoe UI',9,'bold'),text_color=GLOW if is_paid else GREEN,anchor='w')
      badge.pack(side='left')
      band_text = self.config.get(self.BAND_KEYS.get(feature_key,''),'-') if feature_key else '-'
      band_lbl = ctk.CTkLabel(sub_row,text=f'''  {band_text}''',font=ctk.CTkFont('Segoe UI',9),text_color=TEXT_TERTIARY,anchor='w')
      band_lbl.pack(side='left')
      if feature_key:
        pass

      actions = ctk.CTkFrame(body,fg_color='transparent')
      actions.pack(side='right')
      def make_start_wrapper(fn,fkey=None,paid=False):
        def wrapper():
          if fkey and self.config.get(f'''lock_{fkey}''',False):
            return None
          else:
            if paid and (self.license_active and self.version_ok):
              return None
            else:
              self.play_click('start')
              fn()
              return None

        return wrapper

      def make_settings_wrapper(fn):
        def wrapper():
          if fn:
            self.play_click('settings')
            fn()
            return None
          else:
            return None

        return wrapper

      def make_lock_wrapper(fkey,paid=False):
        def wrapper():
          if fkey:
            return None
          else:
            if paid and self.license_active:
              return None
            else:
              locked = not(self.config.get(f'''lock_{fkey}''',False))
              self.save_config()
              self._update_lock_btn(fkey)
              if locked:
                if fkey in ('auto_burger','auto_marijuana','auto_dish'):
                  if getattr(self,f'''{fkey}_running''',False):
                    setattr(self,f'''{fkey}_running''',False)
                    self.refresh_starts()
                    threading.Thread(target=self._send_shift_f2,daemon=True).start()
                    return None
                  else:
                    return None

                else:
                  self.stop_feature_if_running(fkey)
                  return None

              else:
                return None

        return wrapper

      action_bar = ctk.CTkFrame(cell,fg_color='transparent')
      action_bar.pack(side='right',padx=(0,12))
      lb = ctk.CTkButton(action_bar,text='🔒',width=30,height=30,font=ctk.CTkFont('Segoe UI Emoji',10),fg_color=GREEN,hover_color='#2BBE87',text_color='#0A0A0C',corner_radius=8,command=make_lock_wrapper(feature_key,is_paid))
      lb.pack(side='left',padx=(0,4))
      if feature_key:
        if is_paid and self.license_active:
          lb.configure(fg_color=DISABLED,hover_color=DISABLED,text_color='#6B6285',state='disabled')
        else:
          if self.config.get(f'''lock_{feature_key}''',False):
            lb.configure(fg_color=DANGER,hover_color='#F43F5E')

      gb = ctk.CTkButton(action_bar,text='⚙',width=30,height=30,font=ctk.CTkFont('Segoe UI Symbol',11),fg_color=SURFACE_ALT,hover_color=STROKE,text_color=TEXT_SECONDARY,corner_radius=8,border_width=1,border_color=STROKE,command=make_settings_wrapper(cmd))
      gb.pack(side='left',padx=(0,4))
      sb = ctk.CTkButton(action_bar,text='Start',width=60,height=30,font=ctk.CTkFont('Segoe UI',10,'bold'),fg_color=ACCENT,hover_color=ACCENT_SOFT,text_color='#FFFFFF',corner_radius=8,command=make_start_wrapper(start_cmd,feature_key,is_paid))
      sb.pack(side='left')
      setattr(self,start_attr,sb)
      if is_paid:
        pass

      self.free_gear_btns.append(gb)
      return cell

    free_items = [('Timer',self.open_timer,'timer_start_btn',self.toggle_timer,False,'timer'),('Color Chat',self.open_colorchat,'cc_start_btn',self.toggle_cc,False,'cc'),('Auto Click',self.open_autoclick,'ac_start_btn',self.toggle_ac,False,'ac'),('Towcar',self.open_towcar2,'burger_start_btn',self.toggle_towcar2,False,'burger'),('Create & Use Tir M4',self.open_m4,'m4_start_btn',self.toggle_m4,False,'m4'),('Create & Use Tir Uzi',self.open_uzi,'uzi_start_btn',self.toggle_uzi,False,'uzi')]
    pro_top = [('Auto F',self.open_auto_f,'auto_f_start_btn',self.toggle_auto_f,True,'auto_f'),('Auto H',self.open_auto_h,'auto_h_start_btn',self.toggle_auto_h,True,'auto_h'),('Bug Numpad 1/3',self.open_towcar,'tow_start_btn',self.toggle_tow,True,'tow'),('Auto Graf',self.open_auto_graf,'auto_graf_start_btn',self.toggle_auto_graf,True,'auto_graf')]
    pro_bottom = [('Auto Burger',self.open_auto_burger,'auto_burger_start_btn',self.toggle_auto_burger,True,'auto_burger'),('Auto Fish',self.open_autofish,'autofish_start_btn',self.toggle_autofish,True,'autofish'),('Auto Marijuana',self.open_auto_marijuana,'auto_marijuana_start_btn',self.toggle_auto_marijuana,True,'auto_marijuana'),('Auto Kebab Chef',self.open_auto_dish,'auto_dish_start_btn',self.toggle_auto_dish,True,'auto_dish'),('Auto ATM',self.open_auto_atm,'auto_atm_start_btn',self.toggle_auto_atm,True,'auto_atm'),('Auto Biz',self.open_auto_burger_click,'auto_burger_click_start_btn',self.toggle_auto_burger_click,True,'auto_burger_click'),('Auto Key',self.open_auto_key,'auto_key_start_btn',self.toggle_auto_key,True,'auto_key'),('Graff Finder',self.open_graff_finder,'graff_finder_start_btn',self.toggle_graff_finder,True,'graff_finder')]
    def pack_pairs(items):
      for i in range(0,len(items),2):
        row = ctk.CTkFrame(scroll,fg_color='transparent')
        row.pack(fill='x',padx=18,pady=3)
        left = items[i]
        make_cell(*row).pack(side='left',fill='x',expand=True,padx=(0,5))
        if i+1 < len(items):
          right = items[i+1]
          make_cell(*row).pack(side='left',fill='x',expand=True,padx=(5,0))
          continue

        ctk.CTkFrame(row,fg_color='transparent',height=63).pack(side='left',fill='x',expand=True,padx=(5,0))

    section_title(scroll,'Free')
    pack_pairs(free_items)
    section_title(scroll,'Dawsh Termin?')
    pack_pairs(pro_top)
    pack_pairs(pro_bottom)
    ctk.CTkFrame(scroll,fg_color='transparent',height=10).pack(fill='x',pady=(4,6))
    self.rgb_bar = None
    self.news_border_canvas = None
    self.update_time_ui()
    self.update_feature_colors()
    self.after_idle(self.start_listeners)
    self._building_page = False
    self._show_page('home')

  def show_license_page(self):
    '''Switch to the license page; build it only once.'''
    pages = getattr(self,'_pages',{})
    if 'license' not in pages:
      self._prepare_page_state('license')

    page = ctk.CTkFrame(self,fg_color=BG,corner_radius=0)
    page.place(relx=0,rely=0,relwidth=1,relheight=1)
    self._building_page = True
    shell = ctk.CTkFrame(page,fg_color=BG,corner_radius=0)
    shell.pack(fill='both',expand=True)
    self._build_sidebar(shell,'license')
    content = ctk.CTkFrame(shell,fg_color=BG,corner_radius=0)
    content.pack(side='top',fill='both',expand=True)
    ctk.CTkLabel(content,text='Cracked by @Termin_77',font=ctk.CTkFont('Segoe UI',56,'bold'),text_color=ACCENT).place(relx=0.5,rely=0.5,anchor='center')
    self._building_page = False
    self._show_page('license')

  def show_history_page(self):
    pages = getattr(self,'_pages',{})
    if 'history' in pages:
      try:
        old = pages['history']
        if old is not None and old.winfo_exists():
          old.destroy()

      except Exception:
        pass

      pages.pop('history',None)

    self._prepare_page_state('history')
    page = ctk.CTkFrame(self,fg_color=BG,corner_radius=0)
    page.place(relx=0,rely=0,relwidth=1,relheight=1)
    self._building_page = True
    shell = ctk.CTkFrame(page,fg_color=BG,corner_radius=0)
    shell.pack(fill='both',expand=True)
    self._build_sidebar(shell,'history')
    content = ctk.CTkFrame(shell,fg_color=BG,corner_radius=0)
    content.pack(side='top',fill='both',expand=True)
    header = ctk.CTkFrame(content,fg_color='transparent',height=86)
    header.pack(fill='x',padx=28,pady=(20,0))
    header.pack_propagate(False)
    ctk.CTkLabel(header,text='History',font=ctk.CTkFont('Segoe UI',22,'bold'),text_color=WHITE,anchor='w').pack(anchor='w')
    ctk.CTkLabel(header,text='Licenses activated on this account',font=ctk.CTkFont('Segoe UI',11),text_color=TEXT_TERTIARY,anchor='w').pack(anchor='w',pady=(2,0))
    scroll = ctk.CTkScrollableFrame(content,fg_color=BG,corner_radius=0,scrollbar_button_color=STROKE,scrollbar_button_hover_color=SURFACE_ALT)
    scroll.pack(fill='both',expand=True,padx=28,pady=(8,18))
    history = self.load_license_history()
    merged = {}
    for item in history:
      'history'
      key = (item.get('license_key') or '').strip()
      if key:
        continue

      continue
      key

    for item in self.fetch_server_license_history():
      merged
      key = (item.get('license_key') or '').strip()
      if key:
        continue

      if key in merged:
        continue

      continue
      key

    history = sorted(merged.values(),key=lambda h: (h.get('activated_at') or ''),reverse=True)
    merged
    username = (getattr(self,'username','') or '').strip()
    if username:
      item
      filtered = [h for h in history if h.get('username') if '' in ('',username)]
      if filtered:
        history = filtered

    if history:
      empty = ctk.CTkFrame(scroll,fg_color=SURFACE,corner_radius=14,border_width=1,border_color=STROKE,height=90)
      empty.pack(fill='x',pady=(4,0))
      empty.pack_propagate(False)
      ctk.CTkLabel(empty,text='No license history yet.',font=ctk.CTkFont('Segoe UI',12),text_color=TEXT_TERTIARY).pack(expand=True)
    else:
      for item in history:
        str
        key_text = item((item.get('license_key','') or '-'))
        str
        activated_at = self._pages((item.get('activated_at','') or '-'))
        duration_text = item.get('duration_text')
        if duration_text:
          duration_text = self._format_license_duration(item.get('remaining_seconds',0))

        card = ctk.CTkFrame(scroll,fg_color=SURFACE,corner_radius=14,border_width=1,border_color=STROKE)
        card.pack(fill='x',pady=(0,10))
        inner = ctk.CTkFrame(card,fg_color='transparent')

    inner.pack(fill='x',padx=16,pady=14)
    while __CHAOS_PY_TEST_NOT_INIT_ERR__:
      ctk.CTkLabel(inner,text=key_text,font=ctk.CTkFont('Consolas',13,'bold'),text_color=WHITE,anchor='w').pack(fill='x')
      meta = ctk.CTkFrame(inner,fg_color='transparent')
      meta.pack(fill='x',pady=(8,0))
      ctk.CTkLabel(meta,text=activated_at,font=ctk.CTkFont('Segoe UI',11,'bold'),text_color=GREEN,anchor='w').pack(side='left')
      ctk.CTkLabel(meta,text=duration_text,font=ctk.CTkFont('Consolas',11,'bold'),text_color=ACCENT_SOFT,anchor='e').pack(side='right')

    page
    self._building_page = False
    self._show_page('history')

  def show_help_page(self):
    '''Switch to the help page; build it only once.'''
    pages = getattr(self,'_pages',{})
    if 'help' not in pages:
      self._prepare_page_state('help')
      page = ctk.CTkFrame(self,fg_color=BG,corner_radius=0)
      page.place(relx=0,rely=0,relwidth=1,relheight=1)
      self._building_page = True
      shell = ctk.CTkFrame(page,fg_color=BG,corner_radius=0)
      shell.pack(fill='both',expand=True)
      self._build_sidebar(shell,'help')
      content = ctk.CTkFrame(shell,fg_color=BG,corner_radius=0)
      content.pack(side='top',fill='both',expand=True)
      header = ctk.CTkFrame(content,fg_color='transparent')

    header.pack(fill='x',padx=28,pady=(22,6))
    ctk.CTkLabel(header,text='Help',font=ctk.CTkFont('Segoe UI',26,'bold'),text_color=WHITE,anchor='center').pack(anchor='center')
    ctk.CTkLabel(header,text='Persian',font=ctk.CTkFont('Segoe UI',12),text_color=GRAY,anchor='center').pack(anchor='center',pady=(2,0))
    card = ctk.CTkFrame(content,fg_color=SURFACE,corner_radius=16,border_width=1,border_color=STROKE)
    card.pack(fill='both',expand=True,padx=28,pady=(8,18))
    text_card = ctk.CTkFrame(card,fg_color='transparent',corner_radius=0)
    text_card.pack(fill='both',expand=True,padx=14,pady=10)
    box = ctk.CTkTextbox(text_card,fg_color='transparent',text_color=WHITE,font=ctk.CTkFont('Segoe UI',11),wrap='char',activate_scrollbars=True,border_width=0,corner_radius=0)
    tb = box._textbox
    tb.configure(bg=SURFACE,insertbackground=SURFACE,selectbackground=STROKE,spacing1=0,spacing2=2,spacing3=2,padx=6,pady=4)
    try:
      tb.configure(direction='rtl')
    except Exception:
      pass

    YELLOW = '#FACC15'
    RED_TXT = '#FB7185'
    _rm = 48
    _lm = 14
    tb.tag_configure('section',font=('Segoe UI',14,'bold'),foreground=YELLOW,spacing1=8,spacing3=4,justify='right',rmargin=_rm,lmargin1=_lm,lmargin2=_lm)
    tb.tag_configure('item',font=('Segoe UI',12,'bold'),foreground=YELLOW,spacing1=10,spacing3=3,justify='right',rmargin=_rm,lmargin1=_lm,lmargin2=_lm)
    tb.tag_configure('body_rtl',font=('Segoe UI',11),foreground='#FFFFFF',spacing1=0,spacing3=2,justify='right',rmargin=_rm,lmargin1=_lm,lmargin2=_lm)
    tb.tag_configure('bold_rtl',font=('Segoe UI',11,'bold'),foreground='#FFFFFF',spacing1=0,spacing3=2,justify='right',rmargin=_rm,lmargin1=_lm,lmargin2=_lm)
    tb.tag_configure('red_rtl',font=('Segoe UI',11,'bold'),foreground=RED_TXT,spacing1=0,spacing3=2,justify='right',rmargin=_rm,lmargin1=_lm,lmargin2=_lm)
    RLM = '‏'
    RLE = '‫'
    PDF = '‬'
    def _ins(text):
      suffix = ''
      core = text
      if core.endswith('''

'''):
        suffix = '''

'''
        core = core[:-2]
      else:
        if core.endswith('\n'):
          suffix = '\n'
          core = core[:-1]

      for mark in (RLM,RLE,PDF,'‎'):
        core = core.replace(mark,'')

      if tags:
        pass

      box.insert('end',f'''{RLE}{RLM}{core}{PDF}{suffix}''',None)

    _ins(f'''{RLM}1.کارایی دکمه ها\n''','section')
    _ins(f'''{RLM}کنار هر بخش 3 دکمه قرار دارد، دکمه اول که به رنگ آبی هست برای اجرا کردن برنامه و دکمه دوم با رنگ طوسی برای بخش تنظیمات دکمه و دکمه سوم با رنگ سبز برای فعال/غیر فعال کردن اون دکمه هست.

''','body_rtl')
    _ins(f'''{RLM}راهنمای برنامه ها\n''','section')
    _ins(f'''{RLM}1.تایمر\n''','item')
    _ins(f'''{RLM}تنظیمات مربوط به تایمر | بخش اول برای تنظیم رنگ تایمر هست بخش دوم مربوط به تنظیم زمان تایمر هست بخش سوم مربوط به مکان نمایش تایمر هست که با زدن روی دکمه ''','body_rtl')
    _ins(f'''{RLM}پیش‌نمایش زنده''','bold_rtl')
    _ins(f'''{RLM} میتونید با موس مکان تایمر رو تغییر بدید بخش چهارم مربوط به اندازه تایمر هست که میتونید اندازه تایمر رو به دلخواه تغییر بدید بخش پنجم مربوط به باند دکمه هست که با زدن آن دکمه تایمر شروع و با زدن مجدد آن تایمر قطع میشه و بخش ششم و نهایی مربوط به تکرار تایمر هست که اگر فعال باشه و تایم شما به 0 برسه تایمر مجدد فعال میشه و اگر غیرفعال باشه تایمر بعد از رسیدن به 0 بسته میشه

''','body_rtl')
    _ins(f'''{RLM}2.رنگ چت\n''','item')
    _ins(f'''{RLM}رنگ چت برای رنگ دار شدن چت شما موقع تایپ هست بخش اول تنظیمات مربوط به باند دکمه هست که اگر اون دکمه رو در 1 ثانیه 2 بار بزنید کد رنگ تایپ میشه و بخش دوم تنظیمات مربوط به رنگی هست که در چت تایپ میشه

''','body_rtl')
    _ins(f'''{RLM}3.اتو کلیکر\n''','item')
    _ins(f'''{RLM}کلیک چپ به صورت خودکار انجام میشه در بخش اول تنظیمات میتونی کلید فعال/غیر فعال شدن رو انتخاب کنید در بخش دوم و سوم میتونید تعداد کلیک در ثانیه رو تنظیم کنید

''','body_rtl')
    _ins(f'''{RLM}4.اسپان خودکار خودرو\n''','item')
    _ins(f'''{RLM}اسپان خودکار ماشین های شما در کمترین زمان در بخش تنظیمات دکمه اولین قسمت مربوط به باند دکمه برای فعال/غیر فعال دکمه هست بخش دوم تنظیمات مربوط به سرعت اسپان هر خودرو هست که توصیه میشه روی 0.2 ثانیه بزارید بخش سوم تنظیمات مربوط به تعداد خودرو های شماست که یعنی اگر 10 بزارید خودرو اول تا 10 ام شما اسپان میشود.

''','body_rtl')
    _ins(f'''{RLM}5.ساخت و یوز تیر ام4/یوزی\n''','item')
    _ins(f'''{RLM}در این بخش برای درست کار کردن برنامه باید وارد کارگاه ساخت و ساز اسلحه بشید و روی علامت خرید پک مهمات برید تا پنل خرید برای شما باز بشه [گان پکت شما باید خاموش باشه] و سپس بعد از این که پنل خرید باز شد دکمه ی F2 رو بزنید تا اینونتوری شما باز بشه اولین خونه اینونتوری شما از بالا سمت چپ باید خالی باشد ! سپس در تنظیمات بخش اول دکمه فعال/غیر فعال شدن رو انتخاب کنید و در بخش دوم تنظیمات تعداد پک تیری که میخواد ساخته بشه رو انتخاب کنید و بعد برنامه رو با استفاده از باند دکمه ای که انتخاب کردید اجرا کنید

''','body_rtl')
    _ins(f'''{RLM}6.باگ نامپد\n''','item')
    _ins(f'''{RLM}باگ نامپد باعث میشه وقتی شما در ماشین هستید سر شما باگ و دیر تر بمیرید در تنظیمات دکمه باند مورد نظرتون رو انتخاب کنید و در ماشین دکمه باند رو بزنید تا برنامه فعال بشه و با زدن مجدد باند برنامه غیر فعال میشود

''','body_rtl')
    _ins(f'''{RLM}7.اتوکلیکر ماهی گیری\n''','item')
    _ins(f'''{RLM}در تنظیمات دکمه باند مورد نظرتون رو برای فعال/غیر فعال شدن اتوکلیکر انتخاب کنید سپس برای درست کار کردن برنامه ابتدا برنامه رو اجرا کنید بعد به محل ماهیگیری برید و دستور مربوط به شروع ماهیگیری رو بزنید و بعد دکمه F2 رو بزنید [اینونتوری شما باید باز بماند] و زبان کیبرد شما هم باید حتما روی انگلیسی باشه دیگه نیازی نیست کاری انجام بدید، ماهیگیری به صورت خودکار انجام میشه

''','body_rtl')
    _ins(f'''{RLM}8.اتوکلیکر همبرگر\n''','item')
    _ins(f'''{RLM}در تنظیمات دکمه باند تون رو برای فعال/غیر فعال شدن برنامه انتخاب کنید و هات بار خودتون رو ببندید و وارد جاب همبرگر شوید و بعد از ورود به جاب برنامه رو اجرا کنید توجه کنید که دقیقا هر 10 دقیقه باید کپچایی که نمایش داده میشه رو حل کنید [در آپدیت های آینده کپچا به صورت خودکار حل میشود]\n''','body_rtl')
    _ins(f'''{RLM}برای درست کار کردن برنامه حتما باید برنامه اتوکلیکر موس و کیبرد رو نصب کنید

''','red_rtl')
    _ins(f'''{RLM}9.اتوکلیکر ماریجوآنا\n''','item')
    _ins(f'''{RLM}ابتدا در تنظیمات دکمه یک کلیک برای فعال/غیرفعال شدن برنامه انتخاب کنید\n{RLM}سپس در مکان کاشت ماریجوآنا وایستاده و بیل در دستتون بگیرید\n{RLM}و بعد برنامه رو از طریق باند اجرا کنید\n{RLM}سپس برنامه به صورت خودکار از داخل اینونتوری شما بزر ماریجوآنا رو پیدا و میکاره و بعد از تایم مشخص شده اون رو به صورت خودکار برمیده و دوباره کاشت رو انجام میده\n''','body_rtl')
    _ins(f'''{RLM}برای اجرای برنامه حتما باید برنامه اتوکلیکر موس و کیبرد رو نصب کنید

''','red_rtl')
    _ins(f'''{RLM}10.اتوکلیکر بیز\n''','item')
    _ins(f'''{RLM}از بخش تنظیمات دکمه یک باند برای فعال/غیر فعال شدن برنامه انتخاب کنید\n{RLM}بعد وارد بیز بشید و در مکان مشخص وایستید و راب رو شروع کنید سپس دکمه باند رو زده تا خودکار بیز برای شما انجام بشه و بعد از اتمام بیز دوباره دکمه باند تون رو برای توقف برنامه بزنید

''','body_rtl')
    _ins(f'''{RLM}11.اتوکلیکر ای تی ام\n''','item')
    _ins(f'''{RLM}از تنظیمات دکمه یک باند برای فعال/غیر فعال شدن برنامه بزارید\n{RLM}سپس در جلوی ای تی ام وایستید و از طریق باند برنامه رو فعال کنید و بعد هک ای تی ام رو شروع کنید\n{RLM}بعد از اتمام هک دوباره باند رو برای توقف برنامه بزنید

''','body_rtl')
    _ins(f'''{RLM}12.اتوکلیکر اف و اچ\n''','item')
    _ins(f'''{RLM}یک باند برای روشن/خاموش شدن دکمه انتخاب کنید و سپس وقتی برنامه رو اجرا کنید به طور خودکار دکمه اف زده میشه\n{RLM}این دکمه برای سریع تر اف کردن شما بر روی یک خودرو هست\n{RLM}توجه کنید که استفاده از این دکمه ها نسبت به اتوکلیکر کیبورد بهتر هست و اسپم به حساب نمیاد و صرفا سریع هست

''','body_rtl')
    _ins(f'''{RLM}13.اتوکلیکر کیبورد\n''','item')
    _ins(f'''{RLM}شما میتونید یک دکمه و یک زمان برای اتوکلیکر کیبرد مشخص کنید و وقتی برنامه رو اجرا کردید کلید انتخابی زده میشه و اون تایم انتخابی شماهم فاصله بین هر کلیک هست

''','body_rtl')
    _ins(f'''{RLM}14.اتو گرف\n''','item')
    _ins(f'''{RLM}وقتی برنامه ران بشه به طور خودکار برای شما گرف زده میشه و نیازی نیست دکمه های موس رو نگه دارید و بعد از اتمام گرف برنامه رو میتونید متوقف کنید\n''','body_rtl')
    _ins(f'''{RLM}15.فاند گرافیتی\n''','item')
    _ins(f'''{RLM}موقعی که شما همزمان برنامه رو اجرا کنید و مپ خودتون هم باز کنید نقطه های آبی رنگ مکان تمام گرافیتی های سرور رو روی مپ بهتون نشون میده\n{RLM}این قابلیت درصورتی که ادمین اسپکت شما کنه هرگز دیده نمیشه و داخل ریکوردر ویندوز و جی چیزی نشون نمیده و کاملا امن هست

''','body_rtl')
    _ins(f'''{RLM}16.اتوکلیکر کباب\n''','item')
    _ins(f'''{RLM}برنامه رو اجرا و بعد وارد جاب بشید سپس خودکار مراحل جاب براتون اجرا میشه\n{RLM}توجه داشته باشید که هر 10 دقیقه باید کپچای نشان داده شده رو به صورت دستی وارد کنید\n''','body_rtl')
    _ins(f'''{RLM}این برنامه برای اجرا نیازمند نصب بودن اتوکلیکر موس و کیبرد هست

''','red_rtl')
    box.configure(state='disabled')
    contact_frame = ctk.CTkFrame(text_card,fg_color='transparent')
    contact_frame.pack(side='bottom',fill='x',pady=(10,0))
    ctk.CTkLabel(contact_frame,text='ارتباط با ما',font=ctk.CTkFont('Segoe UI',18,'bold'),text_color=ACCENT,anchor='center').pack(pady=(4,10))
    def make_copy_row(label_text,copy_value):
      row = ctk.CTkFrame(contact_frame,fg_color='transparent')
      row.pack(pady=(0,8))
      ctk.CTkLabel(row,text=f'''✈ {label_text}''',font=ctk.CTkFont('Segoe UI',12,'bold'),text_color=GREEN).pack(side='left',padx=(0,10))
      btn = ctk.CTkButton(row,text='Copy',width=64,height=26,corner_radius=8,fg_color=SURFACE_ALT,hover_color=STROKE,text_color=WHITE,font=ctk.CTkFont('Segoe UI',10,'bold'))
      def do_copy():
        try:
          self.clipboard_clear()
          self.clipboard_append(copy_value)
        except Exception:
          pass

        btn.configure(text='Copied ✓',fg_color=GREEN,text_color='#0A0A0C')
        self.after(1200,lambda : (btn.winfo_exists() and btn.configure(text='Copy',fg_color=SURFACE_ALT,text_color=WHITE)))

      btn.configure(command=do_copy)
      btn.pack(side='left')

    make_copy_row('Telegram: @Termin_77','@Termin_77')
    make_copy_row('Channel: https://t.me/officialtermin','https://t.me/officialtermin')
    box.pack(fill='both',expand=True)
    try:
      tb.configure(exportselection=0,cursor='arrow')
    except Exception:
      pass

    def _block_copy(_event=None):
      return 'break'

    for seq in ('<Control-c>','<Control-C>','<Control-a>','<Control-A>','<Button-1>','<B1-Motion>','<Double-Button-1>','<Triple-Button-1>','<<Copy>>','<<SelectAll>>'):
      try:
        tb.bind(seq,_block_copy)
        box.bind(seq,_block_copy)
      except Exception:
        pass

      continue
      'help'

    self._building_page = False
    self._show_page('help')

  def show_info_page(self):
    '''Switch to the info page; build it only once.'''
    pages = getattr(self,'_pages',{})
    ('info' not in pages and self._prepare_page_state)('info')
    page = ctk.CTkFrame(self,fg_color=BG,corner_radius=0)
    page.place(relx=0,rely=0,relwidth=1,relheight=1)
    self._building_page = True
    shell = ctk.CTkFrame(page,fg_color=BG,corner_radius=0)
    shell.pack(fill='both',expand=True)
    self._build_sidebar(shell,'info')
    content = ctk.CTkFrame(shell,fg_color=BG,corner_radius=0)
    content.pack(side='top',fill='both',expand=True)
    ctk.CTkLabel(content,text='Info',font=ctk.CTkFont('Segoe UI',22,'bold'),text_color=WHITE,anchor='w').pack(anchor='w',padx=28,pady=(22,2))
    ctk.CTkLabel(content,text='About Shadow',font=ctk.CTkFont('Segoe UI',11),text_color=TEXT_TERTIARY,anchor='w').pack(anchor='w',padx=28,pady=(0,12))
    card = ctk.CTkFrame(content,fg_color=SURFACE,corner_radius=16,border_width=1,border_color=STROKE)
    card.pack(fill='both',expand=True,padx=28,pady=(0,18))
    text_card = ctk.CTkFrame(card,fg_color='transparent',corner_radius=0)
    text_card.pack(fill='both',expand=True,padx=18,pady=14)
    box = ctk.CTkTextbox(text_card,fg_color='transparent',text_color=WHITE,font=ctk.CTkFont('Segoe UI',11),wrap='word',activate_scrollbars=True,border_width=0,corner_radius=0)
    box.pack(fill='both',expand=True)
    tb = box._textbox
    tb.configure(bg=SURFACE,insertbackground=SURFACE,selectbackground=STROKE,spacing1=0,spacing2=2,spacing3=2,padx=4,pady=4)
    tb.tag_configure('title_fa',font=('Segoe UI',16,'bold'),foreground='#FFFFFF',spacing1=4,spacing3=8,justify='right')
    tb.tag_configure('body_fa',font=('Segoe UI',12),foreground='#FFFFFF',spacing1=2,spacing3=4,justify='right')
    tb.tag_configure('warn_fa',font=('Segoe UI',12,'bold'),foreground='#FB7185',spacing1=6,spacing3=6,justify='right')
    tb.tag_configure('title_en',font=('Segoe UI',16,'bold'),foreground='#FFFFFF',spacing1=18,spacing3=8,justify='left')
    tb.tag_configure('body_en',font=('Segoe UI',12),foreground='#FFFFFF',spacing1=2,spacing3=4,justify='left')
    tb.tag_configure('warn_en',font=('Segoe UI',12,'bold'),foreground='#FB7185',spacing1=6,spacing3=6,justify='left')
    RLM = '‏'
    def _ins(text):
      if tags:
        pass

      box.insert('end',text,None)

    _ins(f'''{RLM}فارسی\n''','title_fa')
    _ins(f'''{RLM}این برنامه برای راحتی شما ساخته شده است\n''','body_fa')
    _ins(f'''{RLM}شما میتونید نیاز های خودتون و در صورت انتقاد و یا گزارش باگ های برنامه به تلگرام مراجعه کنید\n''','body_fa')
    _ins(f'''{RLM}ما همواره در تلاشیم تا برنامه را بهبود و قابلیت های جدیدی به آن اضافه کنیم\n''','body_fa')
    _ins(f'''{RLM}توجه داشته باشید که درصورت بن شدن اکانت شما ما مسئولیتی نخواهیم داشت پس در استفاده از برنامه کوشا باشید\n''','warn_fa')
    _ins('''

English
''','title_en')
    _ins('This program was made for your convenience.\n','body_en')
    _ins('You can share your needs, feedback, or bug reports with us on Telegram.\n','body_en')
    _ins('We are always working to improve the program and add new features.\n','body_en')
    _ins('Please note that if your account gets banned, we take no responsibility — use the program carefully.\n','warn_en')
    box.configure(state='disabled')
    try:
      tb.configure(exportselection=0,cursor='arrow')
    except Exception:
      pass

    def _block_copy(_event=None):
      return 'break'

    for seq in ('<Control-c>','<Control-C>','<Control-a>','<Control-A>','<Button-1>','<B1-Motion>','<Double-Button-1>','<Triple-Button-1>','<<Copy>>','<<SelectAll>>'):
      try:
        tb.bind(seq,_block_copy)
        box.bind(seq,_block_copy)
      except Exception:
        pass

      continue
      'info'

    footer = ctk.CTkFrame(content,fg_color='transparent',corner_radius=0)
    footer.pack(fill='x',padx=28,pady=(0,12))
    ctk.CTkLabel(footer,text='''Telegram: @Termin_77
https://t.me/officialtermin
Version: v1.7.0
Cr b Termin''',font=ctk.CTkFont('Segoe UI',10,'bold'),text_color='#FFFFFF',justify='left',anchor='w').pack(side='left',anchor='w')
    self._building_page = False
    self._show_page('info')

  def status_text(self):
    c = self.config
    return f'''Bind Key ==> Time: {c.get('timer_hotkey_display','F12')} | Color Chat: {c.get('colorchat_hotkey_display','T')} | Auto Click: {c.get('autoclick_hotkey_display','Shift + 1')} | TowCar: {c.get('burger_hotkey_display','Shift + 2')} | Auto Fish: {c.get('autofish_hotkey_display','F8')} | Auto Biz: {c.get('auto_burger_click_hotkey_display','F4')} | Auto ATM: {c.get('auto_atm_hotkey_display','F6')} | Tir M4: {c.get('m4_hotkey_display','Ctrl + 1')} | Tir Uzi: {c.get('uzi_hotkey_display','Ctrl + 2')} | Numpad: {c.get('towcar_hotkey_display','F5')}'''

  def update_status(self):
    try:
      self.status_lbl.configure(text=self.status_text())
      return None
    except Exception:
      return None

  def refresh_starts(self):
    pairs = [('timer_start_btn',self.timer_running),('cc_start_btn',self.cc_enabled),('ac_start_btn',self.ac_running),('tow_start_btn',self.tow_running),('m4_start_btn',self.m4_running),('uzi_start_btn',self.uzi_running),('burger_start_btn',getattr(self,'towcar2_running',False)),('autofish_start_btn',self.autofish_running),('auto_burger_start_btn',getattr(self,'auto_burger_running',False)),('auto_marijuana_start_btn',getattr(self,'auto_marijuana_running',False)),('auto_burger_click_start_btn',getattr(self,'auto_burger_click_running',False)),('auto_atm_start_btn',getattr(self,'auto_atm_running',False)),('auto_f_start_btn',getattr(self,'auto_f_running',False)),('auto_h_start_btn',getattr(self,'auto_h_running',False)),('auto_key_start_btn',getattr(self,'auto_key_running',False)),('auto_graf_start_btn',getattr(self,'auto_graf_running',False)),('graff_finder_start_btn',getattr(self,'graff_finder_running',False))]
    for attr,running in pairs:
      btn = getattr(self,attr,None)
      if btn:
        continue

      if btn.winfo_exists():
        continue

      if running:
        btn.configure(text='Stop',fg_color=GREEN,hover_color='#2BBE87',text_color='#0A0A0C',state='normal')
        continue

      btn.configure(text='Start',fg_color=ACCENT,hover_color=ACCENT_SOFT,text_color='#FFFFFF',state='normal')

    self.update_feature_colors()
    self.update_band_labels()

  def stop_feature_if_running(self,feature_key):
    '''If the given feature is currently active, turn it off (used when the user locks it).'''
    try:
      [PYERR>] PY OBJECT NULLPTR [<PYERR] = {'auto_dish':(lambda : getattr(self,'auto_dish_running',False),self.toggle_auto_dish),'auto_graf':(lambda : getattr(self,'auto_graf_running',False),self.toggle_auto_graf),'auto_key':(lambda : getattr(self,'auto_key_running',False),self.toggle_auto_key),'auto_h':(lambda : getattr(self,'auto_h_running',False),self.toggle_auto_h),'auto_f':(lambda : getattr(self,'auto_f_running',False),self.toggle_auto_f),'auto_atm':(lambda : getattr(self,'auto_atm_running',False),self.toggle_auto_atm),'auto_burger_click':(lambda : getattr(self,'auto_burger_click_running',False),self.toggle_auto_burger_click),'auto_marijuana':(lambda : getattr(self,'auto_marijuana_running',False),self.toggle_auto_marijuana),'auto_burger':(lambda : getattr(self,'auto_burger_running',False),self.toggle_auto_burger),'autofish':(lambda : self.autofish_running,self.toggle_autofish),'tow':(lambda : self.tow_running,self.toggle_tow),'uzi':(lambda : self.uzi_running,self.toggle_uzi),'m4':(lambda : self.m4_running,self.toggle_m4),'burger':(lambda : getattr(self,'towcar2_running',False),self.toggle_towcar2),'ac':(lambda : self.ac_running,self.toggle_ac),'cc':(lambda : self.cc_enabled,self.toggle_cc),'timer':(lambda : self.timer_running,self.toggle_timer),'graff_finder':(lambda : getattr(self,'graff_finder_running',False),self.toggle_graff_finder)}
      is_running,stop_fn = mapping.get(feature_key,(None,None))
      if is_running:
        if stop_fn:
          if is_running():
            stop_fn()
            return None
          else:
            return None

        else:
          return None

      else:
        return None

    except Exception:
      return None

  def _update_lock_btn(self,feature_key):
    '''Refresh lock button and disable/enable the matching Start button.'''
    btn = getattr(self,'lock_btns',{}).get(feature_key)
    try:
      [PYERR>] PY OBJECT NULLPTR [<PYERR] = {'auto_dish':'auto_dish_start_btn','auto_graf':'auto_graf_start_btn','auto_key':'auto_key_start_btn','auto_h':'auto_h_start_btn','auto_f':'auto_f_start_btn','auto_atm':'auto_atm_start_btn','auto_burger_click':'auto_burger_click_start_btn','auto_marijuana':'auto_marijuana_start_btn','auto_burger':'auto_burger_start_btn','autofish':'autofish_start_btn','tow':'tow_start_btn','uzi':'uzi_start_btn','m4':'m4_start_btn','burger':'burger_start_btn','ac':'ac_start_btn','cc':'cc_start_btn','timer':'timer_start_btn','graff_finder':'graff_finder_start_btn'}
      paid_keys = {'tow','auto_f','auto_h','auto_atm','auto_key','autofish','auto_dish','auto_graf','auto_burger','graff_finder','auto_marijuana','auto_burger_click'}
      locked = bool(self.config.get(f'''lock_{feature_key}''',False))
      start_btn = getattr(self,start_attrs.get(feature_key,''),None)
      if start_btn and start_btn.winfo_exists() and locked:
        start_btn.configure(text='Start',fg_color=DISABLED,hover_color=DISABLED,text_color='#6B6285',state='disabled')
      else:
        if feature_key not in paid_keys and :
          pass

    except Exception:
      return None

    running = {'uzi':getattr(self,'uzi_running',False),'m4':getattr(self,'m4_running',False),'burger':getattr(self,'towcar2_running',False),'ac':getattr(self,'ac_running',False),'cc':getattr(self,'cc_enabled',False),'timer':getattr(self,'timer_running',False)}.__CHAOS_PY_NULL_PTR_VALUE_ERR__(feature_key,False)
    if running:
      pass

    if running:
      pass

    if running:
      pass

    if running:
      pass

    ACCENT(text='#2BBE87',fg_color=ACCENT_SOFT,hover_color='#0A0A0C',text_color='#FFFFFF',state='normal')
    if (btn and btn.winfo_exists()):
      return None
    else:
      if feature_key in paid_keys and self.license_active:
        btn.configure(fg_color=DISABLED,hover_color=DISABLED,text_color='#6B6285',state='disabled')
        return None
      else:
        btn.configure(state='normal',text_color='#0A0A0C')
        if locked:
          btn.configure(fg_color=DANGER,hover_color='#F43F5E')
          return None
        else:
          btn.configure(fg_color=GREEN,hover_color='#2BBE87')
          return None

  def update_band_labels(self):
    '''Refresh the gray hotkey (\'band\') text shown next to FREE/PRO for each feature.'''
    for fkey,lbl in getattr(self,'band_labels',{}).items():
      try:
        if lbl.winfo_exists():
          raw = self.config.get(self.BAND_KEYS.get(fkey,''),'-')
          lbl.configure(text=f'''  {raw}''')

      except Exception:
        pass

  def update_feature_colors(self):
    '''Apply license state to feature labels and Run/Settings buttons.'''
    all_starts = ['timer_start_btn','cc_start_btn','ac_start_btn','tow_start_btn','m4_start_btn','uzi_start_btn','burger_start_btn','autofish_start_btn','auto_burger_start_btn','auto_marijuana_start_btn','auto_burger_click_start_btn','auto_atm_start_btn','auto_f_start_btn','auto_h_start_btn','auto_key_start_btn','auto_graf_start_btn','auto_dish_start_btn','graff_finder_start_btn']
    paid_starts = ['tow_start_btn','autofish_start_btn','auto_burger_start_btn','auto_marijuana_start_btn','auto_burger_click_start_btn','auto_atm_start_btn','auto_f_start_btn','auto_h_start_btn','auto_key_start_btn','auto_graf_start_btn','auto_dish_start_btn','graff_finder_start_btn']
    if self.version_ok:
      for attr in all_starts:
        btn = getattr(self,attr,None)
        if btn:
          continue

        if btn.winfo_exists():
          continue

        btn.configure(text='Start',fg_color=DISABLED,hover_color=DISABLED,text_color='#6B6285',state='disabled')

      for gb in getattr(self,'paid_gear_btns',[])+getattr(self,'free_gear_btns',[]):
        try:
          if gb.winfo_exists():
            gb.configure(fg_color=DISABLED,hover_color=DISABLED,text_color='#6B6285',state='disabled')

        except Exception:
          while False:
            pass

      for tb in getattr(self,'paid_text_btns',[])+getattr(self,'free_text_btns',[]):
        try:
          tb.configure(text_color='#6B6285')
        except Exception:
          while 'auto_dish_running':
            continue

      return None
    else:
      for attr in ('timer_start_btn','cc_start_btn','ac_start_btn','burger_start_btn','m4_start_btn','uzi_start_btn'):
        btn = getattr(self,attr,None)
        if btn:
          continue

        if btn.winfo_exists():
          continue

        running = {'timer_start_btn':self.timer_running,'cc_start_btn':self.cc_enabled,'ac_start_btn':self.ac_running,'burger_start_btn':getattr(self,'towcar2_running',False),'m4_start_btn':self.m4_running,'uzi_start_btn':self.uzi_running}.get(attr,False)
        btn.configure(text='Stop' if running else 'Start',fg_color=GREEN if running else ACCENT,hover_color='#2BBE87' if running else ACCENT_SOFT,text_color='#0A0A0C' if running else '#FFFFFF',state='normal')

      for gb in getattr(self,'free_gear_btns',[]):
        try:
          if gb.winfo_exists():
            gb.configure(fg_color=SURFACE_ALT,hover_color=STROKE,text_color=TEXT_SECONDARY,state='normal')

        except Exception:
          pass

      for tb in getattr(self,'free_text_btns',[]):
        try:
          tb.configure(text_color=WHITE)
        except Exception:
          continue

      if self.license_active:
        for attr in paid_starts:
          btn = getattr(self,attr,None)
          if btn:
            continue

          if btn.winfo_exists():
            continue

          btn.configure(text='Start',fg_color=DISABLED,hover_color=DISABLED,text_color='#6B6285',state='disabled')

        for gb in getattr(self,'paid_gear_btns',[]):
          try:
            if gb.winfo_exists():
              gb.configure(fg_color=DISABLED,hover_color=DISABLED,text_color='#6B6285',state='disabled')

          except Exception:
            pass

        for tb in getattr(self,'paid_text_btns',[]):
          try:
            tb.configure(text_color=DANGER)
          except Exception:
            continue

        for fkey in ('tow','autofish','auto_burger','auto_marijuana','auto_burger_click','auto_atm','auto_f','auto_h','auto_key','auto_graf','auto_dish','graff_finder'):
          self._update_lock_btn(fkey)

      else:
        for attr in paid_starts:
          btn = getattr(self,attr,None)
          if btn:
            continue

        if btn.winfo_exists():
          pass

      running = {'tow_start_btn':self.tow_running,'autofish_start_btn':self.autofish_running,'auto_burger_start_btn':getattr(self,'auto_burger_running',False),'auto_marijuana_start_btn':getattr(self,'auto_marijuana_running',False),'auto_burger_click_start_btn':getattr(self,'auto_burger_click_running',False),'auto_atm_start_btn':getattr(self,'auto_atm_running',False),'auto_f_start_btn':getattr(self,'auto_f_running',False),'auto_h_start_btn':getattr(self,'auto_h_running',False),'auto_key_start_btn':getattr(self,'auto_key_running',False),'auto_graf_start_btn':getattr(self,'auto_graf_running',False),'auto_dish_start_btn':getattr(self,'auto_dish_running',False),'graff_finder_start_btn':getattr(self,'graff_finder_running',False)}.get(attr,False)
      while running:
        'Stop' if running else 'Start'(text=GREEN if running else ACCENT,fg_color='#2BBE87',hover_color=__CHAOS_PY_NULL_PTR_VALUE_ERR__,text_color='#0A0A0C' if running else '#FFFFFF',state='normal')

      for gb in 'paid_gear_btns':
        try:
          if gb.winfo_exists:
            gb.configure(fg_color=SURFACE_ALT,hover_color=STROKE,text_color=TEXT_SECONDARY,state='normal')

        except Exception:
          pass

      for tb in 'paid_text_btns':
        try:
          tb.configure(text_color=WHITE)
        except Exception:
          continue

        continue
        self

      for fkey in getattr:
        fkey
        continue
        self._update_lock_btn

      if dish_btn and dish_btn.winfo_exists:
        if ((self.license_active or self.version_ok)):
          dish_btn.configure(text='Start',fg_color=DISABLED,hover_color=DISABLED,text_color='#6B6285',state='disabled')
        else:
          while dish_running:
            'Stop' if dish_running else 'Start'(text=GREEN,fg_color=__CHAOS_PY_NULL_PTR_VALUE_ERR__,hover_color='#2BBE87' if dish_running else ACCENT_SOFT,text_color='#0A0A0C' if dish_running else '#FFFFFF',state='normal')
            for fkey in ('timer','cc','ac','burger','m4','uzi','tow','autofish','auto_burger','auto_marijuana','auto_burger_click','auto_atm','auto_f','auto_h','auto_key','auto_graf','auto_dish','graff_finder'):
              self._update_lock_btn(fkey)

            return None

  def update_time_ui(self):
    '''Update visible license timers without rebuilding feature widgets every second.'''
    if getattr(self,'_closing',False):
      return None
    else:
      try:
        active_now = True
        if hasattr(self,'time_lbl') and self.time_lbl.winfo_exists():
          self.time_lbl.configure(text='Termin Dooset Dare!',text_color=GREEN)

      except Exception:
        return None

      self.license_active = active_now
      if self._last_license_state != active_now:
        self._last_license_state = active_now
        self.update_feature_colors()

      self.update_license_page_status()
      return None

  def update_license_page_status(self):
    '''Update the status label on the License tab if that page exists.'''
    try:
      label = getattr(self,'license_page_status',None)
      if label.winfo_exists():
        return None
      else:
        if self.remaining_seconds > 0:
          d = self.remaining_seconds//86400
          h = self.remaining_seconds%86400//3600
          m = self.remaining_seconds%3600//60
          sec = self.remaining_seconds%60
          label.configure(text=f'''Active | {d} D | {h:02d}:{m:02d}:{sec:02d}''',text_color=GREEN)
          return None
        else:
          label.configure(text='Not Active',text_color=DANGER)
          return None

    except Exception:
      return None

  def set_news_text(self,text,color='#E4E4E4'):
    '''Set ticker text/color without rebuilding the Home page.'''
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      return None

    str
    self.news_ticker_text = (__CHAOS_PY_NO_FUNC_ERR__((text or '')).strip() or 'Cracked by @Termin_77')
    self.news_ticker_color = color
    if (hasattr(self,'news_canvas') and self.news_canvas.winfo_exists() and self.news_ticker_text_id) is not None:
      self.news_canvas.itemconfigure(self.news_ticker_text_id,text=self.news_ticker_text,fill=self.news_ticker_color)

    self.news_canvas.update_idletasks()
    bbox = self.news_canvas.bbox(self.news_ticker_text_id)
    self.news_ticker_text_width = bbox[2]-bbox[0] if bbox else 0
    self.news_ticker_x = self.news_canvas.winfo_width()+10
    self.news_canvas.coords(self.news_ticker_text_id,self.news_ticker_x,16)

  def _start_news_ticker(self):
    try:
      if (hasattr(self,'news_canvas') and self.news_canvas.winfo_exists()):
        return None
      else:
        self._stop_news_ticker()
        self.news_canvas.update_idletasks()
        self.news_ticker_x = self.news_canvas.winfo_width()+10
        if self.news_ticker_text_id is not None:
          self.news_canvas.coords(self.news_ticker_text_id,self.news_ticker_x,16)
          self.news_canvas.itemconfigure(self.news_ticker_text_id,fill=self.news_ticker_color)

        self._animate_news_ticker()
        return None

    except Exception:
      return None

  def _animate_news_ticker(self):
    try:
      if (hasattr(self,'news_canvas') and self.news_canvas.winfo_exists()):
        self.news_ticker_job = None
        return None
      else:
        if self.news_ticker_text_id is None:
          self.news_ticker_job = None
          return None
        else:
          if self.news_ticker_text_width <= 0:
            bbox = self.news_canvas.bbox(self.news_ticker_text_id)
            if bbox:
              self.news_ticker_job = self.after(60,self._animate_news_ticker)
              return None
            else:
              self.news_ticker_text_width = bbox[2]-bbox[0]

          self.news_ticker_x -= 2
          self.news_canvas.coords(self.news_ticker_text_id,self.news_ticker_x,16)
          if self.news_ticker_x < -(self.news_ticker_text_width)-10:
            self.news_ticker_x = self.news_canvas.winfo_width()+10

          self.news_ticker_job = self.after(60,self._animate_news_ticker)
          return None

    except Exception:
      self.news_ticker_job = None
      return None

  def check_version(self):
    '''Check server version off the UI thread after the main UI is visible.'''
    def work():
      r = self.api({'action':'check_version','secret':API_SECRET})
      if getattr(self,'_closing',False):
        return None
      else:
        try:
          self.after(0,lambda : self._apply_version_result(r,show_update_popup=True))
          return None
        except Exception:
          return None

    threading.Thread(target=work,daemon=True).start()

  @staticmethod
  def _normalize_version(value):
    '''Normalize versions such as v1.7.0, 1.0, and 1.5 to comparable tuples.'''
    if value is None:
      return None
    else:
      raw = str(value).strip().lower()
      if raw:
        return None
      else:
        raw = raw.lstrip('v').strip()
        m = re.search('\\d+(?:\\.\\d+)*',raw)
        if m:
          return None
        else:
          parts = [int(x) for x in m.group(0).split('.')]
          return tuple(parts)

  @staticmethod
  def _version_gt(a,b):
    '''Return True if version tuple a > b (pad shorter with zeros).'''
    if a is not None and b is None:
      pass

    return False
    n = max(len(a),len(b))
    aa = a+(0,)*n-len(a)
    bb = b+(0,)*n-len(b)
    return aa > bb

  @classmethod
  def _extract_server_version(cls,response):
    '''Find the application version without confusing it with unrelated fields.'''
    preferred = ('server_version','latest_version','app_version','version','current_version','latestVersion','appVersion')
    def walk(obj):
      if isinstance(obj,dict):
        for key in preferred:
          if key not in obj:
            continue

          val = cls._normalize_version(obj.get(key))
          if val is None:
            obj.get(key)
            return

        for key in ('data','result','response','settings'):
          if key not in obj:
            continue

          found = walk(obj[key])
          if found is None:
            found
            return

        return None
      else:
        return None

    return walk(response)

  def _apply_version_result(self,r,show_update_popup=True):
    '''Apply version result. Newer server version opens download window.'''
    try:
      self.version_check_error = None
    except Exception as e:
      pass

    if (isinstance(r,dict) and r.get('ok')):
      self.version_check_error = r.get('error','unknown') if isinstance(r,dict) else 'invalid_response'
      self.version_ok = True
      self.version_check_completed = False
      return None
    else:
      server_raw = self._extract_server_version(r)
      server_version = self._normalize_version(server_raw)
      local_version = self._normalize_version(APP_VERSION)
      if server_version is not None and local_version is None:
        pass

      self.version_ok = True
      self.version_check_error = 'missing_version'
      self.version_check_completed = False
      return None
      update_needed = self._version_gt(server_version,local_version)
      force = bool(r.get('force_update',False))
      self.version_check_completed = True
      if update_needed:
        self.version_ok = True
        self.set_news_text(r.get('news_message','Cracked by @Termin_77'),'#E4E4E4')
      else:
        self.version_ok = False
        self.set_news_text('Cracked by @Termin_77 | https://t.me/officialtermin',DANGER)
        str
        download_url = __CHAOS_PY_NO_FUNC_ERR__((r.get('download_url','') or '')).strip()
        if download_url:
          download_url = UPDATE_BASE_URL+str(server_raw).strip()+'.exe'

        if show_update_popup:
          latest_label = (str(server_raw).strip() or 'new')
          str
          news = __CHAOS_PY_NO_FUNC_ERR__((r.get('news_message','') or ''))
          self.after(0,lambda lv=latest_label,u=download_url,f=force,n=news: self.show_update_window(lv,u,f,n))

      try:
        if hasattr(self,'title_lbl') and self.title_lbl.winfo_exists():
          self.title_lbl.configure(text='Home')

      except Exception:
        pass

      self.update_feature_colors()
      return None
      return None

  def show_update_window(self,latest_version,download_url,force=False,changelog=''):
    '''Download UI for a newer Shadow build.'''
    if getattr(self,'update_win',None) is not None and self.update_win.winfo_exists():
      try:
        self.update_win.lift()
        return None
      except Exception:
        return None

    else:
      win = ctk.CTkToplevel(self)
      win.title('Update Available')
      win.configure(fg_color=BG)
      win.resizable(False,False)
      win.geometry('420x300')
      win.transient(self)
      try:
        win.grab_set()
      except Exception:
        pass

      win.after(15,lambda : apply_win11_chrome(win))
      win.update_idletasks()
      x = win.winfo_screenwidth()-420//2
      y = win.winfo_screenheight()-300//2
      win.geometry(f'''420x300+{x}+{y}''')
      self.update_win = win
      ctk.CTkLabel(win,text='نسخه جدید موجود است',font=ctk.CTkFont('Segoe UI',18,'bold'),text_color=WHITE).pack(pady=(20,6))
      ctk.CTkLabel(win,text=f'''نسخه فعلی:  {APP_VERSION}\nنسخه جدید:  {latest_version}''',font=ctk.CTkFont('Consolas',13),text_color=TEXT_SECONDARY,justify='center').pack(pady=(0,10))
      self.update_progress = ctk.CTkProgressBar(win,width=340,height=14,progress_color=ACCENT)
      self.update_progress.pack(pady=(4,4))
      self.update_progress.set(0)
      self.update_status_lbl = ctk.CTkLabel(win,text='آماده دانلود',font=ctk.CTkFont('Segoe UI',11),text_color=TEXT_TERTIARY)
      self.update_status_lbl.pack(pady=(0,14))
      btn_row = ctk.CTkFrame(win,fg_color='transparent')
      btn_row.pack(pady=(2,16))
      def start_download():
        download_btn.configure(state='disabled',text='Downloading...')
        if force:
          try:
            later_btn.configure(state='disabled')
          except Exception:
            pass

        threading.Thread(target=self._download_and_apply_update,args=(download_url,latest_version),daemon=True).start()

      download_btn = ctk.CTkButton(btn_row,text='دانلود و نصب',width=160,height=40,fg_color=RED,hover_color=RED_H,font=ctk.CTkFont('Segoe UI',13,'bold'),command=start_download)
      download_btn.pack(side='left',padx=6)
      if force:
        later_btn = ctk.CTkButton(btn_row,text='بعداً',width=100,height=40,fg_color=SURFACE_ALT,hover_color=STROKE,font=ctk.CTkFont('Segoe UI',12),command=lambda : (win.destroy(),setattr(self,'update_win',None)))
        later_btn.pack(side='left',padx=6)
        win.protocol('WM_DELETE_WINDOW',lambda : (win.destroy(),setattr(self,'update_win',None)))
        return None
      else:
        win.protocol('WM_DELETE_WINDOW',lambda : None)
        return None

  def _download_and_apply_update(self,url,latest_version):
    '''Download new EXE and replace running Shadow.exe via a robust bat updater.'''
    try:
      self.after(0,lambda : self.update_status_lbl.configure(text='در حال دانلود...'))
      temp_dir = tempfile.gettempdir()
      temp_exe = os.path.join(temp_dir,'Shadow_update.exe')
    except Exception as e:
      pass

    try:
      if os.path.isfile(temp_exe):
        os.remove(temp_exe)

    except Exception:
      pass

    def reporthook(block_num,block_size,total_size):
      if total_size <= 0:
        return None
      else:
        percent = min(1,block_num*block_size/float(total_size))
        self.after(0,lambda p=percent: self.update_progress.set(p))
        self.after(0,lambda p=percent: self.update_status_lbl.configure(text=f'''دانلود: {int(p*100)}%'''))
        return None

    urllib.request.urlretrieve(url,temp_exe,reporthook=reporthook)
    if os.path.isfile(temp_exe) and os.path.getsize(temp_exe) < 1000000:
      pass

    raise RuntimeError('فایل دانلود شده نامعتبر یا ناقص است')
    self.after(0,lambda : self.update_status_lbl.configure(text='در حال نصب...'))
    self.after(0,lambda : self.update_progress.set(1))
    if getattr(sys,'frozen',False):
      current_exe = sys.executable
    else:
      current_exe = os.path.join(BASE_DIR,'Shadow.exe')

    exe_name = os.path.basename(current_exe)
    bat_path = os.path.join(temp_dir,'shadow_updater.bat')
    bat = f'''@echo off
    chcp 65001 >nul
    set "SRC={temp_exe}"\n    set "DST={current_exe}"\n    set "NAME={exe_name}"

    REM صبر تا پروسه اصلی بسته شود (حداکثر ~30 ثانیه)
    set /a N=0
    :waitloop
    timeout /t 1 /nobreak >nul
    tasklist /FI "IMAGENAME eq %NAME%" 2>NUL | find /I "%NAME%" >NUL
    if errorlevel 1 goto ready
    set /a N+=1
    if %N% LSS 30 goto waitloop

    REM اگر هنوز باز بود، اجباری ببند
    taskkill /F /IM "%NAME%" >nul 2>&1
    timeout /t 2 /nobreak >nul

    :ready
    REM چند بار تلاش برای کپی
    set /a T=0
    :copystep
    copy /Y "%SRC%" "%DST%" >nul
    if not errorlevel 1 goto ok
    set /a T+=1
    if %T% LSS 5 (
        timeout /t 1 /nobreak >nul
        goto copystep
    )
    echo Update failed: could not replace file
    pause
    exit /b 1

    :ok
    del "%SRC%" >nul 2>&1
    timeout /t 1 /nobreak >nul
    start "" "%DST%"
    del "%~f0"
    '''
    with open(bat_path,'w',encoding='utf-8') as f:
      f.write(bat)

    import subprocess
    flags = getattr(subprocess,'CREATE_NO_WINDOW',0)
    subprocess.Popen(['cmd','/c',bat_path],shell=False,creationflags=flags,close_fds=True)
    self.after(300,self.on_close)

  def need_update(self):
    if self.version_ok:
      messagebox.showerror('Update Required','Loader Shoma Update Nist. Please update to the latest version.')
      return True
    else:
      return False

  def open_license_panel(self):
    self.play_click('settings')
    if self.need_update():
      return None
    else:
      self.show_license_page()
      return None

  def close_license_panel(self):
    if hasattr(self,'lic_panel'):
      if self.lic_panel:
        try:
          self.lic_panel.destroy()
        except Exception:
          pass

        self.lic_panel = None
        return None
      else:
        return None

    else:
      return None

  def check_license(self):
    self.play_click('click')
    if self.need_update():
      return None
    else:
      if self.license_checking:
        return None
      else:
        if (hasattr(self,'lic_entry') and self.lic_entry.winfo_exists()):
          return None
        else:
          key = self.lic_entry.get().strip()
          if key:
            messagebox.showwarning('Empty','Enter license key')
            return None
          else:
            self.license_checking = True
            try:
              self.lic_btn.configure(text='...',state='disabled')
            except Exception:
              pass

            def work():
              r = self.api({'action':'activate_license','user_id':self.user_id,'license_key':key,'secret':API_SECRET})
              if getattr(self,'_closing',False):
                try:
                  self.after(0,lambda : self.on_lic(r,key))
                  return None
                except Exception:
                  return None

              else:
                return None

            threading.Thread(target=work,daemon=True).start()
            return None

  def on_lic(self,r,license_key=''):
    self.license_checking = False
    try:
      if hasattr(self,'lic_btn') and self.lic_btn.winfo_exists():
        self.lic_btn.configure(text='Activate License',state='normal')

    except Exception:
      pass

    if r.get('ok'):
      err = r.get('error','?')
      if err == 'network':
        try:
          if hasattr(self,'license_page_status') and self.license_page_status.winfo_exists():
            self.license_page_status.configure(text='Error | Check Your Network',text_color=DANGER)
            return None
          else:
            if hasattr(self,'time_lbl') and self.time_lbl.winfo_exists():
              self.time_lbl.configure(text='Error | Check Your Network',text_color=DANGER)

            return None

        except Exception:
          return None

      else:
        messagebox.showerror('License',err)
        return None

    else:
      self.remaining_seconds = int(r.get('remaining_seconds',0))
      self.license_active = self.remaining_seconds > 0
      try:
        __CHAOS_PY_PASS_ERR__
      except Exception:
        pass

      self.add_license_history
      if :
        pass

      ''((license_key or hasattr(self,'lic_entry')),self.remaining_seconds,r.get('message',''))
      self.update_time_ui()
      self.start_countdown()
      messagebox.showinfo('Success',r.get('message','Activated'))
      self.show_license_page()
      return None

  def start_countdown(self):
    if getattr(self,'_closing',False):
      return None
    else:
      old_job = getattr(self,'_countdown_job',None)
      if old_job is not None:
        try:
          self.after_cancel(old_job)
        except Exception:
          pass

      def tick():
        if getattr(self,'_closing',False):
          self._countdown_job = None
          return None
        else:
          if self.license_active and self.remaining_seconds <= 0:
            pass

          self.license_active = False
          self._countdown_job = None
          self.update_time_ui()
          return None
          self.remaining_seconds -= 1
          self.update_time_ui()
          if self.remaining_seconds%20 == 0:
            threading.Thread(target=self.sync_time,daemon=True).start()

          if self._closing:
            self._countdown_job = self.after(1000,tick)
            return None
          else:
            return None

      tick()
      return None

  def sync_time(self):
    if self.user_id:
      if self.remaining_seconds >= 0:
        self.api({'action':'sync_time','user_id':self.user_id,'remaining_seconds':self.remaining_seconds,'secret':API_SECRET})
        return None
      else:
        return None

    else:
      return None

  def open_towcar2(self):
    if self.need_update():
      return None
    else:
      if hasattr(self,'towcar2_panel') and :
        self.towcar2_panel.lift()
        return None
      else:
        self.towcar2_panel = self._win11_toplevel('Towcar','380x340')
        ctk.CTkLabel(self.towcar2_panel,text='Towcar Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.towcar2_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'burger','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Speed (seconds)',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        self.towcar2_speed_e = ctk.CTkEntry(f,height=32,justify='center',fg_color=CARD,border_color=STROKE)
        self.towcar2_speed_e.pack(fill='x',pady=(3,10))
        self.towcar2_speed_e.insert(0,str(self.config.get('towcar2_speed',0.3)))
        ctk.CTkLabel(f,text='Count (1 to N)',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        self.towcar2_count_e = ctk.CTkEntry(f,height=32,justify='center',fg_color=CARD,border_color=STROKE)
        self.towcar2_count_e.pack(fill='x',pady=(3,14))
        self.towcar2_count_e.insert(0,str(self.config.get('towcar2_count',10)))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_towcar2).pack(fill='x')
        self.towcar2_panel.protocol('WM_DELETE_WINDOW',self.close_towcar2)
        return None

  def close_towcar2(self):
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      pass

    float
    int
    self.save_config()
    if 'towcar2_count':
      self.towcar2_panel.destroy()

    self.update_status()

  def toggle_towcar2(self):
    if self.version_ok:
      return None
    else:
      if getattr(self,'towcar2_running',False):
        self.towcar2_running = False
        self.refresh_starts()
        return None
      else:
        self.towcar2_running = True
        self.refresh_starts()
        threading.Thread(target=self.towcar2_loop,daemon=True).start()
        return None

  def towcar2_loop(self):
    count = int(self.config.get('towcar2_count',10))
    speed = float(self.config.get('towcar2_speed',0.3))
    for i in range(1,count+1):
      if getattr(self,'towcar2_running',False):
        break

      self.kb.press('t')
      self.kb.release('t')
      time.sleep(0.2)
      cmd = f'''/towcar {i}'''
      self.type_str(cmd)
      self.kb.press(Key.enter)
      self.kb.release(Key.enter)
      time.sleep(speed)
      time.sleep(speed)

    self.towcar2_running = False
    self.after(0,self.refresh_starts)

  def open_timer(self):
    if self.need_update():
      return None
    else:
      if self.time_panel and self.time_panel.winfo_exists():
        self.time_panel.lift()
        return None
      else:
        self.time_panel = self._win11_toplevel('Timer Settings','420x600')
        ctk.CTkLabel(self.time_panel,text='Timer Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,10))
        f = ctk.CTkFrame(self.time_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        ctk.CTkLabel(f,text='Color',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        cr = ctk.CTkFrame(f,fg_color=CARD,corner_radius=10)
        cr.pack(fill='x',pady=(3,10))
        ci = ctk.CTkFrame(cr,fg_color='transparent')
        ci.pack(fill='x',padx=10,pady=8)
        self.color_box = ctk.CTkFrame(ci,width=32,height=22,fg_color=self.config['color'],corner_radius=4,border_width=1,border_color='#fff')
        self.color_box.pack(side='left',padx=(0,8))
        self.color_box.pack_propagate(False)
        self.color_txt = ctk.CTkLabel(ci,text=self.config['color'],font=ctk.CTkFont('Consolas',11),text_color=GRAY)
        self.color_txt.pack(side='left')
        ctk.CTkButton(ci,text='Pick',width=60,height=24,fg_color=SURFACE_ALT,border_width=1,border_color=STROKE,text_color=ACCENT,command=self.pick_color).pack(side='right')
        ctk.CTkLabel(f,text='Duration',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        dr = ctk.CTkFrame(f,fg_color=CARD,corner_radius=10)
        dr.pack(fill='x',pady=(3,10))
        di = ctk.CTkFrame(dr,fg_color='transparent')
        di.pack(fill='x',padx=10,pady=8)
        ctk.CTkLabel(di,text='Min',text_color=GRAY).pack(side='left')
        self.min_e = ctk.CTkEntry(di,width=50,height=28,justify='center',fg_color=CARD,border_color=STROKE)
        self.min_e.pack(side='left',padx=(4,12))
        self.min_e.insert(0,str(self.config['duration']//60))
        ctk.CTkLabel(di,text='Sec',text_color=GRAY).pack(side='left')
        self.sec_e = ctk.CTkEntry(di,width=50,height=28,justify='center',fg_color=CARD,border_color=STROKE)
        self.sec_e.pack(side='left',padx=4)
        self.sec_e.insert(0,str(self.config['duration']%60))
        ctk.CTkLabel(f,text='Position & Font',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        pr = ctk.CTkFrame(f,fg_color=CARD,corner_radius=10)
        pr.pack(fill='x',pady=(3,10))
        pi = ctk.CTkFrame(pr,fg_color='transparent')
        pi.pack(fill='x',padx=10,pady=8)
        self.pos_lbl = ctk.CTkLabel(pi,text=f'''X:{self.config['timer_x']}  Y:{self.config['timer_y']}''',font=ctk.CTkFont('Consolas',11),text_color=ACCENT)
        self.pos_lbl.pack(side='left')
        ctk.CTkButton(pi,text='Live Preview',width=100,height=26,fg_color=SURFACE_ALT,border_width=1,border_color=STROKE,text_color=ACCENT,command=self.live_preview).pack(side='right')
        ctk.CTkLabel(f,text=f'''Font size: {self.config['timer_font_size']}''',text_color=GRAY,font=ctk.CTkFont(size=10)).pack(anchor='w')
        self.font_sl = ctk.CTkSlider(f,from_=20,to=80,number_of_steps=60,command=self.on_font)
        self.font_sl.set(self.config['timer_font_size'])
        self.font_sl.pack(fill='x',pady=(2,12))
        self.build_hotkey_row(f,'timer','Hotkey')
        ctk.CTkLabel(f,text='Tekrar Time',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w',pady=(4,0))
        tr_row = ctk.CTkFrame(f,fg_color=CARD,corner_radius=10)
        tr_row.pack(fill='x',pady=(3,12))
        tri = ctk.CTkFrame(tr_row,fg_color='transparent')
        tri.pack(fill='x',padx=10,pady=8)
        ctk.CTkLabel(tri,text='Repeat when reaches 0',text_color=GRAY,font=ctk.CTkFont(size=11)).pack(side='left')
        self.timer_repeat_sw = ctk.CTkSwitch(tri,text='',width=42,progress_color=GREEN,button_color='#ddd',button_hover_color='#fff',command=self._on_timer_repeat_toggle)
        if self.config.get('timer_repeat',False):
          self.timer_repeat_sw.select()
        else:
          self.timer_repeat_sw.deselect()

        self.timer_repeat_sw.pack(side='right')
        ctk.CTkButton(f,text='Save & Close',height=38,fg_color=RED,hover_color=RED_H,font=ctk.CTkFont(size=13,weight='bold'),command=self.close_timer).pack(fill='x')
        self.time_panel.protocol('WM_DELETE_WINDOW',self.close_timer)
        return None

  def _on_timer_repeat_toggle(self):
    self.save_config()

  def pick_color(self):
    c = colorchooser.askcolor(title='Timer Color',initialcolor=self.config['color'])
    if c:
      if c[1]:
        self.color_box.configure(fg_color=c[1])
        self.color_txt.configure(text=c[1])
        self.save_config()
        return None
      else:
        return None

    else:
      return None

  def on_font(self,v):
    if self.preview_window:
      if self.preview_window.winfo_exists():
        try:
          self.preview_label.configure(font=('Consolas',self.config['timer_font_size'],'bold'))
          return None
        except Exception:
          return None

      else:
        return None

    else:
      return None

  def live_preview(self):
    if self.preview_window and self.preview_window.winfo_exists():
      self.preview_window.lift()
      return None
    else:
      self.preview_window = Tk()
      self.preview_window.overrideredirect(True)
      self.preview_window.attributes('-topmost',True)
      self.preview_window.geometry(f'''280x100+{self.config['timer_x']}+{self.config['timer_y']}''')
      self.preview_window.configure(bg='#010101')
      try:
        self.preview_window.wm_attributes('-transparentcolor','#010101')
      except Exception:
        self.preview_window.attributes('-alpha',0.9)

      self.preview_label = Label(self.preview_window,text='10:00',font=('Consolas',self.config['timer_font_size'],'bold'),fg=self.config['color'],bg='#010101')
      self.preview_label.pack(expand=True)
      self._drag = {'x':0,'y':0}
      def start(e):
        return None

      def drag(e):
        x = self.preview_window.winfo_x()+e.x-self._drag['x']
        y = self.preview_window.winfo_y()+e.y-self._drag['y']
        self.preview_window.geometry(f'''+{x}+{y}''')
        try:
          self.pos_lbl.configure(text=f'''X:{x}  Y:{y}''')
          return None
        except Exception:
          return None

      for w in (self.preview_window,self.preview_label):
        w.bind('<Button-1>',start)
        w.bind('<B1-Motion>',drag)

      def save():
        self.save_config()
        self.preview_window.destroy()
        self.preview_window = None

      Button(self.preview_window,text='Save Pos',command=save,bg=RED,fg='white',font=('Segoe UI',8),relief='flat').place(relx=0.5,rely=0.88,anchor='center')
      self.preview_window.protocol('WM_DELETE_WINDOW',save)
      return None

  def close_timer(self):
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      pass

    int
    int
    if hasattr(self,'timer_repeat_sw'):
      pass

    self.save_config()
    if self.preview_window:
      try:
        self.preview_window.destroy()
      except Exception:
        pass

      self.preview_window = None

    if self.time_panel:
      self.time_panel.destroy()
      self.time_panel = None

    self.update_status()

  def toggle_timer(self):
    if self.version_ok:
      return None
    else:
      if self.timer_running:
        self.close_overlay()
      else:
        self.show_overlay()

      self.refresh_starts()
      return None

  def show_overlay(self):
    if self.timer_overlay:
      return None
    else:
      self.timer_running = True
      self.remain = self.config['duration']
      self.timer_overlay = Tk()
      self.timer_overlay.overrideredirect(True)
      self.timer_overlay.attributes('-topmost',True)
      tr = '#010101'
      try:
        self.timer_overlay.wm_attributes('-transparentcolor',tr)
      except Exception:
        self.timer_overlay.attributes('-alpha',0.9)

      self.timer_overlay.configure(bg=tr)
      self.timer_overlay.geometry(f'''280x90+{self.config['timer_x']}+{self.config['timer_y']}''')
      self.tlbl = Label(self.timer_overlay,text=self.fmt(self.remain),font=('Consolas',self.config['timer_font_size'],'bold'),fg=self.config['color'],bg=tr)
      self.tlbl.pack(expand=True)
      self.tick_overlay()
      self.timer_overlay.protocol('WM_DELETE_WINDOW',self.close_overlay)
      return None

  def fmt(self,s):
    return f'''{s//60:02d}:{s%60:02d}'''

  def tick_overlay(self):
    if (self.timer_running and self.timer_overlay):
      return None
    else:
      self.tlbl.configure(text=self.fmt(self.remain),fg=self.config['color'])
      if self.remain <= 0:
        if self.config.get('timer_repeat',False):
          self.remain = self.config['duration']
          self.tlbl.configure(text=self.fmt(self.remain),fg=self.config['color'])
          self.timer_overlay.after(1000,self.tick_overlay)
          return None
        else:
          self.tlbl.configure(text='End Time',fg=DANGER)
          self.timer_overlay.after(1500,self.close_overlay)
          return None

      else:
        self.remain -= 1
        self.timer_overlay.after(1000,self.tick_overlay)
        return None

  def close_overlay(self):
    self.timer_running = False
    overlay = self.timer_overlay
    self.timer_overlay = None
    if overlay is not None:
      try:
        overlay.destroy()
      except Exception:
        pass

    if getattr(self,'_closing',False):
      if hasattr(self,'_pages'):
        if 'home' in self._pages:
          try:
            self.refresh_starts()
            return None
          except Exception:
            return None

        else:
          return None

      else:
        return None

    else:
      return None

  def open_autoclick(self):
    if self.need_update():
      return None
    else:
      if self.ac_panel and self.ac_panel.winfo_exists():
        self.ac_panel.lift()
        return None
      else:
        self.ac_panel = self._win11_toplevel('Auto Click','380x380')
        ctk.CTkLabel(self.ac_panel,text='Auto Click Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,10))
        f = ctk.CTkFrame(self.ac_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'autoclick','Hotkey')
        ctk.CTkLabel(f,text='Click count (0 = infinite)',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        self.ac_count_e = ctk.CTkEntry(f,height=32,justify='center',fg_color=CARD,border_color=STROKE)
        self.ac_count_e.pack(fill='x',pady=(3,10))
        self.ac_count_e.insert(0,str(self.config['autoclick_count']))
        ctk.CTkLabel(f,text='Interval (ms)',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        self.ac_int_e = ctk.CTkEntry(f,height=32,justify='center',fg_color=CARD,border_color=STROKE)
        self.ac_int_e.pack(fill='x',pady=(3,4))
        self.ac_int_e.insert(0,str(self.config['autoclick_interval_ms']))
        self.ac_int_e.bind('<KeyRelease>',self.update_cps)
        self.cps_lbl = ctk.CTkLabel(f,text='',font=ctk.CTkFont(size=10),text_color=TEXT_TERTIARY)
        self.cps_lbl.pack(anchor='w',pady=(0,12))
        self.update_cps()
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_ac).pack(fill='x')
        self.ac_panel.protocol('WM_DELETE_WINDOW',self.close_ac)
        return None

  def update_cps(self,e=None):
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      self.cps_lbl.configure(text='')
      return None

    int
    ms = __CHAOS_PY_NO_FUNC_ERR__(max,10((self.ac_int_e.get() or 80)))
    self.cps_lbl.configure(text=f'''≈ {round(1000/ms,1)} clicks / sec''')

  def close_ac(self):
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      pass

    int
    int
    self.save_config()
    if self.ac_panel:
      self.ac_panel.destroy()
      self.ac_panel = None

    self.update_status()

  def toggle_ac(self):
    if self.version_ok:
      return None
    else:
      if self.ac_running:
        self.ac_running = False
        self.refresh_starts()
        return None
      else:
        self.ac_running = True
        self.refresh_starts()
        count = self.config.get('autoclick_count',0)
        interval = self.config.get('autoclick_interval_ms',80)/1000
        def loop():
          n = 0
          while self.ac_running:
            try:
              self.mouse.click(MouseButton.left)
            except Exception:
              pass

            n += 1
            if count > 0 and n >= count:
              break
            else:
              time.sleep(interval)
              continue

          self.ac_running = False
          self.after(0,self.refresh_starts)

        threading.Thread(target=loop,daemon=True).start()
        return None

  def open_autofish(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.autofish_panel and self.autofish_panel.winfo_exists():
        self.autofish_panel.lift()
        return None
      else:
        self.autofish_panel = self._win11_toplevel('Auto Fish','380x240')
        ctk.CTkLabel(self.autofish_panel,text='Auto Fish Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,10))
        f = ctk.CTkFrame(self.autofish_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_autofish_bind_row(f)
        ctk.CTkLabel(f,text='Only the bind key can be changed.',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,12))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_autofish).pack(fill='x')
        self.autofish_panel.protocol('WM_DELETE_WINDOW',self.close_autofish)
        return None

  def build_autofish_bind_row(self,parent):
    '''Auto Fish has only one setting: the bind key. No modifier/options.'''
    ctk.CTkLabel(parent,text='Bind Key',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
    hr = ctk.CTkFrame(parent,fg_color=CARD,corner_radius=10)
    hr.pack(fill='x',pady=(3,10))
    hi = ctk.CTkFrame(hr,fg_color='transparent')
    hi.pack(fill='x',padx=10,pady=8)
    self.autofish_hk_lbl = ctk.CTkLabel(hi,text=f'''Key: {self.config.get('autofish_hotkey_display','F8')}''',text_color=ACCENT)
    self.autofish_hk_lbl.pack(side='left')
    self.autofish_bind_btn = ctk.CTkButton(hi,text='Bind',width=70,height=26,fg_color=SURFACE_ALT,border_width=1,border_color=STROKE,text_color=ACCENT,command=lambda : self.start_bind('autofish'))
    self.autofish_bind_btn.pack(side='right')

  def close_autofish(self):
    if self.autofish_panel:
      try:
        self.autofish_panel.destroy()
      except Exception:
        pass

      self.autofish_panel = None

    self.update_status()

  def toggle_autofish(self):
    if (self.version_ok and self.license_active):
      return None
    else:
      if self.autofish_running:
        self.autofish_running = False
        self.refresh_starts()
        return None
      else:
        self.autofish_running = True
        self.refresh_starts()
        threading.Thread(target=self.autofish_loop,daemon=True).start()
        return None

  def _autofish_calibrate(self,sct,monitor):
    '''
Find the red/yellow/green vertical meter in the lower-right area.
The target is near the lower end of the green section, matching
the arrow position in the supplied reference screenshot.
'''
    from PIL import Image
    W = monitor['width']
    H = monitor['height']
    search = {'left':monitor['left']+int(W*0.8),'top':monitor['top']+int(H*0.65),'width':max(1,int(W*0.2)),'height':max(1,int(H*0.35))}
    shot = sct.grab(search)
    im = Image.frombytes('RGB',shot.size,shot.rgb)
    pix = im.load()
    sw,sh = im.size
    col_counts = [0]*sw
    for x in range(0,sw,2):
      c = 0
      for y in range(0,sh,2):
        r,g,b = pix[(x,y)]
        mx = max(r,g,b)
        mn = min(r,g,b)
        if mx <= 70:
          continue

        if mx-mn <= 50:
          continue

        c += 1

      continue
      x

    best_x = max(range(sw),key=lambda x: col_counts[x])
    if col_counts[best_x] < max(25,sh//12):
      return None
    else:
      def sat_count_at_x(x):
        c = 0
        for y in range(0,sh,2):
          r,g,b = pix[(x,y)]
          mx = max(r,g,b)
          mn = min(r,g,b)
          if mx <= 70:
            continue

          if mx-mn <= 50:
            continue

          c += 1

        return c

      threshold = max(25,col_counts[best_x]//3)
      left = best_x
      right = best_x
      while left > 0:
        if sat_count_at_x(left-1) >= threshold:
          left -= 1
          continue

    rows = []
    green_rows = []
    for y in range(sh):
      sat = 0
      green = 0

    for x in range(left,right+1):
      r,g,b = pix[(x,y)]
      mx = max(r,g,b)
      mn = min(r,g,b)
      if mx > 70 and mx-mn > 50:
        sat += 1

      if g <= 70:
        continue

      if g <= r+15:
        continue

      if g <= b+15:
        continue

      green += 1
      continue
      col_counts

    width = max(1,right-left+1)
    if sat >= max(2,int(width*0.5)):
      rows.append(y)

    while green < max(2,int(width*0.5)):
      continue
      green_rows.append(y)

    c
    if rows and green_rows:
      pass

    return None
    bar_top = min(rows)
    bar_bottom = max(rows)
    green_bottom = max(green_rows)
    target_y = green_bottom-max(4,int(H*0.006))
    return {'screen_right':search['left']+right,'screen_top':search['top']+bar_top,'screen_bottom':search['top']+bar_bottom,'target_y':search['top']+target_y}

  def _autofish_arrow_y(self,sct,monitor,meter):
    '''Find the dark triangular arrow beside the meter by local contrast.'''
    from PIL import Image
    left = meter['screen_right']-monitor['left']+3
    top = meter['screen_top']-monitor['top']
    width = min(70,monitor['width']-left)
    height = min(meter['screen_bottom']-meter['screen_top']+1,monitor['height']-top)
    if width < 20 and height < 20:
      pass

    return None
    region = {'left':monitor['left']+left,'top':monitor['top']+top,'width':width,'height':height}
    shot = sct.grab(region)
    im = Image.frombytes('RGB',shot.size,shot.rgb)
    raw = im.tobytes()
    row_stride = width*3
    brightness = []
    for y in range(height):
      row = raw[y*row_stride:y+1*row_stride]
      brightness.append(sum(row)/max(1,len(row)))

    best_y = None
    best_contrast = 0
    edge = 6
    for y in range(edge,height-edge):
      contrast = brightness[y-edge]+brightness[y+edge]/2-brightness[y]
      if contrast <= best_contrast:
        continue

      best_contrast = contrast
      best_y = y

    if best_y is not None and best_contrast < 2.8:
      pass

    return None
    return region['top']+best_y

  def _autofish_press_keys(self):
    '''Press J H I K L G together and release them within 0.1 second.'''
    keys = ('j','h','i','k','l','g','p')
    try:
      for key in keys:
        self.kb.press(key)

      time.sleep(0.015)
      for key in reversed(keys):
        self.kb.release(key)

      return None
    except Exception:
      for key in keys:
        try:
          self.kb.release(key)
        except Exception:
          pass

    except:
      pass
    except:
      continue
      return None

  def autofish_loop(self):
    try:
      import mss
    except ImportError:
      self.autofish_running = False
      self.after(0,lambda : messagebox.showerror('Auto Fish','''Auto Fish needs the \'mss\' package.

Install it with: pip install mss'''))
      self.after(0,self.refresh_starts)
      return None

    triggered = False
    meter = None
    last_calibration = 0
    try:
      with mss.mss() as sct:
        monitor = sct.monitors[1]
        while self.autofish_running:
          if self.license_active:
            now = time.monotonic()
            if meter is not None and now-last_calibration > 3:
              pass

            meter = self._autofish_calibrate(sct,monitor)
            last_calibration = now
            if meter is None:
              time.sleep(0.2)
              continue

            arrow_y = self._autofish_arrow_y(sct,monitor,meter)
            if arrow_y is None:
              triggered = False
              time.sleep(0.008)
              continue

            distance = abs(arrow_y-meter['target_y'])

    except Exception:
      return None

    __CHAOS_PY_NO_FUNC_ERR__()
    (distance <= 9 and (triggered or self._autofish_press_keys))(5)
    self.kb.press('`')
    self.kb.release('`')
    time.sleep(0.2)
    self.kb.type('fish')
    self.kb.press(Key.enter)
    self.kb.release(Key.enter)
    self.kb.press('`')
    self.kb.release('`')
    triggered = False
    if distance >= 22:
      triggered = False

    while __CHAOS_PY_TEST_NOT_INIT_ERR__:
      time.sleep(0.006)

    self.autofish_running = False
    self.after(0,self.refresh_starts)

  def type_str(self,s):
    for ch in s:
      self.kb.type(ch)
      time.sleep(0.008)

  def build_hotkey_row(self,parent,target,label_text='Hotkey'):
    ctk.CTkLabel(parent,text=label_text,font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
    hr = ctk.CTkFrame(parent,fg_color=CARD,corner_radius=10)
    hr.pack(fill='x',pady=(3,10))
    hi = ctk.CTkFrame(hr,fg_color='transparent')
    hi.pack(fill='x',padx=10,pady=8)
    __CHAOS_PY_NULL_PTR_VALUE_ERR__ = {'auto_dish':'auto_dish_modifier','auto_graf':'auto_graf_modifier','auto_key':'auto_key_modifier','auto_h':'auto_h_modifier','auto_f':'auto_f_modifier','auto_atm':'auto_atm_modifier','auto_burger_click':'auto_burger_click_modifier','auto_marijuana':'auto_marijuana_modifier','auto_burger':'auto_burger_modifier','autofish':'autofish_modifier','burger':'burger_modifier','colorchat':'colorchat_modifier','uzi':'uzi_modifier','m4':'m4_modifier','towcar':'towcar_modifier','autoclick':'autoclick_modifier','timer':'timer_modifier','graff_finder':'graff_finder_modifier'}
    __CHAOS_PY_NULL_PTR_VALUE_ERR__ = {'auto_dish':'auto_dish_hotkey','auto_graf':'auto_graf_hotkey','auto_key':'auto_key_hotkey','auto_h':'auto_h_hotkey','auto_f':'auto_f_hotkey','auto_atm':'auto_atm_hotkey','auto_burger_click':'auto_burger_click_hotkey','auto_marijuana':'auto_marijuana_hotkey','auto_burger':'auto_burger_hotkey','autofish':'autofish_hotkey','burger':'burger_hotkey','colorchat':'colorchat_hotkey','uzi':'uzi_hotkey','m4':'m4_hotkey','towcar':'towcar_hotkey','autoclick':'autoclick_hotkey','timer':'timer_hotkey','auto_key_spam':'auto_key_spam_key','graff_finder':'graff_finder_hotkey'}
    __CHAOS_PY_NULL_PTR_VALUE_ERR__ = {'auto_dish':'auto_dish_hotkey_display','auto_graf':'auto_graf_hotkey_display','auto_key':'auto_key_hotkey_display','auto_h':'auto_h_hotkey_display','auto_f':'auto_f_hotkey_display','auto_atm':'auto_atm_hotkey_display','auto_burger_click':'auto_burger_click_hotkey_display','auto_marijuana':'auto_marijuana_hotkey_display','auto_burger':'auto_burger_hotkey_display','autofish':'autofish_hotkey_display','burger':'burger_hotkey_display','colorchat':'colorchat_hotkey_display','uzi':'uzi_hotkey_display','m4':'m4_hotkey_display','towcar':'towcar_hotkey_display','autoclick':'autoclick_hotkey_display','timer':'timer_hotkey_display','auto_key_spam':'auto_key_spam_display','graff_finder':'graff_finder_hotkey_display'}
    current_mod = self.config.get(mod_cfg.get(target,''),'none')
    mod_display = {'none':'No Key','ctrl':'Ctrl','alt':'Alt','shift':'Shift'}.get(current_mod,'No Key')
    current_disp = self.config.get(disp_cfg.get(target,''),'...')
    __CHAOS_PY_NULL_PTR_VALUE_ERR__ = {'auto_key_spam':'auto_key_spam_hk_lbl','auto_dish':'auto_dish_hk_lbl','auto_graf':'auto_graf_hk_lbl','auto_key':'auto_key_hk_lbl','auto_h':'auto_h_hk_lbl','auto_f':'auto_f_hk_lbl','auto_atm':'auto_atm_hk_lbl','auto_burger_click':'auto_burger_click_hk_lbl','auto_marijuana':'auto_marijuana_hk_lbl','auto_burger':'auto_burger_hk_lbl','burger':'towcar2_hk_lbl','colorchat':'cc_hk_lbl','uzi':'uzi_hk_lbl','m4':'m4_hk_lbl','towcar':'tow_hk_lbl','autoclick':'ac_hk_lbl','timer':'timer_hk_lbl','graff_finder':'graff_finder_hk_lbl'}
    [PYERR>] PY OBJECT NULLPTR [<PYERR] = {'auto_key_spam':'auto_key_spam_bind_btn','auto_dish':'auto_dish_bind_btn','auto_graf':'auto_graf_bind_btn','auto_key':'auto_key_bind_btn','auto_h':'auto_h_bind_btn','auto_f':'auto_f_bind_btn','auto_atm':'auto_atm_bind_btn','auto_burger_click':'auto_burger_click_bind_btn','auto_marijuana':'auto_marijuana_bind_btn','auto_burger':'auto_burger_bind_btn','burger':'towcar2_bind_btn','colorchat':'cc_bind_btn','uzi':'uzi_bind_btn','m4':'m4_bind_btn','towcar':'tow_bind_btn','autoclick':'ac_bind_btn','timer':'timer_bind_btn','graff_finder':'graff_finder_bind_btn'}
    def on_mod_change(choice):
      mod = {'No Key':'none','Ctrl':'ctrl','Alt':'alt','Shift':'shift'}.get(choice,'none')
      raw_key = self.config.get(key_cfg[target],'?')
      key_disp = raw_key.upper().replace('_',' ')
      full_disp = self._mod_to_display(mod,key_disp)
      self.save_config()
      lbl = getattr(self,lbl_map.get(target,''),None)
      if lbl and lbl.winfo_exists():
        lbl.configure(text=f'''Key: {full_disp}''')

      self.restart_listeners()
      self.update_status()
      self.update_band_labels()

    mod_menu = ctk.CTkOptionMenu(hi,values=['No Key','Ctrl','Alt','Shift'],width=90,height=26,fg_color=SURFACE_ALT,button_color=STROKE,button_hover_color=SURFACE_ALT,dropdown_fg_color=CARD,text_color=ACCENT,command=on_mod_change)
    mod_menu.set(mod_display)
    mod_menu.pack(side='left',padx=(0,8))
    setattr(self,f'''{target}_mod_menu''',mod_menu)
    hk_lbl = ctk.CTkLabel(hi,text=f'''Key: {current_disp}''',text_color=ACCENT)
    hk_lbl.pack(side='left')
    setattr(self,lbl_map.get(target,f'''{target}_hk_lbl'''),hk_lbl)
    bind_btn = ctk.CTkButton(hi,text='Bind',width=70,height=26,fg_color=SURFACE_ALT,border_width=1,border_color=STROKE,text_color=ACCENT,command=lambda : self.start_bind(target))
    bind_btn.pack(side='right')
    setattr(self,btn_map.get(target,f'''{target}_bind_btn'''),bind_btn)

  def _clicker_source_dir(self):
    '''Folder that contains the bundled/source Clicker.exe.'''
    candidates = []
    if getattr(sys,'frozen',False):
      meipass = getattr(sys,'_MEIPASS',None)
      if meipass:
        candidates.append(meipass)

      candidates.append(os.path.dirname(sys.executable))

    candidates.append(BASE_DIR)
    try:
      candidates.append(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
      pass

    for folder in candidates:
      if folder:
        continue

      if os.path.isfile(os.path.join(folder,'Clicker.exe')):
        folder
        return

  def _get_clicker_runtime_dir(self):
    '''Stable writable folder for Clicker.exe.'''
    p = os.path.join(DATA_DIR,'clicker')
    os.makedirs(p,exist_ok=True)
    return p

  def _deploy_clicker_files(self):
    '''
Copy Clicker.exe (and any optional DLLs next to it) into
%APPDATA%/CodeMTA/clicker so it can be launched reliably from a onefile build.
Returns path to deployed Clicker.exe, or None.
'''
    src_dir = self._clicker_source_dir()
    if src_dir:
      return None
    else:
      runtime_dir = self._get_clicker_runtime_dir()
      src_exe = os.path.join(src_dir,'Clicker.exe')
      dst_exe = os.path.join(runtime_dir,'Clicker.exe')
      try:
        if os.path.isfile(src_exe):
          if os.path.isfile(dst_exe) and os.path.getsize(src_exe) != os.path.getsize(dst_exe) and os.path.getmtime(src_exe) > os.path.getmtime(dst_exe):
            pass

          shutil.copy2(src_exe,dst_exe)

      except Exception:
        if os.path.isfile(dst_exe):
          pass

      except:
        pass
        return None

      try:
        for name in os.listdir(src_dir):
          if name.lower().endswith('.dll'):
            continue

          src = os.path.join(src_dir,name)

        dst = os.path.join(runtime_dir,name)
        if os.path.isfile(src):
          pass

      except Exception:
        return None

      try:
        if os.path.isfile(dst) and os.path.getsize(src) != os.path.getsize(dst):
          while os.path.getmtime(src) > os.path.getmtime(dst):
            __CHAOS_PY_WHILE_PASS_ERR__

          shutil.copy2(src,dst)
          continue

      except Exception:
        pass

    if os.path.isfile(dst_exe):
      return dst_exe
    else:
      return None

  def _get_clicker_path(self):
    '''Locate a runnable Clicker.exe (prefers deployed runtime copy).'''
    runtime = os.path.join(self._get_clicker_runtime_dir(),'Clicker.exe')
    if os.path.isfile(runtime):
      return runtime
    else:
      src_dir = self._clicker_source_dir()
      if src_dir:
        p = os.path.join(src_dir,'Clicker.exe')
        if os.path.isfile(p):
          return p
        else:
          return None

      else:
        return None

  def _start_clicker_like_double_click(self):
    '''
Start Clicker.exe exactly like a user double-clicked the file in Explorer.
Uses os.startfile on Windows.
'''
    path = (self._deploy_clicker_files() or self._get_clicker_path())
    if (path and os.path.isfile(path)):
      try:
        self.after(0,lambda : messagebox.showerror('Auto Burger','Clicker.exe پیدا نشد.\nClicker.exe not found.'))
        return False
      except Exception:
        return False

    else:
      try:
        if os.name == 'nt':
          os.startfile(path)
        else:
          import subprocess
          [path]
          __CHAOS_PY_NO_FUNC_ERR__(subprocess.Popen,cwd=(os.path.dirname(path) or None))

      except Exception:
        try:
          self.after(0,lambda : messagebox.showerror('Auto Burger','نتوانست Clicker.exe را باز کند.\nFailed to open Clicker.exe.'))
        except Exception:
          pass

        return True
      except:
        return True

      time.sleep(0.4)
      return True

  def _send_shift_f2(self):
    '''Press Shift + F2 to close / stop Clicker.'''
    try:
      self.kb.press(Key.shift)
      time.sleep(0.02)
      self.kb.press(Key.f2)
      time.sleep(0.05)
      self.kb.release(Key.f2)
      self.kb.release(Key.shift)
      return None
    except Exception:
      try:
        self.kb.release(Key.f2)
      except Exception:
        pass

      return None
    except:
      return None

  def open_auto_burger(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_burger_panel and self.auto_burger_panel.winfo_exists():
        try:
          self.auto_burger_panel.lift()
          self.auto_burger_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_burger_panel = self._win11_toplevel('Auto Burger','380x240')
        ctk.CTkLabel(self.auto_burger_panel,text='Auto Burger Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_burger_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_burger','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Auto Clicker For Burger v1.0.0',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,12))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_burger).pack(fill='x')
        self.auto_burger_panel.protocol('WM_DELETE_WINDOW',self.close_auto_burger)
        return None

  def close_auto_burger(self):
    if self.auto_burger_panel:
      try:
        self.auto_burger_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_burger_panel.destroy()
      except Exception:
        pass

      self.auto_burger_panel = None

    self.update_status()

  def toggle_auto_burger(self):
    if getattr(self,'auto_burger_running',False):
      self.auto_burger_running = False
      self.refresh_starts()
      threading.Thread(target=self._send_shift_f2,daemon=True).start()
      return None
    else:
      if (self.version_ok and self.license_active):
        return None
      else:
        if self.config.get('lock_auto_burger',False):
          return None
        else:
          self.auto_burger_running = True
          self.refresh_starts()
          def work():
            try:
              ok = self._start_clicker_like_double_click()
              if ok:
                self.auto_burger_running = False
                self.after(0,self.refresh_starts)
                return None
              else:
                return None

            except Exception:
              self.auto_burger_running = False
              self.after(0,self.refresh_starts)
              return None

          threading.Thread(target=work,daemon=True).start()
          return None

  def open_auto_burger_click(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_burger_click_panel and self.auto_burger_click_panel.winfo_exists():
        try:
          self.auto_burger_click_panel.lift()
          self.auto_burger_click_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_burger_click_panel = self._win11_toplevel('Auto Biz','380x210')
        ctk.CTkLabel(self.auto_burger_click_panel,text='Auto Biz Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_burger_click_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_burger_click','Hotkey (Start / Stop)')
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_burger_click).pack(fill='x',pady=(4,12))
        self.auto_burger_click_panel.protocol('WM_DELETE_WINDOW',self.close_auto_burger_click)
        return None

  def close_auto_burger_click(self):
    if self.auto_burger_click_panel:
      try:
        self.auto_burger_click_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_burger_click_panel.destroy()
      except Exception:
        pass

      self.auto_burger_click_panel = None

    self.update_status()

  def toggle_auto_burger_click(self):
    if (self.version_ok and self.license_active):
      return None
    else:
      starting = not(getattr(self,'auto_burger_click_running',False))
      if starting:
        self.auto_burger_click_stop.clear()
        self.auto_burger_click_running = True
      else:
        self.auto_burger_click_running = False
        self.auto_burger_click_stop.set()

      self.refresh_starts()
      if starting:
        return None
      else:
        points = ((944,590),(1019,596),(1095,596),(942,550),(1015,548),(1112,548),(943,505),(1010,505),(1105,504))
        def work():
          try:
            if os.name != 'nt':
              raise RuntimeError('Auto Biz requires Windows.')

            import ctypes
            user32 = ctypes.windll.user32
            def move_and_click(x,y):
              if user32.SetCursorPos(int(x),int(y)):
                raise RuntimeError(f'''SetCursorPos failed at {x},{y}''')

              time.sleep(0.03)
              user32.mouse_event(2,0,0,0,0)
              user32.mouse_event(4,0,0,0,0)

          except Exception as e:
            self.auto_burger_click_running = False
            try:
              self.after(0,lambda err=str(e): messagebox.showerror('Auto Biz',f'''Mouse clicker error:\n{err}'''))
            except Exception:
              pass

          if (self.auto_burger_click_running and self.auto_burger_click_stop.is_set()):
            pass

          if getattr(self,'_closing',False) and self.license_active:
            for x,y in points:
              if (self.auto_burger_click_running and (self.auto_burger_click_stop.is_set() or getattr(self,'_closing',False) or self.license_active)):
                self.auto_burger_click_running = False
                try:
                  self.after(0,self.refresh_starts)
                  return None
                except Exception:
                  return None

              else:
                move_and_click(x,y)
                while self.auto_burger_click_stop.wait(1.1):
                  self.auto_burger_click_running = False
                  try:
                    self.after(0,self.refresh_starts)
                    return None
                  except Exception:
                    return None

        threading.Thread(target=work,daemon=True).start()
        return None

  def open_auto_atm(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_atm_panel and self.auto_atm_panel.winfo_exists():
        try:
          self.auto_atm_panel.lift()
          self.auto_atm_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_atm_panel = self._win11_toplevel('Auto ATM','380x240')
        ctk.CTkLabel(self.auto_atm_panel,text='Auto ATM Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_atm_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_atm','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Hack ATM "v1.0.0" buttons\n Only (1920x1080)',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,10))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_atm).pack(fill='x',pady=(4,12))
        self.auto_atm_panel.protocol('WM_DELETE_WINDOW',self.close_auto_atm)
        return None

  def close_auto_atm(self):
    if self.auto_atm_panel:
      try:
        self.auto_atm_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_atm_panel.destroy()
      except Exception:
        pass

      self.auto_atm_panel = None

    self.update_status()

  def toggle_auto_atm(self):
    if (self.version_ok and self.license_active):
      return None
    else:
      starting = not(getattr(self,'auto_atm_running',False))
      if starting:
        self.auto_atm_stop.clear()
        self.auto_atm_running = True
      else:
        self.auto_atm_running = False
        self.auto_atm_stop.set()

      self.refresh_starts()
      if starting:
        return None
      else:
        ATM_COLS = (662,775,890,1005,1125,1235)
        ATM_ROWS = (337,407,477,547,617,687,757)
        CAP_X = 600
        CAP_Y = 300
        CAP_W = 700
        CAP_H = 520
        def work():
          try:
            if os.name != 'nt':
              pass

          except Exception as e:
            pass

          try:
            gdi32.DeleteObject(hbmp)
            gdi32.DeleteDC(hdc_mem)
            user32.ReleaseDC(0,hdc_screen)
            self.auto_atm_running = False
          except Exception:
            pass

          try:
            self.after(0,self.refresh_starts)
            return None
          except Exception:
            return None

          self.auto_atm_running = False
          try:
            self.after(0,self.refresh_starts)
          except:
            pass
          except:
            pass
          except:
            pass
          except:
            pass
          except:
            pass
          except:
            pass
          except:
            pass
          except Exception:
            pass

        threading.Thread(target=work,daemon=True).start()
        return None

  def _close_status_overlay(self,which):
    '''which: \'f\', \'h\', or \'tow\''''
    attr = f'''auto_{which}_overlay'''
    job_attr = f'''_auto_{which}_hide_job'''
    job = getattr(self,job_attr,None)
    if job is not None:
      try:
        self.after_cancel(job)
      except Exception:
        pass

      setattr(self,job_attr,None)

    win = getattr(self,attr,None)
    setattr(self,attr,None)
    if win is not None:
      try:
        win.destroy()
        return None
      except Exception:
        return None

    else:
      return None

  def _show_status_overlay(self,which,text,color):
    show_key = f'''auto_{which}_show_info'''
    if self.config.get(show_key,False):
      return None
    else:
      self._close_status_overlay(which)
      _default_y = {'f':260,'h':320,'tow':380}.get(which,300)
      x = int(self.config.get(f'''auto_{which}_x''',300))
      y = int(self.config.get(f'''auto_{which}_y''',_default_y))
      fs = int(self.config.get(f'''auto_{which}_font_size''',28))
      win = Tk()
      win.overrideredirect(True)
      win.attributes('-topmost',True)
      tr = '#010101'
      try:
        win.wm_attributes('-transparentcolor',tr)
      except Exception:
        win.attributes('-alpha',0.92)

      win.configure(bg=tr)
      win.geometry(f'''360x70+{x}+{y}''')
      lbl = Label(win,text=text,font=('Consolas',fs,'bold'),fg=color,bg=tr)
      lbl.pack(expand=True)
      setattr(self,f'''auto_{which}_overlay''',win)
      if 'Stop' in text:
        job = self.after(2000,lambda w=which: self._close_status_overlay(w))
        setattr(self,f'''_auto_{which}_hide_job''',job)
        return None
      else:
        return None

  def _live_preview_status(self,which):
    prev_attr = f'''auto_{which}_preview'''
    old = getattr(self,prev_attr,None)
    if old is not None and old.winfo_exists():
      try:
        old.lift()
        return None
      except Exception:
        return None

    else:
      _default_y = {'f':260,'h':320,'tow':380}.get(which,300)
      x = int(self.config.get(f'''auto_{which}_x''',300))
      y = int(self.config.get(f'''auto_{which}_y''',_default_y))
      fs = int(self.config.get(f'''auto_{which}_font_size''',28))
      if which == 'f':
        sample = 'Auto F Run'
      else:
        sample = sample if which == 'h' else 'Auto H Run'

      win = Tk()
      win.overrideredirect(True)
      win.attributes('-topmost',True)
      tr = '#010101'
      try:
        win.wm_attributes('-transparentcolor',tr)
      except Exception:
        win.attributes('-alpha',0.9)

      win.configure(bg=tr)
      win.geometry(f'''360x90+{x}+{y}''')
      lbl = Label(win,text=sample,font=('Consolas',fs,'bold'),fg=GREEN,bg=tr)
      lbl.pack(expand=True)
      setattr(self,prev_attr,win)
      drag = {'x':0,'y':0}
      def start(e):
        return None

      def move(e):
        nx = win.winfo_x()+e.x-drag['x']
        ny = win.winfo_y()+e.y-drag['y']
        win.geometry(f'''+{nx}+{ny}''')
        pos_lbl = getattr(self,f'''auto_{which}_pos_lbl''',None)
        if pos_lbl is not None:
          try:
            pos_lbl.configure(text=f'''X:{nx}  Y:{ny}''')
            return None
          except Exception:
            return None

        else:
          return None

      for w in (win,lbl):
        w.bind('<Button-1>',start)
        w.bind('<B1-Motion>',move)

      def save():
        self.save_config()
        try:
          win.destroy()
        except Exception:
          pass

        setattr(self,prev_attr,None)

      Button(win,text='Save Pos',command=save,bg=RED,fg='white',font=('Segoe UI',8),relief='flat').place(relx=0.5,rely=0.88,anchor='center')
      win.protocol('WM_DELETE_WINDOW',save)
      return None

  def _build_status_settings_block(self,parent,which):
    prefix = f'''auto_{which}'''
    ctk.CTkLabel(parent,text='Status Text Position',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w',pady=(6,0))
    pr = ctk.CTkFrame(parent,fg_color=CARD,corner_radius=10)
    pr.pack(fill='x',pady=(3,8))
    pi = ctk.CTkFrame(pr,fg_color='transparent')
    pi.pack(fill='x',padx=10,pady=8)
    pos_lbl = ctk.CTkLabel(pi,text=f'''X:{self.config.get({prefix}_x,300)}  Y:{self.config.get({prefix}_y,260)}''',font=ctk.CTkFont('Consolas',11),text_color=ACCENT)
    pos_lbl.pack(side='left')
    setattr(self,f'''{prefix}_pos_lbl''',pos_lbl)
    ctk.CTkButton(pi,text='Live Preview',width=100,height=26,fg_color=SURFACE_ALT,border_width=1,border_color=STROKE,text_color=ACCENT,command=lambda : self._live_preview_status(which)).pack(side='right')
    fs = int(self.config.get(f'''{prefix}_font_size''',28))
    fs_lbl = ctk.CTkLabel(parent,text=f'''Font size: {fs}''',text_color=GRAY,font=ctk.CTkFont(size=10))
    fs_lbl.pack(anchor='w')
    setattr(self,f'''{prefix}_font_lbl''',fs_lbl)
    def on_font(v,w=which,lab=fs_lbl):
      val = int(float(v))
      lab.configure(text=f'''Font size: {val}''')
      prev = getattr(self,f'''auto_{w}_preview''',None)
      if prev is not None:
        try:
          for child in prev.winfo_children():
            if isinstance(child,Label):
              continue

            child.configure(font=('Consolas',val,'bold'))
            continue
            f'''auto_{w}_font_size'''

          return None
        except Exception:
          return None

      else:
        return None

    sl = ctk.CTkSlider(parent,from_=16,to=64,number_of_steps=48,command=on_font)
    sl.set(fs)
    sl.pack(fill='x',pady=(2,8))
    ctk.CTkLabel(parent,text='Namayesh Info',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w',pady=(2,0))
    tr = ctk.CTkFrame(parent,fg_color=CARD,corner_radius=10)
    tr.pack(fill='x',pady=(3,10))
    tri = ctk.CTkFrame(tr,fg_color='transparent')
    tri.pack(fill='x',padx=10,pady=8)
    ctk.CTkLabel(tri,text='ON = hide status text',text_color=GRAY,font=ctk.CTkFont(size=11)).pack(side='left')
    def on_toggle(w=which):
      sw = getattr(self,f'''auto_{w}_show_sw''',None)
      if sw is None:
        return None
      else:
        self.save_config()
        if self.config[f'''auto_{w}_show_info''']:
          self._close_status_overlay(w)
          return None
        else:
          return None

    sw = ctk.CTkSwitch(tri,text='',width=42,progress_color=GREEN,button_color='#ddd',button_hover_color='#fff',command=on_toggle)
    if self.config.get(f'''{prefix}_show_info''',False):
      sw.select()
    else:
      sw.deselect()

    sw.pack(side='right')
    setattr(self,f'''{prefix}_show_sw''',sw)

  def open_auto_f(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_f_panel and self.auto_f_panel.winfo_exists():
        try:
          self.auto_f_panel.lift()
          self.auto_f_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_f_panel = self._win11_toplevel('Auto F','380x470')
        ctk.CTkLabel(self.auto_f_panel,text='Auto F Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_f_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_f','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Taps F with slight timing variation (0.10–0.15s)',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,4))
        self._build_status_settings_block(f,'f')
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_f).pack(fill='x',pady=(4,12))
        self.auto_f_panel.protocol('WM_DELETE_WINDOW',self.close_auto_f)
        return None

  def close_auto_f(self):
    prev = getattr(self,'auto_f_preview',None)
    if prev is not None:
      try:
        prev.destroy()
      except Exception:
        pass

      self.auto_f_preview = None

    try:
      if :
        pass

    except Exception:
      pass

    self.save_config()
    if self.auto_f_panel:
      try:
        self.auto_f_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_f_panel.destroy()
      except Exception:
        pass

      self.auto_f_panel = None

    self.update_status()
    self.update_band_labels()

  def toggle_auto_f(self):
    if (self.version_ok and self.license_active):
      return None
    else:
      if self.auto_f_running:
        self.auto_f_running = False
        self.auto_f_stop.set()
        self._show_status_overlay('f','Auto F Stop',DANGER)
        self.refresh_starts()
        return None
      else:
        self.auto_f_stop.clear()
        self.auto_f_running = True
        self._show_status_overlay('f','Auto F Run',GREEN)
        self.refresh_starts()
        threading.Thread(target=self._auto_letter_loop,args=('f','auto_f'),daemon=True).start()
        return None

  def open_auto_h(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_h_panel and self.auto_h_panel.winfo_exists():
        try:
          self.auto_h_panel.lift()
          self.auto_h_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_h_panel = self._win11_toplevel('Auto H','380x470')
        ctk.CTkLabel(self.auto_h_panel,text='Auto H Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_h_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_h','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Taps H with slight timing variation (0.10–0.15s)',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,4))
        self._build_status_settings_block(f,'h')
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_h).pack(fill='x',pady=(4,12))
        self.auto_h_panel.protocol('WM_DELETE_WINDOW',self.close_auto_h)
        return None

  def close_auto_h(self):
    prev = getattr(self,'auto_h_preview',None)
    if prev is not None:
      try:
        prev.destroy()
      except Exception:
        pass

      self.auto_h_preview = None

    try:
      if :
        pass

    except Exception:
      pass

    self.save_config()
    if self.auto_h_panel:
      try:
        self.auto_h_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_h_panel.destroy()
      except Exception:
        pass

      self.auto_h_panel = None

    self.update_status()
    self.update_band_labels()

  def toggle_auto_h(self):
    if (self.version_ok and self.license_active):
      return None
    else:
      if self.auto_h_running:
        self.auto_h_running = False
        self.auto_h_stop.set()
        self._show_status_overlay('h','Auto H Stop',DANGER)
        self.refresh_starts()
        return None
      else:
        self.auto_h_stop.clear()
        self.auto_h_running = True
        self._show_status_overlay('h','Auto H Run',GREEN)
        self.refresh_starts()
        threading.Thread(target=self._auto_letter_loop,args=('h','auto_h'),daemon=True).start()
        return None

  def _name_to_vk(self,key_name):
    '''Resolve a key name to a Windows Virtual-Key code.'''
    str
    name = __CHAOS_PY_NO_FUNC_ERR__((key_name or '')).strip().lower()
    if name:
      return None
    else:
      if len(name) == 1 and 'a' <= name and name <= 'z':
        return ord(name.upper())
      else:
        if len(name) == 1 and '0' <= name and name <= '9':
          return ord(name)
        else:
          [PYERR>] PY OBJECT NULLPTR [<PYERR] = {'esc':27,'tab':9,'return':13,'enter':13,'space':32,'f12':123,'f11':122,'f10':121,'f9':120,'f8':119,'f7':118,'f6':117,'f5':116,'f4':115,'f3':114,'f2':113,'f1':112,'escape':27,'backspace':8,'shift':16,'ctrl':17,'alt':18,'up':38,'down':40,'left':37,'right':39,'insert':45,'delete':46,'home':36,'end':35,'pageup':33,'pagedown':34}
          return special.get(name)

  def _tap_key(self,key_name):
    '''
Hardware-like key tap for games (MTA/GTA).
Uses Windows keybd_event + scan code so the game sees a real key,
not typed text input.
'''
    vk = self._name_to_vk(key_name)
    if vk is None:
      try:
        __CHAOS_PY_PASS_ERR__
      except Exception:
        return None

      str
      name = __CHAOS_PY_NO_FUNC_ERR__((key_name or '')).strip().lower()
      k = KEY_MAP.get(name,name)
      self.kb.press(k)
      self.kb.release(k)
      return None
    else:
      try:
        import ctypes
        user32 = ctypes.windll.user32
        scan = user32.MapVirtualKeyW(vk,0)&255
        KEYEVENTF_KEYUP = 2
        user32.keybd_event(vk,scan,0,0)
        time.sleep(0.012)
        user32.keybd_event(vk,scan,KEYEVENTF_KEYUP,0)
        return None
      except Exception:
        try:
          k = KeyCode.from_vk(vk)
          self.kb.press(k)
          self.kb.release(k)
        except Exception:
          pass

      except:
        pass
      except:
        return None

  def _auto_letter_loop(self,letter,flag_name):
    '''Press a letter key with varying short delays until stopped.'''
    delays = (0.1,0.12,0.15,0.11)
    stop_attr = f'''{flag_name}_stop'''
    i = 0
    try:
      pass    except:
      setattr(self,f'''{flag_name}_running''',False)
      try:
        self.after(0,self.refresh_starts)
      except Exception:
        pass

    except:
      pass

    setattr(self,f'''{flag_name}_running''',False)
    try:
      self.after(0,self.refresh_starts)
      return None
    except Exception:
      return None

  def open_auto_key(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_key_panel and self.auto_key_panel.winfo_exists():
        try:
          self.auto_key_panel.lift()
          self.auto_key_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_key_panel = self._win11_toplevel('Auto Key','380x370')
        ctk.CTkLabel(self.auto_key_panel,text='Auto Key Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_key_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_key','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Spam Key',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        hr = ctk.CTkFrame(f,fg_color=CARD,corner_radius=10)
        hr.pack(fill='x',pady=(3,10))
        hi = ctk.CTkFrame(hr,fg_color='transparent')
        hi.pack(fill='x',padx=10,pady=8)
        self.auto_key_spam_hk_lbl = ctk.CTkLabel(hi,text=f'''Key: {self.config.get('auto_key_spam_display','E')}''',text_color=ACCENT)
        self.auto_key_spam_hk_lbl.pack(side='left')
        self.auto_key_spam_bind_btn = ctk.CTkButton(hi,text='Bind',width=70,height=26,fg_color=SURFACE_ALT,border_width=1,border_color=STROKE,text_color=ACCENT,command=lambda : self.start_bind('auto_key_spam'))
        self.auto_key_spam_bind_btn.pack(side='right')
        ctk.CTkLabel(f,text='Interval (seconds)',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        self.auto_key_interval_e = ctk.CTkEntry(f,height=32,justify='center',fg_color=CARD,border_color=STROKE)
        self.auto_key_interval_e.pack(fill='x',pady=(3,12))
        self.auto_key_interval_e.insert(0,str(self.config.get('auto_key_interval',0.12)))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_key).pack(fill='x',pady=(4,12))
        self.auto_key_panel.protocol('WM_DELETE_WINDOW',self.close_auto_key)
        return None

  def close_auto_key(self):
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      pass

    float
    val = __CHAOS_PY_NO_FUNC_ERR__((self.auto_key_interval_e.get() or 0.12))
    self.save_config()
    if self.auto_key_panel:
      try:
        self.auto_key_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_key_panel.destroy()
      except Exception:
        pass

      self.auto_key_panel = None

    self.update_status()
    self.update_band_labels()

  def toggle_auto_key(self):
    if (self.version_ok and self.license_active):
      return None
    else:
      if self.auto_key_running:
        self.auto_key_running = False
        self.auto_key_stop.set()
        self.refresh_starts()
        return None
      else:
        self.auto_key_stop.clear()
        self.auto_key_running = True
        self.refresh_starts()
        threading.Thread(target=self._auto_key_loop,daemon=True).start()
        return None

  def _auto_key_loop(self):
    str
    key_name = __CHAOS_PY_NO_FUNC_ERR__((self.config.get('auto_key_spam_key','e') or 'e')).lower()
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      interval = 0.12

    float
    interval = __CHAOS_PY_NO_FUNC_ERR__((self.config.get('auto_key_interval',0.12) or 0.12))
    interval = max(0.02,min(5,interval))
    try:
      pass    except:
      self.auto_key_running = False
      try:
        self.after(0,self.refresh_starts)
      except Exception:
        pass

    except:
      pass

    self.auto_key_running = False
    try:
      self.after(0,self.refresh_starts)
      return None
    except Exception:
      return None

  def open_auto_graf(self):
    '''Auto Graf settings: bind the hotkey used to show/hide Graff.png.'''
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_graf_panel and self.auto_graf_panel.winfo_exists():
        try:
          self.auto_graf_panel.lift()
          self.auto_graf_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_graf_panel = self._win11_toplevel('Auto Graf','380x240')
        ctk.CTkLabel(self.auto_graf_panel,text='Auto Graf Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_graf_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_graf','Hotkey (Show / Hide Graff)')
        ctk.CTkLabel(f,text='Press the bound key once to show Graff.png, again to hide it.',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,10))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_graf).pack(fill='x',pady=(4,12))
        self.auto_graf_panel.protocol('WM_DELETE_WINDOW',self.close_auto_graf)
        return None

  def close_auto_graf(self):
    if self.auto_graf_panel:
      try:
        self.auto_graf_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_graf_panel.destroy()
      except Exception:
        pass

      self.auto_graf_panel = None

    self.update_status()
    self.update_band_labels()

  def toggle_auto_graf(self):
    '''Exact toggle behavior: one press opens Graff.png, next press closes it.'''
    if (self.version_ok and self.license_active):
      return None
    else:
      overlay_open = False
      try:
        ov = getattr(self,'graff_finder_overlay',None)
      except Exception:
        overlay_open = getattr(self,'graff_finder_overlay',None) is not None

      overlay_open = (ov is not None and bool(ov.winfo_exists()))
      if self.auto_graf_running and overlay_open:
        pass

      self.close_graff_finder_overlay()
      self.auto_graf_running = False
      self.refresh_starts()
      return None
      img_path = self._find_graff_image()
      if img_path:
        try:
          messagebox.showerror('Auto Graf','''Graff.png پیدا نشد!

فایل Graff.png را کنار Shadow.py یا کنار فایل exe بگذارید.''')
          return None
        except Exception:
          return None

      else:
        try:
          self.show_graff_finder_overlay(img_path)
          self.auto_graf_running = True
          self.refresh_starts()
          return None
        except Exception as e:
          self.auto_graf_running = False
          self.close_graff_finder_overlay()
          try:
            messagebox.showerror('Auto Graf',f'''خطا در نمایش Graff.png:\n{e}''')
          except:
            pass

          return None

  def _find_graff_image(self):
    '''Locate Graff.png next to the script / exe / APPDATA / cwd.'''
    candidates = []
    if getattr(sys,'frozen',False):
      meipass = getattr(sys,'_MEIPASS',None)
      if meipass:
        candidates.append(meipass)

      candidates.append(os.path.dirname(sys.executable))

    candidates.append(BASE_DIR)
    candidates.append(DATA_DIR)
    try:
      candidates.append(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
      pass

    try:
      candidates.append(os.getcwd())
    except Exception:
      pass

    for folder in candidates:
      if folder:
        continue

      for name in ('Graff.png','graff.png','GRAFF.png'):
        p = os.path.join(folder,name)

    if os.path.isfile(p):
      pass

    try:
      dst = os.path.join(DATA_DIR,'Graff.png')
      if os.path.abspath(p) != os.path.abspath(dst) and os.path.isfile(dst):
        while os.path.getsize(p) != os.path.getsize(dst):
          pass

    except Exception:
      pass

  def open_graff_finder(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.graff_finder_panel and self.graff_finder_panel.winfo_exists():
        try:
          self.graff_finder_panel.lift()
          self.graff_finder_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.graff_finder_panel = self._win11_toplevel('Graff Finder','380x240')
        ctk.CTkLabel(self.graff_finder_panel,text='Graff Finder Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.graff_finder_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'graff_finder','Hotkey (Show / Hide map)')
        ctk.CTkLabel(f,text='Shows graffiti locations over the in-game radar map',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,10))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_graff_finder).pack(fill='x',pady=(4,12))
        self.graff_finder_panel.protocol('WM_DELETE_WINDOW',self.close_graff_finder)
        return None

  def close_graff_finder(self):
    if self.graff_finder_panel:
      try:
        self.graff_finder_panel.grab_release()
      except Exception:
        pass

      try:
        self.graff_finder_panel.destroy()
      except Exception:
        pass

      self.graff_finder_panel = None

    self.update_status()
    self.update_band_labels()

  def toggle_graff_finder(self):
    if self.version_ok:
      return None
    else:
      if self.license_active:
        try:
          messagebox.showwarning('Graff Finder','این قابلیت Pro است.\nبرای استفاده باید لایسنس فعال باشد.')
          return None
        except Exception:
          return None

      else:
        overlay_open = False
        try:
          ov = getattr(self,'graff_finder_overlay',None)
        except Exception:
          overlay_open = getattr(self,'graff_finder_overlay',None) is not None

        overlay_open = (ov is not None and bool(ov.winfo_exists()))
        if self.graff_finder_running and overlay_open:
          pass

        self.close_graff_finder_overlay()
        self.refresh_starts()
        return None
        img_path = self._find_graff_image()
        if img_path:
          try:
            messagebox.showerror('Graff Finder','''Graff.png پیدا نشد!

فایل Graff.png را کنار Shadow.py یا کنار فایل exe بگذارید.
Place Graff.png next to Shadow.py / the .exe''')
          except Exception:
            pass

          self.graff_finder_running = False
          try:
            self.refresh_starts()
            return None
          except Exception:
            return None

        else:
          try:
            self.show_graff_finder_overlay(img_path)
            self.refresh_starts()
            return None
          except Exception as e:
            self.close_graff_finder_overlay()
            self.refresh_starts()
            try:
              messagebox.showerror('Graff Finder',f'''خطا در نمایش نقشه:\n{e}''')
            except:
              pass

            return None

  def _apply_clickthrough_styles(self,ov):
    '''Make window click-through and non-activating (Windows only).'''
    if os.name != 'nt':
      return None
    else:
      try:
        import ctypes
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 524288
        WS_EX_TRANSPARENT = 32
        WS_EX_TOPMOST = 8
        WS_EX_NOACTIVATE = 134217728
        WS_EX_TOOLWINDOW = 128
        SWP_NOACTIVATE = 16
        SWP_SHOWWINDOW = 64
        SWP_NOMOVE = 2
        SWP_NOSIZE = 1
        HWND_TOPMOST = -1
        user32 = ctypes.windll.user32
        hwnd = ov.winfo_id()
        parent = user32.GetParent(hwnd)
        if parent:
          hwnd = parent

        style = user32.GetWindowLongW(hwnd,GWL_EXSTYLE)
        style |= WS_EX_LAYERED|WS_EX_TRANSPARENT|WS_EX_TOPMOST|WS_EX_NOACTIVATE|WS_EX_TOOLWINDOW
        user32.SetWindowLongW(hwnd,GWL_EXSTYLE,style)
        user32.SetWindowPos(hwnd,HWND_TOPMOST,0,0,0,0,SWP_NOMOVE|SWP_NOSIZE|SWP_NOACTIVATE|SWP_SHOWWINDOW)
        return None
      except Exception:
        return None

  def show_graff_finder_overlay(self,img_path):
    '''Show Graff.png stretched to the in-game map size & position.\nClick-through + no focus steal so the game keeps mouse/keyboard.'''
    self.close_graff_finder_overlay()
    try:
      from PIL import Image as PILImage
      from PIL import ImageTk
    except Exception:
      try:
        messagebox.showerror('Graff Finder','Pillow (PIL) is required.')
      except Exception:
        pass

    except:
      pass

    try:
      pil_img = PILImage.open(img_path).convert('RGBA')
    except Exception as e:
      try:
        messagebox.showerror('Graff Finder',f'''Cannot open image:\n{e}''')
      except Exception:
        pass

    try:
      sw = int(self.winfo_screenwidth())
      sh = int(self.winfo_screenheight())
    except Exception:
      sh = 1080
      sw = 1920

    if pil_img.size != (sw,sh):
      try:
        pil_img = pil_img.resize((sw,sh),PILImage.Resampling.LANCZOS)
      except Exception:
        try:
          pil_img = pil_img.resize((sw,sh),PILImage.LANCZOS)
        except Exception:
          pil_img = pil_img.resize((sw,sh))

      except:
        pass

    CHROMA = '#FF00FF'
    try:
      px = pil_img.load()
      w,h = pil_img.size
      for y in range(h):
        for x in range(w):
          r,g,b,a = px[(x,y)]
          if a == 0:
            continue

          if r >= 245 and g <= 20 and b >= 245:
            continue

          brightness = max(r,g,b)
          if brightness <= 24:
            continue

          if brightness >= 55:
            continue

          alpha = int(brightness-24*255/31)
          continue
          (x,y)

        continue
        px

      pil_img = pil_img.convert('RGBA')
    except Exception:
      pass

    ov = Tk()
    ov.withdraw()
    ov.overrideredirect(True)
    ov.attributes('-topmost',True)
    try:
      ov.wm_attributes('-transparentcolor',CHROMA)
    except Exception:
      try:
        ov.attributes('-transparentcolor',CHROMA)
      except Exception:
        pass

    except:
      pass

    ov.geometry(f'''{sw}x{sh}+0+0''')
    ov.configure(bg=CHROMA)
    self._graff_photo = ImageTk.PhotoImage(pil_img,master=ov)
    lbl = Label(ov,image=self._graff_photo,bg=CHROMA,borderwidth=0,highlightthickness=0)
    lbl.image = self._graff_photo
    lbl.pack(fill='both',expand=True)
    self._graff_label = lbl
    ov.update_idletasks()
    ov.deiconify()
    ov.lift()
    ov.update()
    self._graff_hwnd = None
    try:
      import ctypes
      hwnd = ov.winfo_id()
      parent = ctypes.windll.user32.GetParent(hwnd)
      self._graff_hwnd = parent if parent else hwnd
    except Exception:
      try:
        self._graff_hwnd = ov.winfo_id()
      except Exception:
        self._graff_hwnd = None

    except:
      pass

    self._apply_clickthrough_styles(ov)
    try:
      ov.after(50,lambda : self._apply_clickthrough_styles(ov))
      ov.after(250,lambda : self._apply_clickthrough_styles(ov))
    except Exception:
      pass

    try:
      ov.focus_set = lambda : None
    except Exception:
      pass

    self.graff_finder_overlay = ov
    self.graff_finder_running = True
    ov.protocol('WM_DELETE_WINDOW',self.close_graff_finder_overlay)
    return None
    e = None
    del(e)

  def close_graff_finder_overlay(self):
    '''Force-close the Graff overlay window (must always work on Stop / hotkey).'''
    self.graff_finder_running = False
    ov = getattr(self,'graff_finder_overlay',None)
    hwnd = getattr(self,'_graff_hwnd',None)
    self.graff_finder_overlay = None
    self._graff_photo = None
    self._graff_label = None
    self._graff_hwnd = None
    if ov is not None:
      try:
        ov.attributes('-topmost',False)
      except Exception:
        pass

      try:
        ov.attributes('-alpha',1)
      except Exception:
        pass

      try:
        ov.withdraw()
      except Exception:
        pass

      try:
        ov.update_idletasks()
      except Exception:
        pass

      try:
        ov.destroy()
      except Exception:
        pass

    if hwnd and os.name == 'nt':
      try:
        import ctypes
        user32 = ctypes.windll.user32
        if user32.IsWindow(hwnd):
          user32.ShowWindow(hwnd,0)
          user32.DestroyWindow(hwnd)

      except Exception:
        pass

    if getattr(self,'_closing',False):
      try:
        self.refresh_starts()
        return None
      except Exception:
        return None

    else:
      return None

  def _marijuana_source_dir(self):
    candidates = []
    if getattr(sys,'frozen',False):
      meipass = getattr(sys,'_MEIPASS',None)
      if meipass:
        candidates.append(meipass)

      candidates.append(os.path.dirname(sys.executable))

    candidates.append(BASE_DIR)
    try:
      candidates.append(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
      pass

    for folder in candidates:
      if folder:
        continue

      if os.path.isfile(os.path.join(folder,'Marijuana.exe')):
        folder
        return

  def _get_marijuana_runtime_dir(self):
    p = os.path.join(DATA_DIR,'marijuana')
    os.makedirs(p,exist_ok=True)
    return p

  def _deploy_marijuana_files(self):
    src_dir = self._marijuana_source_dir()
    if src_dir:
      return None
    else:
      runtime_dir = self._get_marijuana_runtime_dir()
      src_exe = os.path.join(src_dir,'Marijuana.exe')
      dst_exe = os.path.join(runtime_dir,'Marijuana.exe')
      try:
        if os.path.isfile(src_exe):
          if os.path.isfile(dst_exe) and os.path.getsize(src_exe) != os.path.getsize(dst_exe) and os.path.getmtime(src_exe) > os.path.getmtime(dst_exe):
            pass

          shutil.copy2(src_exe,dst_exe)

      except Exception:
        if os.path.isfile(dst_exe):
          pass

      except:
        pass
        return None

      try:
        for name in os.listdir(src_dir):
          if name.lower().endswith('.dll'):
            continue

          src = os.path.join(src_dir,name)

        dst = os.path.join(runtime_dir,name)
        if os.path.isfile(src):
          pass

      except Exception:
        return None

      try:
        if os.path.isfile(dst) and os.path.getsize(src) != os.path.getsize(dst):
          while os.path.getmtime(src) > os.path.getmtime(dst):
            __CHAOS_PY_WHILE_PASS_ERR__

          shutil.copy2(src,dst)
          continue

      except Exception:
        pass

    if os.path.isfile(dst_exe):
      return dst_exe
    else:
      return None

  def _get_marijuana_path(self):
    runtime = os.path.join(self._get_marijuana_runtime_dir(),'Marijuana.exe')
    if os.path.isfile(runtime):
      return runtime
    else:
      src_dir = self._marijuana_source_dir()
      if src_dir:
        p = os.path.join(src_dir,'Marijuana.exe')
        if os.path.isfile(p):
          return p
        else:
          return None

      else:
        return None

  def _start_marijuana_like_double_click(self):
    path = (self._deploy_marijuana_files() or self._get_marijuana_path())
    if (path and os.path.isfile(path)):
      try:
        self.after(0,lambda : messagebox.showerror('Auto Marijuana','Marijuana.exe پیدا نشد.\nMarijuana.exe not found.'))
        return False
      except Exception:
        return False

    else:
      try:
        if os.name == 'nt':
          os.startfile(path)
        else:
          import subprocess
          [path]
          __CHAOS_PY_NO_FUNC_ERR__(subprocess.Popen,cwd=(os.path.dirname(path) or None))

      except Exception:
        try:
          self.after(0,lambda : messagebox.showerror('Auto Marijuana','نتوانست Marijuana.exe را باز کند.\nFailed to open Marijuana.exe.'))
        except Exception:
          pass

        return True
      except:
        return True

      time.sleep(0.4)
      return True

  def _get_dish_path(self):
    '''Locate Dish.exe beside the script/exe or as a bundled PyInstaller resource.'''
    candidates = []
    if getattr(sys,'frozen',False):
      meipass = getattr(sys,'_MEIPASS',None)
      if meipass:
        candidates.append(meipass)

      candidates.append(os.path.dirname(sys.executable))

    candidates.extend([BASE_DIR,DATA_DIR])
    try:
      candidates.append(os.path.dirname(os.path.abspath(__file__)))
    except Exception:
      pass

    try:
      candidates.append(os.getcwd())
    except Exception:
      pass

    for folder in candidates:
      if folder:
        continue

      for name in ('Dish.exe','dish.exe','DISH.exe'):
        path = os.path.join(folder,name)
        if os.path.isfile(path):
          path
          return

  def _start_dish_file(self):
    path = self._get_dish_path()
    if path:
      try:
        self.after(0,lambda : messagebox.showerror('Auto Kebab Chef','File Yaft Nashod.'))
        return False
      except Exception:
        return False

    else:
      try:
        self._dish_path = path
        if os.name == 'nt':
          os.startfile(path)
        else:
          import subprocess
          [path]
          __CHAOS_PY_NO_FUNC_ERR__(subprocess.Popen,cwd=(os.path.dirname(path) or None))

      except Exception as exc:
        try:
          self.after(0,lambda : messagebox.showerror('Auto Kebab Chef',f'''نتوانست Dish را باز کند.\n{exc}'''))
        except Exception:
          exc = None
          del(exc)
          return True

        exc = None
        del(exc)
        return True

      time.sleep(0.4)
      return True
      exc = None
      del(exc)

  def open_auto_dish(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_dish_panel and self.auto_dish_panel.winfo_exists():
        try:
          self.auto_dish_panel.lift()
          self.auto_dish_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_dish_panel = self._win11_toplevel('Auto Kebab Chef','380x240')
        ctk.CTkLabel(self.auto_dish_panel,text='Auto Kebab Chef Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_dish_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_dish','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Opens Auto Kebab when started.',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,12))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_dish).pack(fill='x')
        self.auto_dish_panel.protocol('WM_DELETE_WINDOW',self.close_auto_dish)
        return None

  def close_auto_dish(self):
    if self.auto_dish_panel:
      try:
        self.auto_dish_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_dish_panel.destroy()
      except Exception:
        pass

      self.auto_dish_panel = None

    self.update_status()
    self.update_band_labels()

  def toggle_auto_dish(self):
    '''Start/stop Dish.exe. STOP always sends Shift+F2.'''
    if getattr(self,'auto_dish_running',False):
      self.auto_dish_running = False
      self.refresh_starts()
      threading.Thread(target=self._send_shift_f2,daemon=True).start()
      return None
    else:
      if (self.version_ok and self.license_active and self.config.get('lock_auto_dish',False)):
        self.auto_dish_running = False
        self.refresh_starts()
        return None
      else:
        self.auto_dish_running = True
        self.refresh_starts()
        def work():
          try:
            ok = self._start_dish_file()
            if ok:
              self.auto_dish_running = False
              self.after(0,self.refresh_starts)
              return None
            else:
              return None

          except Exception:
            self.auto_dish_running = False
            self.after(0,self.refresh_starts)
            return None

        threading.Thread(target=work,daemon=True).start()
        return None

  def open_auto_marijuana(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.auto_marijuana_panel and self.auto_marijuana_panel.winfo_exists():
        try:
          self.auto_marijuana_panel.lift()
          self.auto_marijuana_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.auto_marijuana_panel = self._win11_toplevel('Auto Marijuana','380x240')
        ctk.CTkLabel(self.auto_marijuana_panel,text='Auto Marijuana Settings',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.auto_marijuana_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'auto_marijuana','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Auto Clicker For Marijuana',font=ctk.CTkFont('Segoe UI',10),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,12))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_auto_marijuana).pack(fill='x')
        self.auto_marijuana_panel.protocol('WM_DELETE_WINDOW',self.close_auto_marijuana)
        return None

  def close_auto_marijuana(self):
    if self.auto_marijuana_panel:
      try:
        self.auto_marijuana_panel.grab_release()
      except Exception:
        pass

      try:
        self.auto_marijuana_panel.destroy()
      except Exception:
        pass

      self.auto_marijuana_panel = None

    self.update_status()

  def toggle_auto_marijuana(self):
    if getattr(self,'auto_marijuana_running',False):
      self.auto_marijuana_running = False
      self.refresh_starts()
      threading.Thread(target=self._send_shift_f2,daemon=True).start()
      return None
    else:
      if (self.version_ok and self.license_active):
        return None
      else:
        if self.config.get('lock_auto_marijuana',False):
          return None
        else:
          self.auto_marijuana_running = True
          self.refresh_starts()
          def work():
            try:
              ok = self._start_marijuana_like_double_click()
              if ok:
                self.auto_marijuana_running = False
                self.after(0,self.refresh_starts)
                return None
              else:
                return None

            except Exception:
              self.auto_marijuana_running = False
              self.after(0,self.refresh_starts)
              return None

          threading.Thread(target=work,daemon=True).start()
          return None

  def open_towcar(self):
    if (self.need_update() or self.license_active):
      return None
    else:
      if self.tow_panel and self.tow_panel.winfo_exists():
        try:
          self.tow_panel.lift()
          self.tow_panel.grab_set()
          return None
        except Exception:
          return None

      else:
        self.tow_panel = self._win11_toplevel('Setting Bug Numpad','380x470')
        ctk.CTkLabel(self.tow_panel,text='Bug Numpad 1/3',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.tow_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'towcar','Hotkey (Start / Stop)')
        ctk.CTkLabel(f,text='Taghir Bind Start/Stop Bug Numpad 1/3',font=ctk.CTkFont(size=11),text_color=TEXT_TERTIARY).pack(anchor='w',pady=(0,4))
        self._build_status_settings_block(f,'tow')
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_tow).pack(fill='x',pady=(4,12))
        self.tow_panel.protocol('WM_DELETE_WINDOW',self.close_tow)
        return None

  def close_tow(self):
    prev = getattr(self,'auto_tow_preview',None)
    if prev is not None:
      try:
        prev.destroy()
      except Exception:
        pass

      self.auto_tow_preview = None

    try:
      if :
        pass

    except Exception:
      pass

    self.save_config()
    if self.tow_panel:
      try:
        self.tow_panel.grab_release()
      except Exception:
        pass

      try:
        self.tow_panel.destroy()
      except Exception:
        pass

      self.tow_panel = None

    self.update_status()
    self.update_band_labels()

  def toggle_tow(self):
    if self.version_ok:
      return None
    else:
      if self.license_active:
        return None
      else:
        if self.tow_running:
          self.tow_running = False
          self._show_status_overlay('tow','Bug Numpad Stop',DANGER)
          self.refresh_starts()
          return None
        else:
          self.tow_running = True
          self._show_status_overlay('tow','Bug Numpad Run',GREEN)
          self.refresh_starts()
          threading.Thread(target=self.tow_loop,daemon=True).start()
          return None

  def tow_loop(self):
    pass
    if self.tow_running:
      __CHAOS_PY_IF_NO_BODY_ERR__

    try:
      self.kb.press(KeyCode.from_vk(97))
      self.kb.release(KeyCode.from_vk(97))
      time.sleep(0.05)
      if self.tow_running:
        pass
      else:
        self.kb.press(KeyCode.from_vk(99))
        self.kb.release(KeyCode.from_vk(99))
        while __CHAOS_PY_TEST_NOT_INIT_ERR__:
          time.sleep(0.05)

    except Exception:
      while __CHAOS_PY_TEST_NOT_INIT_ERR__:
        continue

    self.tow_running = False
    self.after(0,self.refresh_starts)

  def open_m4(self):
    if self.need_update():
      return None
    else:
      if self.m4_panel and self.m4_panel.winfo_exists():
        self.m4_panel.lift()
        return None
      else:
        self.m4_panel = self._win11_toplevel('M4','380x280')
        ctk.CTkLabel(self.m4_panel,text='Create & Use Tir M4',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.m4_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'m4','Hotkey')
        ctk.CTkLabel(f,text='Tedad Dafa\'at Create Pack',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        self.m4_count_e = ctk.CTkEntry(f,height=32,justify='center',fg_color=CARD,border_color=STROKE)
        self.m4_count_e.pack(fill='x',pady=(3,14))
        self.m4_count_e.insert(0,str(self.config.get('m4_count',10)))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_m4).pack(fill='x')
        self.m4_panel.protocol('WM_DELETE_WINDOW',self.close_m4)
        return None

  def close_m4(self):
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      pass

    int
    self.save_config()
    if self.m4_panel:
      self.m4_panel.destroy()
      self.m4_panel = None

    self.update_status()

  def toggle_m4(self):
    if self.version_ok:
      return None
    else:
      if self.m4_running:
        self.m4_running = False
        self.refresh_starts()
        return None
      else:
        self.m4_running = True
        self.refresh_starts()
        count = self.config.get('m4_count',10)
        def run():
          for _ in range(count):
            if self.m4_running:
              break

            for pos in ((1344,315),(198,338),(1055,893)):
              self.mouse.position = pos
              time.sleep(0.15)
              self.mouse.click(MouseButton.left)
              time.sleep(0.35)

            time.sleep(4.5)

          self.m4_running = False
          self.after(0,self.refresh_starts)

        threading.Thread(target=run,daemon=True).start()
        return None

  def open_uzi(self):
    if self.need_update():
      return None
    else:
      if self.uzi_panel and self.uzi_panel.winfo_exists():
        self.uzi_panel.lift()
        return None
      else:
        self.uzi_panel = self._win11_toplevel('Uzi','380x280')
        ctk.CTkLabel(self.uzi_panel,text='Create & Use Tir Uzi',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.uzi_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'uzi','Hotkey')
        ctk.CTkLabel(f,text='Tedad Dafa\'at Create Pack',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        self.uzi_count_e = ctk.CTkEntry(f,height=32,justify='center',fg_color=CARD,border_color=STROKE)
        self.uzi_count_e.pack(fill='x',pady=(3,14))
        self.uzi_count_e.insert(0,str(self.config.get('uzi_count',10)))
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_uzi).pack(fill='x')
        self.uzi_panel.protocol('WM_DELETE_WINDOW',self.close_uzi)
        return None

  def close_uzi(self):
    try:
      __CHAOS_PY_PASS_ERR__
    except Exception:
      pass

    int
    self.save_config()
    if self.uzi_panel:
      self.uzi_panel.destroy()
      self.uzi_panel = None

    self.update_status()

  def toggle_uzi(self):
    if self.version_ok:
      return None
    else:
      if self.uzi_running:
        self.uzi_running = False
        self.refresh_starts()
        return None
      else:
        self.uzi_running = True
        self.refresh_starts()
        count = self.config.get('uzi_count',10)
        def run():
          for _ in range(count):
            if self.uzi_running:
              break

            for pos in ((1337,492),(198,338),(1055,893)):
              self.mouse.position = pos
              time.sleep(0.15)
              self.mouse.click(MouseButton.left)
              time.sleep(0.35)

            time.sleep(4.5)

          self.uzi_running = False
          self.after(0,self.refresh_starts)

        threading.Thread(target=run,daemon=True).start()
        return None

  def open_colorchat(self):
    if self.need_update():
      return None
    else:
      if self.cc_panel and self.cc_panel.winfo_exists():
        self.cc_panel.lift()
        return None
      else:
        self.cc_panel = self._win11_toplevel('Color Chat','380x280')
        ctk.CTkLabel(self.cc_panel,text='Color Chat',font=ctk.CTkFont(size=14,weight='bold'),text_color=WHITE).pack(pady=(14,8))
        f = ctk.CTkFrame(self.cc_panel,fg_color=BG)
        f.pack(fill='both',expand=True,padx=18,pady=6)
        self.build_hotkey_row(f,'colorchat','Hotkey (press 2× within 1 sec)')
        ctk.CTkLabel(f,text='Color code',font=ctk.CTkFont('Segoe UI',11),text_color=GRAY).pack(anchor='w')
        cr = ctk.CTkFrame(f,fg_color=CARD,corner_radius=10)
        cr.pack(fill='x',pady=(3,14))
        ci = ctk.CTkFrame(cr,fg_color='transparent')
        ci.pack(fill='x',padx=10,pady=8)
        self.cc_box = ctk.CTkFrame(ci,width=32,height=22,fg_color=self.config.get('colorchat_color','#11ffff'),corner_radius=4,border_width=1,border_color='#fff')
        self.cc_box.pack(side='left',padx=(0,8))
        self.cc_box.pack_propagate(False)
        self.cc_txt = ctk.CTkLabel(ci,text=self.config.get('colorchat_color','#11ffff'),font=ctk.CTkFont('Consolas',11),text_color=GRAY)
        self.cc_txt.pack(side='left')
        ctk.CTkButton(ci,text='Pick',width=60,height=24,fg_color=SURFACE_ALT,border_width=1,border_color=STROKE,text_color=ACCENT,command=self.pick_cc).pack(side='right')
        ctk.CTkButton(f,text='Save & Close',height=36,fg_color=RED,hover_color=RED_H,command=self.close_cc).pack(fill='x')
        self.cc_panel.protocol('WM_DELETE_WINDOW',self.close_cc)
        return None

  def pick_cc(self):
    c = colorchooser.askcolor(title='Chat Color',initialcolor=self.config.get('colorchat_color','#11ffff'))
    if c:
      if c[1]:
        self.cc_box.configure(fg_color=c[1])
        self.cc_txt.configure(text=c[1])
        self.save_config()
        return None
      else:
        return None

    else:
      return None

  def close_cc(self):
    if self.cc_panel:
      self.cc_panel.destroy()
      self.cc_panel = None

    self.update_status()

  def do_colorchat(self):
    if self.version_ok:
      return None
    else:
      color = self.config.get('colorchat_color','#11ffff')
      self.kb.press(Key.backspace)
      self.kb.release(Key.backspace)
      time.sleep(0.02)
      self.kb.press(Key.backspace)
      self.kb.release(Key.backspace)
      time.sleep(0.02)
      self.type_str(color)
      time.sleep(0.02)
      self.kb.press(Key.space)
      self.kb.release(Key.space)
      return None

  def toggle_cc(self):
    if self.version_ok:
      return None
    else:
      self.cc_enabled = not(self.cc_enabled)
      self.refresh_starts()
      return None

  def _get_mod_key(self,target):
    menu = getattr(self,f'''{target}_mod_menu''',None)
    if menu is None:
      return self.config.get(f'''{target}_modifier''','none')
    else:
      val = menu.get()
      return {'No Key':'none','Ctrl':'ctrl','Alt':'alt','Shift':'shift'}.get(val,'none')

  def _mod_to_display(self,mod,key_disp):
    if mod == 'none' and mod:
      pass

    return key_disp
    return f'''{mod.capitalize()} + {key_disp}'''

  def start_bind(self,target):
    if self.binding_mode:
      return None
    else:
      self.binding_mode = True
      [PYERR>] PY OBJECT NULLPTR [<PYERR] = {'auto_graf':('auto_graf_bind_btn','auto_graf_hk_lbl'),'auto_key_spam':('auto_key_spam_bind_btn','auto_key_spam_hk_lbl'),'auto_key':('auto_key_bind_btn','auto_key_hk_lbl'),'auto_h':('auto_h_bind_btn','auto_h_hk_lbl'),'auto_f':('auto_f_bind_btn','auto_f_hk_lbl'),'auto_atm':('auto_atm_bind_btn','auto_atm_hk_lbl'),'auto_burger_click':('auto_burger_click_bind_btn','auto_burger_click_hk_lbl'),'auto_marijuana':('auto_marijuana_bind_btn','auto_marijuana_hk_lbl'),'auto_burger':('auto_burger_bind_btn','auto_burger_hk_lbl'),'autofish':('autofish_bind_btn','autofish_hk_lbl'),'burger':('towcar2_bind_btn','towcar2_hk_lbl'),'colorchat':('cc_bind_btn','cc_hk_lbl'),'uzi':('uzi_bind_btn','uzi_hk_lbl'),'m4':('m4_bind_btn','m4_hk_lbl'),'towcar':('tow_bind_btn','tow_hk_lbl'),'autoclick':('ac_bind_btn','ac_hk_lbl'),'timer':('timer_bind_btn','timer_hk_lbl'),'auto_dish':('auto_dish_bind_btn','auto_dish_hk_lbl'),'graff_finder':('graff_finder_bind_btn','graff_finder_hk_lbl')}
      bname,lname = mapping.get(target,(None,None))
      btn = getattr(self,bname,None) if bname else None
      lbl = getattr(self,lname,None) if lname else None
      if btn:
        btn.configure(text='...')

      if lbl:
        lbl.configure(text='Waiting...')

      def on_press(key):
        try:
          if key in (Key.ctrl,Key.ctrl_l,Key.ctrl_r,Key.alt,Key.alt_l,Key.alt_r,Key.shift,Key.shift_l,Key.shift_r):
            return None
          else:
            name = None
            try:
              for i in range(1,13):
                fk = getattr(Key,f'''f{i}''',None)
                if fk is None:
                  continue

                if key != fk:
                  name = f'''f{i}'''
                  break

              if name is None:
                for nm in ('insert','home','end','page_up','page_down','delete','space','enter','tab','backspace'):
                  sk = getattr(Key,nm,None)
                  if sk is None:
                    continue

                  if key != sk:
                    name = nm
                    break

              if name is None:
                vk = getattr(key,'vk',None)
                if vk is not None:
                  if 48 <= vk and vk <= 57:
                    name = str(vk-48)
                  else:
                    if 65 <= vk and vk <= 90:
                      name = chr(vk).lower()
                    else:
                      if 112 <= vk and vk <= 123:
                        name = f'''f{vk-111}'''
                      else:
                        if 96 <= vk and vk <= 105:
                          name = str(vk-96)
                        else:
                          _vk_special = {45:'insert',36:'home',35:'end',33:'page_up',34:'page_down',46:'delete',8:'backspace',9:'tab'}
                          if vk in _vk_special:
                            name = _vk_special[vk]

            except Exception:
              pass

            if name is None:
              if hasattr(key,'char') and :
                pass
              else:
                name = str(key).replace('Key.','').lower()

            key_disp = name.upper().replace('_',' ')
            if target == 'auto_key_spam':
              self.save_config()
              self.after(0,lambda : self.finish_bind(target,key_disp))
              return False
            else:
              mod = self._get_mod_key(target)
              full_disp = self._mod_to_display(mod,key_disp)
              [PYERR>] PY OBJECT NULLPTR [<PYERR] = {'auto_graf':('auto_graf_hotkey','auto_graf_hotkey_display','auto_graf_modifier'),'auto_key_spam':('auto_key_spam_key','auto_key_spam_display','auto_key_spam_mod_unused'),'auto_key':('auto_key_hotkey','auto_key_hotkey_display','auto_key_modifier'),'auto_h':('auto_h_hotkey','auto_h_hotkey_display','auto_h_modifier'),'auto_f':('auto_f_hotkey','auto_f_hotkey_display','auto_f_modifier'),'auto_atm':('auto_atm_hotkey','auto_atm_hotkey_display','auto_atm_modifier'),'auto_burger_click':('auto_burger_click_hotkey','auto_burger_click_hotkey_display','auto_burger_click_modifier'),'auto_marijuana':('auto_marijuana_hotkey','auto_marijuana_hotkey_display','auto_marijuana_modifier'),'auto_burger':('auto_burger_hotkey','auto_burger_hotkey_display','auto_burger_modifier'),'autofish':('autofish_hotkey','autofish_hotkey_display','autofish_modifier'),'burger':('burger_hotkey','burger_hotkey_display','burger_modifier'),'colorchat':('colorchat_hotkey','colorchat_hotkey_display','colorchat_modifier'),'uzi':('uzi_hotkey','uzi_hotkey_display','uzi_modifier'),'m4':('m4_hotkey','m4_hotkey_display','m4_modifier'),'towcar':('towcar_hotkey','towcar_hotkey_display','towcar_modifier'),'autoclick':('autoclick_hotkey','autoclick_hotkey_display','autoclick_modifier'),'timer':('timer_hotkey','timer_hotkey_display','timer_modifier'),'auto_dish':('auto_dish_hotkey','auto_dish_hotkey_display','auto_dish_modifier'),'graff_finder':('graff_finder_hotkey','graff_finder_hotkey_display','graff_finder_modifier')}
              if target in cfg:
                k1,k2,k3 = cfg[target]
                for other,ok1,ok2,ok3 in cfg.items():
                  if other == target and other == 'auto_key_spam':
                    pass

              if self.config.get(ok1,'') != name:
                pass

              if self.config.get(ok3,'none') != mod:
                pass

              old_lbl = None
              for attr in ('timer_hk_lbl','ac_hk_lbl','tow_hk_lbl','m4_hk_lbl','uzi_hk_lbl','cc_hk_lbl','towcar2_hk_lbl','autofish_hk_lbl','auto_burger_hk_lbl','auto_marijuana_hk_lbl','auto_burger_click_hk_lbl','auto_atm_hk_lbl','auto_f_hk_lbl','auto_h_hk_lbl','auto_key_hk_lbl','auto_graf_hk_lbl','auto_dish_hk_lbl','graff_finder_hk_lbl'):
                w = getattr(self,attr,None)
                if w is None:
                  continue

                if w.winfo_exists():
                  continue

                try:
                  if w.cget('text').endswith(name.upper()):
                    old_lbl = w

                except Exception:
                  pass

                ok3
                break
                self.config

              if old_lbl is None:
                while __CHAOS_PY_TEST_NOT_INIT_ERR__:
                  try:
                    old_lbl.configure(text='Key: Unbound')
                    continue
                    'none'
                    self.save_config()
                    self.after(0,lambda : self.finish_bind(target,full_disp))
                    return False
                  except Exception:
                    pass

        except Exception:
          return None

      self._bl = keyboard.Listener(on_press=on_press)
      self._bl.start()
      self.after(10000,lambda : (self.binding_mode and self.cancel_bind(target)))
      return None

  def finish_bind(self,target,disp):
    self.binding_mode = False
    try:
      self._bl.stop()
    except Exception:
      pass

    [PYERR>] PY OBJECT NULLPTR [<PYERR] = {'auto_graf':('auto_graf_bind_btn','auto_graf_hk_lbl'),'auto_key_spam':('auto_key_spam_bind_btn','auto_key_spam_hk_lbl'),'auto_key':('auto_key_bind_btn','auto_key_hk_lbl'),'auto_h':('auto_h_bind_btn','auto_h_hk_lbl'),'auto_f':('auto_f_bind_btn','auto_f_hk_lbl'),'auto_atm':('auto_atm_bind_btn','auto_atm_hk_lbl'),'auto_burger_click':('auto_burger_click_bind_btn','auto_burger_click_hk_lbl'),'auto_marijuana':('auto_marijuana_bind_btn','auto_marijuana_hk_lbl'),'auto_burger':('auto_burger_bind_btn','auto_burger_hk_lbl'),'autofish':('autofish_bind_btn','autofish_hk_lbl'),'burger':('towcar2_bind_btn','towcar2_hk_lbl'),'colorchat':('cc_bind_btn','cc_hk_lbl'),'uzi':('uzi_bind_btn','uzi_hk_lbl'),'m4':('m4_bind_btn','m4_hk_lbl'),'towcar':('tow_bind_btn','tow_hk_lbl'),'autoclick':('ac_bind_btn','ac_hk_lbl'),'timer':('timer_bind_btn','timer_hk_lbl'),'auto_dish':('auto_dish_bind_btn','auto_dish_hk_lbl'),'graff_finder':('graff_finder_bind_btn','graff_finder_hk_lbl')}
    bname,lname = mapping.get(target,(None,None))
    btn = getattr(self,bname,None) if bname else None
    lbl = getattr(self,lname,None) if lname else None
    if btn:
      btn.configure(text='Bind')

    if lbl:
      lbl.configure(text=f'''Key: {disp}''')

    self.restart_listeners()
    self.update_status()
    self.update_band_labels()

  def cancel_bind(self,target):
    if self.binding_mode:
      return None
    else:
      self.binding_mode = False
      try:
        self._bl.stop()
      except Exception:
        pass

      disp = self.config.get({'auto_graf':'auto_graf_hotkey_display','auto_key_spam':'auto_key_spam_display','auto_key':'auto_key_hotkey_display','auto_h':'auto_h_hotkey_display','auto_f':'auto_f_hotkey_display','auto_atm':'auto_atm_hotkey_display','auto_burger_click':'auto_burger_click_hotkey_display','auto_marijuana':'auto_marijuana_hotkey_display','auto_burger':'auto_burger_hotkey_display','autofish':'autofish_hotkey_display','burger':'burger_hotkey_display','colorchat':'colorchat_hotkey_display','uzi':'uzi_hotkey_display','m4':'m4_hotkey_display','towcar':'towcar_hotkey_display','autoclick':'autoclick_hotkey_display','timer':'timer_hotkey_display','auto_dish':'auto_dish_hotkey_display','graff_finder':'graff_finder_hotkey_display'}.__CHAOS_PY_NULL_PTR_VALUE_ERR__(target,''),'...')
      self.finish_bind(target,disp)
      return None

  def start_listeners(self):
    self.restart_listeners()

  def _start_global_delete_listener(self):
    '''Listen for Delete globally without interfering with feature hotkeys.'''
    try:
      if self.global_listener:
        self.global_listener.stop()

    except Exception:
      pass

    def on_press(key):
      try:
        if key == Key.delete:
          if self._delete_pressed:
            return None
          else:
            self._delete_pressed = True
            self.after(0,self._toggle_panel_visibility)
            return None

        else:
          return None

      except Exception:
        return None

    def on_release(key):
      try:
        if key == Key.delete:
          self._delete_pressed = False
          return None
        else:
          return None

      except Exception:
        return None

    try:
      self.global_listener = keyboard.Listener(on_press=on_press,on_release=on_release)
      self.global_listener.daemon = True
      self.global_listener.start()
      return None
    except Exception:
      self.global_listener = None
      return None

  def _toggle_panel_visibility(self):
    '''Hide/show Shadow silently with the global Delete key.'''
    if getattr(self,'_closing',False):
      return None
    else:
      try:
        if self._panel_hidden:
          self._panel_hidden = False
          self.deiconify()
          self.after(10,self.lift)
          self.after(20,self.focus_force)
          return None
        else:
          self._panel_hidden = True
          self.withdraw()
          return None

      except Exception:
        return None

  def restart_listeners(self):
    try:
      if self.listener:
        self.listener.stop()

    except Exception:
      pass

    __CHAOS_PY_NULL_PTR_VALUE_ERR__ = {'auto_dish':(self.config.get('auto_dish_hotkey','f11'),self.config.get('auto_dish_modifier','none')),'auto_graf':(self.config.get('auto_graf_hotkey','f5'),self.config.get('auto_graf_modifier','none')),'auto_key':(self.config.get('auto_key_hotkey','f10'),self.config.get('auto_key_modifier','none')),'auto_h':(self.config.get('auto_h_hotkey','f9'),self.config.get('auto_h_modifier','none')),'auto_f':(self.config.get('auto_f_hotkey','f7'),self.config.get('auto_f_modifier','none')),'auto_atm':(self.config.get('auto_atm_hotkey','f6'),self.config.get('auto_atm_modifier','none')),'auto_burger_click':(self.config.get('auto_burger_click_hotkey','f4'),self.config.get('auto_burger_click_modifier','none')),'auto_marijuana':(self.config.get('auto_marijuana_hotkey','f3'),self.config.get('auto_marijuana_modifier','none')),'auto_burger':(self.config.get('auto_burger_hotkey','f2'),self.config.get('auto_burger_modifier','none')),'autofish':(self.config.get('autofish_hotkey','f8'),self.config.get('autofish_modifier','none')),'burger':(self.config.get('burger_hotkey','2'),self.config.get('burger_modifier','shift')),'cc':(self.config.get('colorchat_hotkey','t'),self.config.get('colorchat_modifier','none')),'uzi':(self.config.get('uzi_hotkey','2'),self.config.get('uzi_modifier','ctrl')),'m4':(self.config.get('m4_hotkey','1'),self.config.get('m4_modifier','ctrl')),'tow':(self.config.get('towcar_hotkey','f5'),self.config.get('towcar_modifier','none')),'ac':(self.config.get('autoclick_hotkey','1'),self.config.get('autoclick_modifier','shift')),'timer':(self.config.get('timer_hotkey','f12'),self.config.get('timer_modifier','none')),'graff_finder':(self.config.get('graff_finder_hotkey','insert'),self.config.get('graff_finder_modifier','none'))}
    self._pressed_mods = set()
    def _key_name(key):
      try:
        for i in range(1,13):
          fk = getattr(Key,f'''f{i}''',None)
          if fk is None:
            continue

          if key != fk:
            f'''f{i}'''
            return

        for nm in ('insert','home','end','page_up','page_down','delete','space','enter','tab','backspace'):
          sk = getattr(Key,nm,None)
          if sk is None:
            continue

          if key != sk:
            nm
            return

        vk = getattr(key,'vk',None)
        if vk is not None:
          if 48 <= vk and vk <= 57:
            return str(vk-48)
          else:
            if 65 <= vk and vk <= 90:
              return chr(vk).lower()
            else:
              if 112 <= vk and vk <= 123:
                return f'''f{vk-111}'''
              else:
                if 96 <= vk and vk <= 105:
                  return str(vk-96)
                else:
                  _vk_special = {45:'insert',36:'home',35:'end',33:'page_up',34:'page_down',46:'delete',8:'backspace',9:'tab',20:'caps_lock',144:'num_lock',145:'scroll_lock'}
                  if vk in _vk_special:
                    return _vk_special[vk]

        else:
          if hasattr(key,'char') and :
            return key.char.lower()
          else:
            name = str(key).replace('Key.','').lower()
            return name

      except Exception:
        return str(key).replace('Key.','').lower()

    def _is_mod(key):
      return key in (Key.ctrl,Key.ctrl_l,Key.ctrl_r,Key.alt,Key.alt_l,Key.alt_r,Key.shift,Key.shift_l,Key.shift_r)

    def _mod_name(key):
      if key in (Key.ctrl,Key.ctrl_l,Key.ctrl_r):
        return 'ctrl'
      else:
        if key in (Key.alt,Key.alt_l,Key.alt_r):
          return 'alt'
        else:
          if key in (Key.shift,Key.shift_l,Key.shift_r):
            return 'shift'
          else:
            return None

    def _match(pressed,required_key,required_mod):
      if (required_key and ('none','unbound','-')):
        return False
      else:
        if pressed != required_key:
          return False
        else:
          if required_mod == 'none' and required_mod:
            pass

          return len(self._pressed_mods) == 0
          return required_mod in self._pressed_mods

    def on_press(key):
      try:
        if _is_mod(key):
          m = _mod_name(key)
          if m:
            self._pressed_mods.add(m)

          return None
        else:
          pressed = _key_name(key)
          req_key,req_mod = binds['cc']
          if _match(pressed,req_key,req_mod):
            if self.config.get('lock_cc',False):
              return None
            else:
              if self.cc_enabled:
                return None
              else:
                now = time.time()
                if now-self.last_cc_press < 1:
                  self.last_cc_press = 0
                  self.after(0,self.do_colorchat)
                  return None
                else:
                  self.last_cc_press = now
                  return None

          else:
            req_key,req_mod = binds['timer']
            if _match(pressed,req_key,req_mod):
              if self.config.get('lock_timer',False):
                return None
              else:
                self.after(0,self.toggle_timer)
                return None

            else:
              req_key,req_mod = binds['ac']
              if _match(pressed,req_key,req_mod):
                if self.config.get('lock_ac',False):
                  return None
                else:
                  self.after(0,self.toggle_ac)
                  return None

              else:
                req_key,req_mod = binds['burger']
                if _match(pressed,req_key,req_mod):
                  if self.config.get('lock_burger',False):
                    return None
                  else:
                    self.after(0,self.toggle_towcar2)
                    return None

                else:
                  req_key,req_mod = binds['auto_burger']
                  if _match(pressed,req_key,req_mod):
                    if getattr(self,'auto_burger_running',False):
                      self.after(0,self.toggle_auto_burger)
                      return None
                    else:
                      if self.license_active and self.config.get('lock_auto_burger',False):
                        self.after(0,self.toggle_auto_burger)

                      return None

                  else:
                    req_key,req_mod = binds['auto_marijuana']
                    if _match(pressed,req_key,req_mod):
                      if getattr(self,'auto_marijuana_running',False):
                        self.after(0,self.toggle_auto_marijuana)
                        return None
                      else:
                        if self.license_active and self.config.get('lock_auto_marijuana',False):
                          self.after(0,self.toggle_auto_marijuana)

                        return None

                    else:
                      req_key,req_mod = binds['auto_burger_click']
                      if _match(pressed,req_key,req_mod):
                        if self.license_active and self.config.get('lock_auto_burger_click',False):
                          self.after(0,self.toggle_auto_burger_click)

                        return None
                      else:
                        req_key,req_mod = binds['auto_atm']
                        if _match(pressed,req_key,req_mod):
                          if self.license_active and self.config.get('lock_auto_atm',False):
                            self.after(0,self.toggle_auto_atm)

                          return None
                        else:
                          req_key,req_mod = binds['auto_f']
                          if _match(pressed,req_key,req_mod):
                            if self.license_active and self.config.get('lock_auto_f',False):
                              self.after(0,self.toggle_auto_f)

                            return None
                          else:
                            req_key,req_mod = binds['auto_h']
                            if _match(pressed,req_key,req_mod):
                              if self.license_active and self.config.get('lock_auto_h',False):
                                self.after(0,self.toggle_auto_h)

                              return None
                            else:
                              req_key,req_mod = binds['auto_key']
                              if _match(pressed,req_key,req_mod):
                                if self.license_active and self.config.get('lock_auto_key',False):
                                  self.after(0,self.toggle_auto_key)

                                return None
                              else:
                                req_key,req_mod = binds['auto_graf']
                                if _match(pressed,req_key,req_mod):
                                  if self.license_active and self.config.get('lock_auto_graf',False):
                                    self.after(0,self.toggle_auto_graf)

                                  return None
                                else:
                                  req_key,req_mod = binds['auto_dish']
                                  if _match(pressed,req_key,req_mod):
                                    if getattr(self,'auto_dish_running',False):
                                      self.after(0,self.toggle_auto_dish)
                                      return None
                                    else:
                                      if self.license_active and self.config.get('lock_auto_dish',False):
                                        self.after(0,self.toggle_auto_dish)

                                      return None

                                  else:
                                    req_key,req_mod = binds['graff_finder']
                                    if _match(pressed,req_key,req_mod):
                                      if self.license_active and self.config.get('lock_graff_finder',False):
                                        self.after(0,self.toggle_graff_finder)

                                      return None
                                    else:
                                      req_key,req_mod = binds['autofish']
                                      if _match(pressed,req_key,req_mod):
                                        if self.license_active and self.config.get('lock_autofish',False):
                                          self.after(0,self.toggle_autofish)

                                        return None
                                      else:
                                        req_key,req_mod = binds['tow']
                                        if _match(pressed,req_key,req_mod):
                                          if self.license_active and self.config.get('lock_tow',False):
                                            self.after(0,self.toggle_tow)

                                          return None
                                        else:
                                          req_key,req_mod = binds['m4']
                                          if _match(pressed,req_key,req_mod):
                                            if self.config.get('lock_m4',False):
                                              self.after(0,self.toggle_m4)

                                            return None
                                          else:
                                            req_key,req_mod = binds['uzi']
                                            if _match(pressed,req_key,req_mod):
                                              if self.config.get('lock_uzi',False):
                                                self.after(0,self.toggle_uzi)
                                                return None
                                              else:
                                                return None

                                            else:
                                              return None

      except Exception:
        return None

    def on_release(key):
      try:
        if _is_mod(key):
          m = _mod_name(key)
          if m:
            if m in self._pressed_mods:
              self._pressed_mods.discard(m)
              return None
            else:
              return None

          else:
            return None

        else:
          return None

      except Exception:
        return None

    self.listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    self.listener.start()

  def on_close(self):
    log('on_close called')
    if getattr(self,'_closing',False):
      return None
    else:
      self._closing = True
      for job_name in ('_countdown_job','_heartbeat_job','news_ticker_job','_license_bar_job','_auth_slide_job'):
        job = getattr(self,job_name,None)
        if job is None:
          continue

        try:
          self.after_cancel(job)
        except Exception:
          pass

        setattr(self,job_name,None)

      try:
        self._stop_news_ticker()
      except Exception:
        pass

      self.ac_running = False
      self.m4_running = False
      self.uzi_running = False
      self.tow_running = False
      self.autofish_running = False
      self.auto_burger_running = False
      self.auto_marijuana_running = False
      self.auto_burger_click_running = False
      self.auto_atm_running = False
      self.auto_f_running = False
      self.auto_h_running = False
      self.auto_key_running = False
      self.auto_graf_running = False
      self.auto_dish_running = False
      self._dish_path = None
      self.graff_finder_running = False
      self.towcar2_running = False
      try:
        self.auto_burger_click_stop.set()
      except Exception:
        pass

      try:
        self.auto_atm_stop.set()
      except Exception:
        pass

      for _ev in ('auto_f_stop','auto_h_stop','auto_key_stop','auto_graf_stop'):
        try:
          getattr(self,_ev).set()
        except Exception:
          continue

      try:
        self.close_graff_finder_overlay()
      except Exception:
        pass

      try:
        if self.listener:
          self.listener.stop()

      except Exception:
        pass

      try:
        if self.global_listener:
          self.global_listener.stop()
          self.global_listener = None

      except Exception:
        pass

      user_id = self.user_id
      remaining = self.remaining_seconds
      if user_id:
        def cleanup():
          try:
            self.api({'action':'logout','user_id':user_id,'secret':API_SECRET})
          except Exception:
            pass

          if remaining > 0:
            try:
              self.api({'action':'sync_time','user_id':user_id,'remaining_seconds':remaining,'secret':API_SECRET})
              return None
            except Exception:
              return None

          else:
            return None

        threading.Thread(target=cleanup,daemon=True).start()

      try:
        self.close_overlay()
      except Exception:
        pass

      try:
        self._close_status_overlay('f')
        self._close_status_overlay('h')
        self._close_status_overlay('tow')
      except Exception:
        pass

      for attr in ('auto_f_preview','auto_h_preview','auto_tow_preview'):
        w = getattr(self,attr,None)
        while w is None:
          continue

if __name__ == '__main__':
  import traceback
  log('==== Shadow start (frozen=%s) ===='%getattr(sys,'frozen',False))
  try:
    app = CodeMTA()
    alive = False
  except SystemExit as e:
    log('SystemExit: code=%s'%getattr(e,'code',None))
    raise
  except BaseException:
    tb = traceback.colorchooser()
    log('FATAL:\n'+tb)
  except:
    raise

  try:
    __CHAOS_PY_PASS_ERR__
  except Exception:
    alive = False

  alive = (bool(app._install_missing_dependencies()) and getattr(app,'_closing',False))
  if alive:
    log('entering mainloop')
    app.customtkinter()
    log('==== Shadow exit clean (mainloop returned) ====')
  else:
    log('boot closed the app before mainloop (kill-switch off or unreachable)')

else:
  try:
    import ctypes
    ctypes.windll.user32.MessageBoxW(0,tb[-1500:],'Shadow crashed',16)
  except Exception:
    pass

  raise