import board, time
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.combos import Combos, Chord
from kmk.extensions.unicode import UnicodeMode
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.rotary_encoder import RotaryEncoderHandler
from kmk.handlers.sequences import simple_key_sequence
from kmk.extensions.OLED import OLED, OledDisplayMode, OledReactionType

# Keyboard
kbd = KMKKeyboard()
kbd.row_pins = (board.GP6, board.GP7)  # rows: D4, D1
kbd.col_pins = (board.GP3, board.GP4, board.GP5)  # cols: SW1-6, SW7-8
kbd.diode_orientation = kbd.DIODE_COL2ROW

# Rotary encoder
enc = RotaryEncoderHandler()
enc.pins = ((board.GP10, board.GP11, board.GP12),)  # A, B, Switch
enc.map = (
    (
        simple_key_sequence((KC.VOLD,)),  # CCW
        simple_key_sequence((KC.VOLU,)),  # CW
        simple_key_sequence((KC.MUTE,)),  # Press
    ),
)
kbd.modules.append(enc)

# Unicode
uni = UnicodeMode(mode=UnicodeMode.MAC)
kbd.extensions.append(uni)

# Diacritics
GRAVE  = KC.N1   # SW1
ACUTE  = KC.N2   # SW2
CEDIL  = KC.N3   # SW3
UMLAUT = KC.N4   # SW4
CIRC   = KC.N5   # SW5
TILDE  = KC.N6   # SW6
RING   = KC.N7   # SW7
SLASH  = KC.N8   # SW8

# Keymap layout
kbd.keymap = [[
    GRAVE,  UMLAUT, KC.NO,
    ACUTE,  CIRC,   RING,
    CEDIL,  TILDE,  SLASH,
]]

# Combos
def UC(hexstr): return KC.UC(int(hexstr, 16))

combos = Combos()
kbd.modules.append(combos)

combos.combos = [
    # Acute
    Chord((KC.A, ACUTE), UC("00E1")), Chord((KC.E, ACUTE), UC("00E9")),
    Chord((KC.I, ACUTE), UC("00ED")), Chord((KC.O, ACUTE), UC("00F3")),
    Chord((KC.U, ACUTE), UC("00FA")),
    # Grave
    Chord((KC.A, GRAVE), UC("00E0")), Chord((KC.E, GRAVE), UC("00E8")),
    Chord((KC.I, GRAVE), UC("00EC")), Chord((KC.O, GRAVE), UC("00F2")),
    Chord((KC.U, GRAVE), UC("00F9")),
    # Circumflex
    Chord((KC.A, CIRC),  UC("00E2")), Chord((KC.E, CIRC),  UC("00EA")),
    Chord((KC.I, CIRC),  UC("00EE")), Chord((KC.O, CIRC),  UC("00F4")),
    Chord((KC.U, CIRC),  UC("00FB")),
    # Tilde
    Chord((KC.N, TILDE), UC("00F1")), Chord((KC.A, TILDE), UC("00E3")),
    Chord((KC.O, TILDE), UC("00F5")),
    # Umlaut
    Chord((KC.A, UMLAUT), UC("00E4")), Chord((KC.E, UMLAUT), UC("00EB")),
    Chord((KC.I, UMLAUT), UC("00EF")), Chord((KC.O, UMLAUT), UC("00F6")),
    Chord((KC.U, UMLAUT), UC("00FC")),
    # Cedilla
    Chord((KC.C, CEDIL), UC("00E7")), Chord((KC.S, CEDIL), UC("015F")),
    Chord((KC.T, CEDIL), UC("0163")),
    # Ring
    Chord((KC.A, RING),  UC("00E5")), Chord((KC.U, RING),  UC("016F")),
    # Slash
    Chord((KC.O, SLASH), UC("00F8")), Chord((KC.L, SLASH), UC("0142")),
]

# Encoder keys
kbd.extensions.append(MediaKeys())

# OLED
def draw_oled(oled, keyboard):
    oled.fill(0)
    oled.text("AccentBean", 0, 0, 1)
    oled.text("Layer: BASE", 0, 8, 1)
    keys = keyboard.record.keys_pressed
    if keys:
        oled.text(f"Key: {keys[-1]}", 0, 16, 1)
    enc_state = enc.last_direction
    if enc_state == -1:
        oled.text("ENC: CCW", 70, 16, 1)
    elif enc_state == 1:
        oled.text("ENC: CW", 70, 16, 1)
    elif enc_state == 2:
        oled.text("ENC: MUTE", 64, 16, 1)
    oled.show()

# Patch encoder press feedback
_original_handler = enc.handler
def _patched_handler(*args, **kwargs):
    result = _original_handler(*args, **kwargs)
    if enc.switch_state:
        enc.last_direction = 2
    return result
enc.last_direction = 0
enc.handler = _patched_handler

oled_ext = OLED(
    OledDisplayMode.BOTH,
    flip=False,
    target=None,
    timeout=0,
    rate=10,
)
oled_ext.add_display_callback(OledReactionType.PERIODIC, draw_oled)
kbd.extensions.append(oled_ext)





if __name__ == '__main__':
    kbd.go()

