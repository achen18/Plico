import board
import time

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.keys import KC, Key
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.extensions.RGB import RGB

class LedKey(Key):
    def __init__(self, key, led_index, hue=280, sat=255, val=255, fade_steps=5):
        self.key = key
        self.led_index = led_index
        self.hue = hue
        self.sat = sat
        self.val = val
        self.fade_steps = fade_steps

    def on_press(self, keyboard, coord_int=None):
        keyboard.add_key(self.key)
        keyboard.rgb.set_hsv(self.hue, self.sat, self.val, self.led_index)
        keyboard.rgb.show()

    def on_release(self, keyboard, coord_int=None):
        keyboard.remove_key(self.key)
        # Fade LED gradually
        for i in range(self.fade_steps, 0, -1):
            keyboard.rgb.set_hsv(self.hue, self.sat, int(self.val * i / self.fade_steps), self.led_index)
            keyboard.rgb.show()
            time.sleep(0.02)  #  migt need adjustment for BLE, sleep stops main loop, so also stops comms?

keyboard = KMKKeyboard()

# Matrix pins
keyboard.col_pins = (
    board.D1,    # col 0
    board.D2,    # col 1
    board.D3,    # col 2
    board.D4,    # col 3
    board.D5,    # col 4
)

keyboard.row_pins = (
    board.D10,   # row 0
    board.D9,    # row 1
    board.D8,    # row 2
    board.D7,    # row 3
    board.D6,    # row 4
)

# Diode direction: Column to Row
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Keymap
keyboard.keymap = [
    [LedKey(KC.N6,0), LedKey(KC.N7,1), LedKey(KC.N8,2), LedKey(KC.N9,3), LedKey(KC.N0,4)],
    [LedKey(KC.Y,5), LedKey(KC.U,6), LedKey(KC.I,7), LedKey(KC.O,8), LedKey(KC.P,9)],
    [LedKey(KC.H,10), LedKey(KC.J,11), LedKey(KC.K,12), LedKey(KC.L,13), LedKey(KC.SCOLON,14)],
    [LedKey(KC.N,15), LedKey(KC.M,16), LedKey(KC.COMMA,17), LedKey(KC.DOT,18), LedKey(KC.SLASH,19)],
    [KC.NO, KC.NO, KC.NO, LedKey(KC.BSPACE,21), LedKey(KC.SPACE,20)]
]

# Bluetooth Low Energy
split = Split(
    split_type=SplitType.BLE,
    split_side=SplitSide.RIGHT
)
keyboard.modules.append(split)

rgb = RGB(
    pixel_pin=board.NFC1,
    num_pixels=22,
    rgb_order=(1, 0, 2),      
    hue_default=0,             # <-
    sat_default=255,           # <-
    val_default=255,           # Pretty sure this makes white
    val_limit=255              # Maximum brightness allowed
)
keyboard.extensions.append(rgb)


if __name__ == "__main__":
    keyboard.go()
