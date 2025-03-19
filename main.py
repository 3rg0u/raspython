import libs.wgyKeyPad, libs.pnhLCD1602
import time
from db import fetch_pass
import hashlib
import pygame
import threading
from libs.EmulatorGUI import GPIO
from flask import Flask, request, jsonify
from flask_cors import CORS


__PW = fetch_pass()
__ROW_PINS = [14, 15, 18, 23]
__COL_PINS = [24, 25, 8, 7]
__RELAY_PIN = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(__RELAY_PIN, GPIO.OUT)


_KEYPAD = libs.wgyKeyPad.KeyPad(
    row_pins=__ROW_PINS,
    col_pins=__COL_PINS,
    key_map="4x4",
)
_CURRENT = b""
_MSG = f"Enter: {_CURRENT.decode()}"


def sha1(bstr):
    return hashlib.sha1(bstr).digest().hex()


def lcd_config():
    global _MSG
    _lcd = libs.pnhLCD1602.LCD1602()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        _lcd.clear()
        _lcd.write_string(_MSG)
        pygame.time.delay(200)
        _lcd.backlight_off()
        pygame.time.delay(50)
        _lcd.backlight_on()
        pygame.time.delay(50)
        _lcd.home()
        pygame.time.delay(50)
        time.sleep(0.1)


def input_scan():
    global _KEYPAD, __PW, __RELAY_PIN, _MSG, _CURRENT
    while True:
        pressed = _KEYPAD.scan()
        if pressed:
            _CURRENT += pressed.encode()
            _MSG = f"Enter: {_CURRENT.decode()}"
        time.sleep(0.1)


def password_check():
    global _MSG, _CURRENT
    while True:
        if len(_CURRENT) == 4 and sha1(_CURRENT) == __PW:
            _MSG = "Door opened"
            GPIO.output(__RELAY_PIN, GPIO.HIGH)
            time.sleep(5)
            _MSG = "Door closed"
            GPIO.output(__RELAY_PIN, GPIO.LOW)
            time.sleep(2)
            _CURRENT = b""
            _MSG = f"Enter: {_CURRENT.decode()}"
        elif len(_CURRENT) == 4 and sha1(_CURRENT) != __PW:
            _MSG = "Incorrect"
            _CURRENT = b""
            time.sleep(2)
            _MSG = f"Enter: {_CURRENT.decode()}"
        time.sleep(0.1)


_app = Flask(__name__)
CORS(_app)


@_app.route("/api/open", methods=["POST"])
def rpc_open():
    global _CURRENT, __PW
    _passcode = request.get_json()["passcode"].encode()
    if sha1(_passcode) == __PW:
        _CURRENT = _passcode
        return jsonify({"status": "success", "message": "Door opened!"})
    return jsonify({"status": "error", "message": "Incorret passcode!"})


def serve():
    global _app
    _app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)


def main():
    while True:
        time.sleep(0.1)


threading.Thread(target=lcd_config).start()
threading.Thread(target=input_scan).start()
threading.Thread(target=password_check).start()
threading.Thread(target=serve).start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        GPIO.cleanup()
        exit()
