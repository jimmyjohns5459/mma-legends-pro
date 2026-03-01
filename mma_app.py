"""
MMA Legends Pro — Mobile App
Kivy wrapper that runs the terminal game in a thread and displays it
on a touch-friendly screen. Packages to Android APK via Buildozer.
"""

# ═══════════════════════════════════════════════════════════════════════════
#  I/O BRIDGE — patch builtins BEFORE the game module is imported so every
#  print() / input() / os.system('cls') in the game goes through our queues.
# ═══════════════════════════════════════════════════════════════════════════
import sys, os, re, pathlib, builtins, threading, queue as _queue

_out_q  = _queue.Queue()   # game → UI
_in_q   = _queue.Queue()   # UI  → game
_CLEAR  = '\x00CLR\x00'    # sentinel: clear the terminal widget

# ── Patch print ──────────────────────────────────────────────────────────────
_orig_print = builtins.print
def _app_print(*args, sep=' ', end='\n', file=None, flush=False):
    # Let stderr through normally; redirect everything else
    if file is not None and file not in (sys.stdout, sys.__stdout__, None):
        _orig_print(*args, sep=sep, end=end, file=file, flush=flush)
        return
    _out_q.put(sep.join(str(a) for a in args) + end)
builtins.print = _app_print

# ── Patch input ──────────────────────────────────────────────────────────────
def _app_input(prompt=''):
    if prompt:
        _out_q.put(str(prompt))
    return _in_q.get()          # blocks until UI sends something
builtins.input = _app_input

# ── Patch os.system (used by clear_screen / ANSI init) ───────────────────────
_orig_os_sys = os.system
def _app_os_sys(cmd):
    if cmd in ('cls', 'clear', ''):
        if cmd in ('cls', 'clear'):
            _out_q.put(_CLEAR)
        return 0
    return _orig_os_sys(cmd)
os.system = _app_os_sys

# ═══════════════════════════════════════════════════════════════════════════
#  IMPORT GAME MODULE (I/O already redirected at this point)
# ═══════════════════════════════════════════════════════════════════════════
try:
    import mma_manager_pro as _g
    _GAME_OK = True
except Exception as _e:
    _GAME_OK = False
    _GAME_ERR = str(_e)

# ── Override clear_screen and _save_path in the game module ──────────────────
if _GAME_OK:
    _g.clear_screen = lambda: _out_q.put(_CLEAR)

    def _android_save_path():
        try:
            from kivy.app import App
            app = App.get_running_app()
            if app:
                return pathlib.Path(app.user_data_dir) / "mma_save.pkl"
        except Exception:
            pass
        return pathlib.Path(".") / "mma_save.pkl"

    _g._save_path = _android_save_path

# ═══════════════════════════════════════════════════════════════════════════
#  ANSI → KIVY MARKUP CONVERTER
# ═══════════════════════════════════════════════════════════════════════════
_ANSI_SPLIT = re.compile(r'\033\[([0-9;]*)m')

_ANSI_MAP = {
    '91': ('color', 'ff5555'),   # red
    '92': ('color', '55dd55'),   # green
    '93': ('color', 'ffff44'),   # yellow
    '94': ('color', '5599ff'),   # blue
    '95': ('color', 'ff55ff'),   # magenta
    '96': ('color', '44ffff'),   # cyan
    '97': ('color', 'ffffff'),   # white
    '2':  ('color', '888888'),   # dim
    '1':  ('b',     None),       # bold
}

def _ansi_to_markup(text):
    """Convert ANSI escape codes to Kivy [color=...] markup."""
    parts = _ANSI_SPLIT.split(text)   # even=literal, odd=code
    result = []
    open_tags = []

    for i, part in enumerate(parts):
        if i % 2 == 0:                        # literal text
            s = part.replace('&', '&amp;')    # escape & first
            s = s.replace('[', '[lb]')         # escape [ for Kivy
            s = s.replace(']', '[rb]')         # escape ]
            result.append(s)
        else:                                  # ANSI code(s)
            for code in (part.split(';') if part else ['0']):
                if code in ('0', ''):          # reset
                    for tag in reversed(open_tags):
                        result.append(f'[/{tag}]')
                    open_tags = []
                elif code in _ANSI_MAP:
                    tag_type, value = _ANSI_MAP[code]
                    if value:
                        result.append(f'[{tag_type}={value}]')
                    else:
                        result.append(f'[{tag_type}]')
                    open_tags.append(tag_type)

    for tag in reversed(open_tags):
        result.append(f'[/{tag}]')
    return ''.join(result)

