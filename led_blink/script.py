import RPi.GPIO as GPIO
import time

LED_PINS = [4, 17, 27, 22, 5, 6, 13]
BUTTON_PIN = 26

running = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PINS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def toggle_running(channel):
    global running
    running = not running
    print("Start" if running else "Stop")


GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=toggle_running, bouncetime=300)

try:
    while True:
        if running:
            for pin in LED_PINS:
                if not running:
                    break
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(pin, GPIO.LOW)

        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExit")
finally:
    GPIO.cleanup()
