import libs.wgyKeyPad, libs.pnhLCD1602
import time
from db import fetch_pass
import hashlib
import pygame
import threading
from libs.EmulatorGUI import GPIO


pw = fetch_pass()
_row_pins = [14, 15, 18, 23]
_col_pins = [24, 25, 8, 7]
_relay_pins = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(_relay_pins, GPIO.OUT)
key = libs.wgyKeyPad.KeyPad(
    row_pins=_row_pins,
    col_pins=_col_pins,
    key_map="4x4",
)
_msg = ""


def config_lcd():
    global _msg
    _lcd = libs.pnhLCD1602.LCD1602()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        _lcd.clear()
        _lcd.write_string(_msg)
        pygame.time.delay(200)
        _lcd.backlight_off()
        pygame.time.delay(50)
        _lcd.backlight_on()
        pygame.time.delay(50)
        _lcd.home()
        pygame.time.delay(50)
        time.sleep(0.1)


def sha1(bstr):
    return hashlib.sha1(bstr).digest().hex()


threading.Thread(target=config_lcd).start()


def main():
    global key, pw, _msg, _relay_pins
    _curr = b""
    _msg = f"Enter: {_curr}"
    while True:
        prs = key.scan()
        if prs:
            _curr += prs.encode()
            _msg = f"Enter: {_curr}"
            if len(_curr) == 4 and sha1(_curr) == pw:
                _msg = "Door opened"
                GPIO.output(_relay_pins, GPIO.HIGH)
                time.sleep(5)
                _msg = "Door closed"
                GPIO.output(_relay_pins, GPIO.LOW)
                time.sleep(2)
                _curr = b""
                _msg = f"Enter: {_curr}"
            elif len(_curr) == 4 and sha1(_curr) != pw:
                _msg = "Incorrect"
                _curr = b""
                time.sleep(2)
                _msg = f"Enter: {_curr}"
        time.sleep(0.1)


if __name__ == "__main__":
    main()
