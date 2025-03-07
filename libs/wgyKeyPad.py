from libs.EmulatorGUI import GPIO
import threading
import time
from tkinter import *
import tkinter as tk


class App(threading.Thread):
    def __init__(self, keypad):
        self.keypad = keypad
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.wm_title("KEYPAD")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.keys = self.keypad.key_map

        for i in range(4):
            for j in range(4):
                button = tk.Button(
                    self.root,
                    text=self.keys[i][j],
                    width=8,
                    height=5,
                    command=lambda row=i, col=j: self.btn_sim_gpio(row=row, col=col),
                )
                button.grid(row=i, column=j)
        self.root.mainloop()

    def btn_sim_gpio(self, row, col):
        self.keypad.btn_press_sim(row, col)


class KeyPad:
    __KEY_MAPS = {
        "4x4": [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"],
        ],
        "3x3": [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]],
        "3x4": [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["*", "0", "#"]],
    }

    def __init__(self, row_pins, col_pins, key_map="4x4", emu=True):
        self.row_pins = row_pins
        self.col_pins = col_pins
        self.key_map = KeyPad.__KEY_MAPS[key_map]
        self.__setup()
        self.emu = emu
        if self.emu:
            self.app = App(self)
            self.pressed = None

    def scan(self):
        if not self.emu:
            for r, row in enumerate(self.row_pins):
                GPIO.output(row, GPIO.LOW)
                for c, col in enumerate(self.col_pins):
                    if GPIO.input(col) == 0:
                        GPIO.output(row, GPIO.HIGH)
                        return self.key_map[r][c]
                GPIO.output(row, GPIO.HIGH)
            return None
        return self.pressed

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.row_pins:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.col_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def btn_press_sim(self, row, col):
        self.pressed = self.key_map[row][col]
        time.sleep(0.1)
        self.pressed = None
