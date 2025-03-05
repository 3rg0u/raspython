import libs.wgyKeyPad
import time

key = libs.wgyKeyPad.KeyPad(
    row_pins=[14, 15, 18, 23],
    col_pins=[24, 25, 8, 7],
    key_map=[
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"],
    ],
)


def main():
    global key
    while True:
        prs = key.scan()
        if prs:
            print(prs)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
