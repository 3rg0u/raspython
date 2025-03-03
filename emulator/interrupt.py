from EmulatorGUI import GPIO
import time
import threading
from DHT22 import readSensor
import pygame
from LCD1602 import LCD1602

_sensor_90 = 22
_sensor_45 = 26
_relay_90 = 17
_relay_45 = 27
_lcd = LCD1602()
_btn_start = 23
_btn_stop = 24
_led = 25
_sensor_dht = 4
_state = False
_cnt_90 = 0
_cnt_45 = 0
_init = False


GPIO.setmode(GPIO.BCM)

GPIO.setup(_sensor_90, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_sensor_45, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_btn_start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_btn_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(_relay_90, GPIO.OUT)
GPIO.setup(_relay_45, GPIO.OUT)
GPIO.setup(_led, GPIO.OUT)


def read_sensor():
    global _sensor_dht
    return readSensor(_sensor_dht)


def start():
    global _state, _btn_start, _init
    while True:
        if GPIO.input(_btn_start) == 0:
            _init = True
            _state = True
            print("started")
        time.sleep(0.1)


def stop():
    global _state, _btn_stop
    while True:
        if GPIO.input(_btn_stop) == 0:
            _state = False
            print("stopped")
        time.sleep(0.1)


def led():
    global _state, _led
    while True:
        if _state:
            GPIO.output(_led, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(_led, GPIO.LOW)
            time.sleep(2)


def clsf():
    global _state, _sensor_90, _sensor_45, _cnt_90, _cnt_45, _relay_90, _relay_45
    while True:
        if _state and GPIO.input(_sensor_90) == 0:
            print("valid 90cm")
            _cnt_90 += 1
            GPIO.output(_relay_90, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(_relay_45, GPIO.LOW)
        elif _state and GPIO.input(_sensor_45) == 0:
            print("valid 45cm")
            _cnt_45 += 1
            GPIO.output(_relay_45, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(_relay_90, GPIO.LOW)
        elif _state:
            print("not valid")
            GPIO.output(_relay_90, GPIO.LOW)
            GPIO.output(_relay_45, GPIO.LOW)
            time.sleep(7)
        time.sleep(0.1)


def main():
    global _lcd, _init, _cnt_90, _cnt_45
    while True:
        temp, humi = read_sensor()
        _lcd.clear()
        if not _init:
            _lcd.write_string("DEM SAN PHAM D")
            _lcd.set_cursor(1, 0)
            _lcd.write_string(f"{temp:.2f}°C - {humi:.2f}%")
        else:
            _lcd.write_string(f"{temp:.2f}°C - {humi:.2f}%")
            _lcd.setdefault(1, 0)
            _lcd.write_string(f"90c={_cnt_90}-45c={_cnt_45}")
        pygame.time.delay(200)
        _lcd.backlight_off()
        pygame.time.delay(50)
        _lcd.backlight_on()
        pygame.time.delay(50)
        _lcd.home()
        pygame.time.delay(50)
        time.sleep(2)
        _lcd.clear()


threading.Thread(target=start, daemon=True).start()
threading.Thread(target=stop, daemon=True).start()
threading.Thread(target=led, daemon=True).start()
threading.Thread(target=clsf, daemon=True).start()
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        GPIO.cleanup()
        exit()
