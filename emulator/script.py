import time
import traceback
from EmulatorGUI import GPIO
import threading

BTN_STATE = False

LED_PINS = [2, 3, 4, 17, 27, 22]


GPIO.setmode(GPIO.BCM)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def blink():
    global LED_PINS
    for pin in LED_PINS:
        GPIO.output(pin, True)
        time.sleep(0.2)
        GPIO.output(pin, False)


def toggle_switch():

    global BTN_STATE
    while True:
        time.sleep(5)
        GPIO.input = lambda pin: False if pin == 23 else GPIO.input(pin)
        blink()
        time.sleep(0.1)
        GPIO.input = lambda pin: True if pin == 23 else GPIO.input(pin)


def main():
    threading.Thread(target=toggle_switch, daemon=True).start()

    try:
        while True:
            print(f'LED is {"on" if BTN_STATE else "off"}')
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
