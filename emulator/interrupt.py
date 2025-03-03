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

GPIO.setmode(GPIO.BCM)

GPIO.setup(_sensor_90, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_sensor_45, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_btn_start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(_btn_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.setup(_relay_90, GPIO.OUT)
GPIO.setup(_relay_45, GPIO.OUT)
GPIO.setup(_led, GPIO.OUT)


_state = False
_clsf_90 = False
_clsf_45 = False
_cnt_90 = 0
_cnt_45 = 0


def read_sensor():
    global _sensor_dht
    return readSensor(_sensor_dht)


def start():
    global _state, _btn_start
    while True:
        if GPIO.input(_btn_start) == 0:
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


def clsf_90():
    global _state, _sensor_90, _clsf_90, _relay_90
    while True:
        if _state and GPIO.input(_sensor_90) == 0:
            _clsf_90 = not _clsf_90
            print(f'class 90: {"on" if _clsf_90 else "off"}')
            GPIO.output(_relay_90, GPIO.HIGH if _clsf_90 else GPIO.LOW)
            print(f'relay 90: {"on" if _clsf_90 else "off"}')
        time.sleep(0.1)


def clsf_45():
    global _state, _sensor_45, _clsf_45
    while True:
        if _state and GPIO.input(_sensor_45) == 0:
            _clsf_45 = not _clsf_45
            print(f'class 45: {"on" if _clsf_45 else "off"}')
        time.sleep(0.1)


def lcd_config(line1: str, line2: str):
    global _lcd
    _lcd.clear()
    _lcd.write_string(line1)
    _lcd.set_cursor(1, 0)
    _lcd.write_string(line2)
    pygame.time.delay(3000)


threading.Thread(target=start, daemon=True).start()
threading.Thread(target=stop, daemon=True).start()
threading.Thread(target=led, daemon=True).start()
threading.Thread(target=clsf_90, daemon=True).start()
threading.Thread(target=clsf_45, daemon=True).start()


def main():
    global _state, _led
    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        temp, humi = read_sensor()
        lcd_config(line1="Dem san pham d", line2=f" {temp:.1f}°C - {humi:.2f}%")
        main()
    except Exception as e:
        GPIO.cleanup()
        exit()
