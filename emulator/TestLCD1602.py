from LCD1602 import LCD1602
import pygame
from string import ascii_letters

if __name__ == "__main__":
    lcd = LCD1602()
    try:

        for x in ascii_letters:
            lcd.clear()
            # Hiển thị cả hai dòng cùng lúc
            lcd.write_string(f"test-{x}")
            lcd.set_cursor(1, 0)  # Đặt con trỏ ở dòng thứ 2
            lcd.write_string("9999999999999989")
            pygame.time.delay(500)  # Hiển thị trong 3 giây
            lcd.backlight_off()
            pygame.time.delay(500)
            lcd.backlight_on()
            pygame.time.delay(500)
            lcd.home()
            pygame.time.delay(500)
    finally:
        lcd.close()
