############################################
#  KMK macropad: 8‑diacritic chords + audio knob
############################################
#  • Hold any letter together with one of the
#    eight diacritic keys  →  pre‑composed glyph
#  • EC11 encoder:  CW = volume‑up,
#                   CCW = volume‑down,
#                   press = mute
#
#  ▸ Adjust the pin lists (row_pins, col_pins, encoder pins)
#    plus the keymap layout to match your PCB.
############################################

import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.combos import Combos, Chord
from kmk.extensions.unicode import UnicodeMode
from kmk.modules.rotary_encoder import RotaryEncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.handlers.sequences import simple_key_sequence

kbd = KMKKeyboard()

# ──‑ Matrix wiring (change to suit your build) ─────────────────────────────────
kbd.row_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4)
kbd.col_pins = (board.GP5, board.GP6, board.GP7, board.GP8)
kbd.diode_orientation = kbd.DIODE_COL2ROW

# ──‑ Rotary encoder (EC11) ────────────────────────────────────────────────────
enc = RotaryEncoderHandler()
enc.pins = (
    (board.GP10, board.GP11, board.GP12),   # (pinA, pinB, switch)
)
enc.map = (
    (
        simple_key_sequence((KC.VOLD,)),     # CCW
        simple_key_sequence((KC.VOLU,)),     # CW
        simple_key_sequence((KC.MUTE,)),     # press
    ),
)
kbd.modules.append(enc)

# ──‑ Unicode output (pick mode for your OS) ‑──────────────────────────────────
uni = UnicodeMode(mode=UnicodeMode.MAC)      # MAC / WIN / WIN10 / LINUX
kbd.extensions.append(uni)

# ──‑ Physical diacritic keys (rename to your liking) ‑─────────────────────────
GRAVE   = KC.N1     # `
ACUTE   = KC.N2     # ´
CEDIL   = KC.N3     # ¸
UMLAUT  = KC.N4     # ¨
CIRC    = KC.N5     # ^
TILDE   = KC.N6     # ~
RING    = KC.N7     # ˚
SLASH   = KC.N8     # ˗  (slash overlay)

# ──‑ Example 5 × 4 keymap (20 keys) ‑──────────────────────────────────────────
# Row 0:   A  E  I  O
# Row 1:   U  N  C  S
# Row 2:   <GRAVE> <ACUTE> <CEDIL> <UMLAUT>
# Row 3:   <CIRC>  <TILDE> <RING>  <SLASH>
# Row 4:   (spare) (spare) (spare) (spare)
keymap = [
    [KC.A,    KC.E,     KC.I,     KC.O],
    [KC.U,    KC.N,     KC.C,     KC.S],
    [GRAVE,   ACUTE,    CEDIL,    UMLAUT],
    [CIRC,    TILDE,    RING,     SLASH],
    [KC.NO,   KC.NO,    KC.NO,    KC.NO],
]
kbd.keymap = [keymap]

# ──‑ Combos: letter + diacritic → Unicode char ‑──────────────────────────────
def UC(code_hex: str):
    """Return a KC that types the given Unicode code point."""
    return KC.UC(int(code_hex, 16))

combos = Combos()
kbd.modules.append(combos)

combos.combos = [
    # ── Acute (´)─────────────────────────────────
    Chord((KC.A, ACUTE), UC("00E1")),  # á
    Chord((KC.E, ACUTE), UC("00E9")),  # é
    Chord((KC.I, ACUTE), UC("00ED")),  # í
    Chord((KC.O, ACUTE), UC("00F3")),  # ó
    Chord((KC.U, ACUTE), UC("00FA")),  # ú

    # ── Grave (`)─────────────────────────────────
    Chord((KC.A, GRAVE), UC("00E0")),  # à
    Chord((KC.E, GRAVE), UC("00E8")),  # è
    Chord((KC.I, GRAVE), UC("00EC")),  # ì
    Chord((KC.O, GRAVE), UC("00F2")),  # ò
    Chord((KC.U, GRAVE), UC("00F9")),  # ù

    # ── Circumflex (^)────────────────────────────
    Chord((KC.A, CIRC),  UC("00E2")),  # â
    Chord((KC.E, CIRC),  UC("00EA")),  # ê
    Chord((KC.I, CIRC),  UC("00EE")),  # î
    Chord((KC.O, CIRC),  UC("00F4")),  # ô
    Chord((KC.U, CIRC),  UC("00FB")),  # û

    # ── Tilde (˜)─────────────────────────────────
    Chord((KC.N, TILDE), UC("00F1")),  # ñ
    Chord((KC.A, TILDE), UC("00E3")),  # ã
    Chord((KC.O, TILDE), UC("00F5")),  # õ

    # ── Umlaut / Diaeresis (¨)────────────────────
    Chord((KC.A, UMLAUT), UC("00E4")),  # ä
    Chord((KC.E, UMLAUT), UC("00EB")),  # ë
    Chord((KC.I, UMLAUT), UC("00EF")),  # ï
    Chord((KC.O, UMLAUT), UC("00F6")),  # ö
    Chord((KC.U, UMLAUT), UC("00FC")),  # ü

    # ── Cedilla (¸)───────────────────────────────
    Chord((KC.C, CEDIL), UC("00E7")),  # ç
    Chord((KC.S, CEDIL), UC("015F")),  # ş
    Chord((KC.T, CEDIL), UC("0163")),  # ţ

    # ── Ring (˚)──────────────────────────────────
    Chord((KC.A, RING),  UC("00E5")),  # å
    Chord((KC.U, RING),  UC("016F")),  # ů

    # ── Slash / Stroke (˗)────────────────────────
    Chord((KC.O, SLASH), UC("00F8")),  # ø
    Chord((KC.L, SLASH), UC("0142")),  # ł
]

# ──‑ Media keys extension is required for VOLU/VOLD/MUTE ‑─────────────────────
kbd.extensions.append(MediaKeys())

if __name__ == "__main__":
    kbd.go()