# ═══════════════════════════════════════════════════════════════════════════
#  CONTEXT-SENSITIVE BUTTON SETS
#  Each entry: (value_sent_to_game, display_label)
# ═══════════════════════════════════════════════════════════════════════════
_BTN_SETS = {
    'title': [
        ('N','▶ New Game'), ('L','◈ Load Save'), ('X','✕ Exit'),
    ],
    'main': [
        ('1','My Gym'),('2','Rankings'),('3','Records'),('4','Recruit'),
        ('5','Advance Wk'),('C','Camp'),('S','Save'),('7','Cheats'),('6','Exit'),
    ],
    'weight': [
        ('1','Flyweight'),('2','Bantam'),('3','Feather'),('4','Light'),
        ('5','Welter'),('6','Middle'),('7','Light HW'),('8','Heavy'),
        ('b','◀ Back'),
    ],
    'style': [
        ('1','Striker'),('2','Grappler'),('3','Brawler'),('4','Balanced'),
        ('b','◀ Back'),
    ],
    'mentality': [
        ('1','Aggressive'),('2','Technical'),('3','Explosive'),
        ('4','Calculated'),('5','Wild'),('6','Composed'),
        ('b','◀ Back'),
    ],
    'camp': [
        ('S','Striking'),('G','Grappling'),('D','Defense'),('C','Cardio'),
        ('P','Power'),('T','Toughness'),('W','Sparring'),('R','Rest'),
        ('B','✔ Done'),
    ],
    'cheats': [
        ('1','$500K'),('2','$2M'),('3','$10M'),
        ('4','Max Stats'),('5','Max Fame'),('6','+10 Wins'),
        ('7','Streak +5'),('8','Champ'),('9','Skip Camp'),
        ('G','God Mode'),('K','Mega Boost'),('R','Reset Save'),('B','◀ Back'),
    ],
    'rankings': [
        ('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
        ('6','6'),('7','7'),('8','8'),('0','Champ'),('b','◀ Back'),
    ],
    'fighter_profile': [
        ('F','Book Fight'),('C','Camp'),('B','◀ Back'),
    ],
    'matchmaking': [
        ('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
        ('6','6'),('7','7'),('8','8'),('9','9'),('b','◀ Back'),
    ],
    'recruit': [
        ('1','Sign #1'),('2','Sign #2'),('3','Sign #3'),('b','◀ Back'),
    ],
    'gym': [
        ('1','Fighter 1'),('2','Fighter 2'),('3','Fighter 3'),
        ('4','Fighter 4'),('5','Fighter 5'),('b','◀ Back'),
    ],
    'yesno': [
        ('Y','✔ YES'), ('N','✕ NO'),
    ],
    'confirm_yes': [
        ('YES','✔ Confirm YES'), ('b','✕ Cancel'),
    ],
    'continue': [
        ('','⬛  Continue / Enter'),
    ],
    'default': [
        ('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
        ('6','6'),('7','7'),('8','8'),('b','◀ Back'),('','↵ Enter'),
    ],
}

def _detect_ctx(text):
    """Heuristically detect which game screen is showing."""
    r = text[-800:] if len(text) > 800 else text
    if ('MMA LEGENDS PRO' in r or 'Load Save' in r or 'No save file' in r) and \
       ('New Game' in r or 'New Career' in r):
        return 'title'
    if 'ADVANCE WEEK' in r and 'MY GYM' in r:
        return 'main'
    if 'WEIGHT CLASS' in r and ('Flyweight' in r or 'Bantamweight' in r):
        return 'weight'
    if 'FIGHTING STYLE' in r and 'Striker' in r and 'Grappler' in r:
        return 'style'
    if 'MENTALITY' in r and 'Aggressive' in r:
        return 'mentality'
    if 'TRAINING DRILLS' in r and 'Camp Stamina' in r:
        return 'camp'
    if 'CHEAT CODES' in r:
        return 'cheats'
    if 'Global Rankings' in r.upper() or ('Rankings' in r and '#1' in r and '#5' in r):
        return 'rankings'
    if 'MATCHMAKING' in r or 'Book fight for' in r:
        return 'matchmaking'
    if 'SCOUTING' in r and 'Sign recruit' in r:
        return 'recruit'
    if 'YOUR GYM' in r and 'Select fighter' in r:
        return 'gym'
    if 'Book a Fight' in r and 'Camp Training' in r:
        return 'fighter_profile'
    if 'Save before exit' in r or ('YES' in r and 'NO' in r and 'exit' in r.lower()):
        return 'yesno'
    if "Type 'YES' to confirm" in r or "Type YES" in r:
        return 'confirm_yes'
    if ('Press ENTER' in r or 'press Enter' in r or 'start round' in r
            or 'WINNER:' in r or 'JUDGES SCORECARD' in r
            or 'begin your career' in r or 'start the fight' in r):
        return 'continue'
    return 'default'

# ═══════════════════════════════════════════════════════════════════════════
#  KIVY IMPORTS & THEME
# ═══════════════════════════════════════════════════════════════════════════
os.environ.setdefault('KIVY_NO_ENV_CONFIG', '1')
os.environ.setdefault('KIVY_NO_CONSOLELOG', '1')

from kivy.app              import App
from kivy.uix.boxlayout    import BoxLayout
from kivy.uix.scrollview   import ScrollView
from kivy.uix.label        import Label
from kivy.uix.textinput    import TextInput
from kivy.uix.button       import Button
from kivy.uix.gridlayout   import GridLayout
from kivy.uix.widget       import Widget
from kivy.clock            import Clock
from kivy.core.window      import Window
from kivy.metrics          import dp
from kivy.graphics         import Color, Rectangle

# Colour palette
_C_BG_DARK  = (0.04, 0.04, 0.06, 1)
_C_BG_HDR   = (0.08, 0.07, 0.03, 1)
_C_GOLD     = (1.00, 0.85, 0.15, 1)
_C_BTN_BG   = (0.10, 0.10, 0.13, 1)
_C_BTN_PRS  = (0.22, 0.18, 0.04, 1)
_C_TEXT     = (0.92, 0.92, 0.92, 1)
_C_DIM      = (0.50, 0.50, 0.50, 1)

Window.clearcolor = _C_BG_DARK


def _bg_widget(color):
    """Create a Widget with a solid background colour."""
    w = Widget()
    with w.canvas.before:
        Color(*color)
        rect = Rectangle(pos=w.pos, size=w.size)
    w.bind(pos=lambda obj, v: setattr(rect, 'pos', v),
           size=lambda obj, v: setattr(rect, 'size', v))
    return w


class _StyledButton(Button):
    def __init__(self, label, value, cb, **kw):
        super().__init__(
            text=label,
            bold=True,
            font_size=kw.pop('font_size', dp(11)),
            color=_C_GOLD,
            background_normal='',
            background_color=_C_BTN_BG,
            **kw,
        )
        self._value = value
        self._cb    = cb
        self.bind(on_press=self._fired)

    def _fired(self, *_):
        self._cb(self._value)


# ═══════════════════════════════════════════════════════════════════════════
#  TERMINAL VIEW  (the main game screen)
# ═══════════════════════════════════════════════════════════════════════════
class TerminalView(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation='vertical', spacing=0, **kw)
        self._lines   = []
        self._ctx     = 'title'
        self._raw_txt = ''

        # ── Header bar ────────────────────────────────────────────────────
        hdr = BoxLayout(
            size_hint=(1, None), height=dp(42),
            padding=(dp(10), dp(6)),
        )
        with hdr.canvas.before:
            Color(*_C_BG_HDR)
            _r = Rectangle(pos=hdr.pos, size=hdr.size)
        hdr.bind(pos=lambda o, v: setattr(_r, 'pos', v),
                 size=lambda o, v: setattr(_r, 'size', v))

        self._hdr_lbl = Label(
            text='[b][color=ffcc00] ★  MMA LEGENDS PRO  ★ [/color][/b]',
            markup=True, font_size=dp(15), halign='center',
        )
        hdr.add_widget(self._hdr_lbl)
        self.add_widget(hdr)

        # ── Terminal scrollview ───────────────────────────────────────────
        self._scroll = ScrollView(
            size_hint=(1, 1), do_scroll_x=False,
            bar_width=dp(4), bar_color=_C_GOLD,
        )
        self._term = Label(
            text='', markup=True,
            halign='left', valign='top',
            font_size=dp(10.5),
            color=_C_TEXT,
            size_hint=(1, None),
            padding=(dp(5), dp(5)),
        )
        self._term.bind(texture_size=self._term.setter('size'))
        self._scroll.add_widget(self._term)
        self.add_widget(self._scroll)

        # ── Context button grid ───────────────────────────────────────────
        self._btn_grid = GridLayout(
            cols=4, size_hint=(1, None), height=dp(104),
            spacing=dp(2), padding=(dp(2), dp(2)),
        )
        with self._btn_grid.canvas.before:
            Color(0.07, 0.07, 0.09, 1)
            _r2 = Rectangle(pos=self._btn_grid.pos, size=self._btn_grid.size)
        self._btn_grid.bind(
            pos=lambda o, v: setattr(_r2, 'pos', v),
            size=lambda o, v: setattr(_r2, 'size', v),
        )
        self.add_widget(self._btn_grid)

        # ── Input bar ─────────────────────────────────────────────────────
        ibar = BoxLayout(
            size_hint=(1, None), height=dp(52),
            spacing=dp(4), padding=(dp(6), dp(7)),
        )
        with ibar.canvas.before:
            Color(0.06, 0.06, 0.08, 1)
            _r3 = Rectangle(pos=ibar.pos, size=ibar.size)
        ibar.bind(pos=lambda o, v: setattr(_r3, 'pos', v),
                  size=lambda o, v: setattr(_r3, 'size', v))

        self._txt_in = TextInput(
            multiline=False,
            font_size=dp(14),
            size_hint=(1, None), height=dp(38),
            background_color=(0.09, 0.09, 0.12, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 0.85, 0.15, 1),
            hint_text='type here or use buttons above',
            hint_text_color=(0.35, 0.35, 0.35, 1),
            padding=(dp(8), dp(8)),
        )
        self._txt_in.bind(on_text_validate=lambda x: self._send(self._txt_in.text))

        _send_btn = Button(
            text='▶',
            bold=True, font_size=dp(18),
            size_hint=(None, None), width=dp(50), height=dp(38),
            background_normal='', background_color=(0.75, 0.55, 0.05, 1),
            color=(0, 0, 0, 1),
        )
        _send_btn.bind(on_press=lambda x: self._send(self._txt_in.text))

        ibar.add_widget(self._txt_in)
        ibar.add_widget(_send_btn)
        self.add_widget(ibar)

        # ── Bind window resize ────────────────────────────────────────────
        Window.bind(size=self._on_win_resize)
        self._on_win_resize(Window, Window.size)

        # ── Build initial buttons & start update loop ─────────────────────
        self._rebuild_buttons()
        Clock.schedule_interval(self._update, 0.1)

    # ── Helpers ───────────────────────────────────────────────────────────
    def _on_win_resize(self, win, size):
        self._term.text_size = (size[0] - dp(10), None)

    def _send(self, val):
        _in_q.put(str(val))
        self._txt_in.text = ''
        Clock.schedule_once(lambda dt: setattr(self._txt_in, 'focus', False), 0)

    def _quick_send(self, val):
        _in_q.put(str(val))

    # ── Periodic update (polls output queue) ──────────────────────────────
    def _update(self, dt):
        changed = False
        while not _out_q.empty():
            try:
                chunk = _out_q.get_nowait()
            except Exception:
                break
            if chunk == _CLEAR:
                self._lines = []
            else:
                self._lines.extend(chunk.split('\n'))
                if len(self._lines) > 500:
                    self._lines = self._lines[-500:]
            changed = True

        if changed:
            self._raw_txt = '\n'.join(self._lines)
            self._term.text = _ansi_to_markup(self._raw_txt)
            # Scroll to bottom
            Clock.schedule_once(lambda dt: setattr(self._scroll, 'scroll_y', 0), 0.03)
            # Update context buttons
            new_ctx = _detect_ctx(self._raw_txt)
            if new_ctx != self._ctx:
                self._ctx = new_ctx
                self._rebuild_buttons()

    # ── Context button builder ────────────────────────────────────────────
    def _rebuild_buttons(self):
        self._btn_grid.clear_widgets()
        pairs   = _BTN_SETS.get(self._ctx, _BTN_SETS['default'])
        n       = len(pairs)
        cols    = min(5, max(3, n))
        rows    = -(-n // cols)                              # ceiling division
        self._btn_grid.cols   = cols
        self._btn_grid.height = dp(rows * 48 + (rows - 1) * 2 + 8)

        for value, label in pairs:
            btn = _StyledButton(
                label=label, value=value, cb=self._quick_send,
                font_size=dp(10),
            )
            self._btn_grid.add_widget(btn)


# ═══════════════════════════════════════════════════════════════════════════
#  KIVY APP CLASS
# ═══════════════════════════════════════════════════════════════════════════
class MMAApp(App):
    def build(self):
        self.title = 'MMA Legends Pro'
        self._view = TerminalView()
        self._start_game()
        return self._view

    def _start_game(self):
        t = threading.Thread(target=self._game_loop, daemon=True)
        t.start()

    def _game_loop(self):
        if not _GAME_OK:
            _out_q.put(f'\n[color=ff5555]ERROR: Could not load game module.[/color]\n{_GAME_ERR}\n')
            return
        try:
            loaded = _g.menu_title_screen()
            if loaded:
                g = loaded
            else:
                g = _g.GameState()
                starter = _g.menu_create_fighter(g)
                g.gym_roster.append(starter)
                g.world_roster[starter.weight_class].insert(40, starter)
            _g.menu_main(g)
        except SystemExit:
            pass                           # normal exit from game
        except Exception as exc:
            import traceback
            _out_q.put(f'\n\n[CRASH] {exc}\n{traceback.format_exc()}\n')

    def on_pause(self):
        return True                        # allow Android home-button pause

    def on_resume(self):
        pass


# ═══════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    MMAApp().run()
