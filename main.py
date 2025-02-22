from ctypes import WinDLL, c_bool, c_wchar_p, c_int, c_byte, POINTER, create_unicode_buffer as c_u_b

LOGI_LCD_TYPE_MONO = 0x00000001
LOGI_LCD_TYPE_COLOR = 0x00000002

LOGI_LCD_MONO_BUTTON_0 = 0x00000001
LOGI_LCD_MONO_BUTTON_1 = 0x00000002
LOGI_LCD_MONO_BUTTON_2 = 0x00000004
LOGI_LCD_MONO_BUTTON_3 = 0x00000008

LOGI_LCD_COLOR_BUTTON_LEFT = 0x00000100
LOGI_LCD_COLOR_BUTTON_RIGHT = 0x00000200
LOGI_LCD_COLOR_BUTTON_OK = 0x00000400
LOGI_LCD_COLOR_BUTTON_CANCEL = 0x00000800
LOGI_LCD_COLOR_BUTTON_UP = 0x00001000
LOGI_LCD_COLOR_BUTTON_DOWN = 0x00002000
LOGI_LCD_COLOR_BUTTON_MENU = 0x00004000

LOGI_LCD_MONO_WIDTH = 160
LOGI_LCD_MONO_HEIGHT = 43

LOGI_LCD_COLOR_WIDTH = 320
LOGI_LCD_COLOR_HEIGHT = 240

class Logi_LCD(WinDLL):
    def __init__(self, applet_name: str, lcd_type: int):
        super().__init__('C:\\Program Files\\Logitech Gaming Software\\SDK\\LCD\\x64\\LogitechLcd.dll')

        self.LogiLcdInit.argtypes = [c_wchar_p, c_int]
        self.LogiLcdInit.restype = c_bool

        self.LogiLcdIsConnected.argtypes = [c_int]
        self.LogiLcdIsConnected.restype = c_bool

        self.LogiLcdIsButtonPressed.argtypes = [c_int]
        self.LogiLcdIsButtonPressed.restype = c_bool

        self.LogiLcdUpdate.argtypes = []
        self.LogiLcdUpdate.restype = None

        self.LogiLcdShutdown.argtypes = []
        self.LogiLcdShutdown.restype = None

        self.LogiLcdMonoSetBackground.argtypes = [POINTER(c_byte)]
        self.LogiLcdMonoSetBackground.restype = c_bool

        self.LogiLcdMonoSetText.argtypes = [c_int, c_wchar_p]
        self.LogiLcdMonoSetText.restype = c_bool

        self.LogiLcdColorSetBackground.argtypes = [POINTER(c_byte)]
        self.LogiLcdColorSetBackground.restype = c_bool

        self.LogiLcdColorSetTitle.argtypes = [c_wchar_p, c_int, c_int, c_int]
        self.LogiLcdColorSetTitle.restype = c_bool

        self.LogiLcdColorSetText.argtypes = [c_int, c_wchar_p, c_int, c_int, c_int]
        self.LogiLcdColorSetText.restype = c_bool

        self.LogiLcdColorSetBackgroundUDK.argtypes = [POINTER(c_byte), c_int]
        self.LogiLcdColorSetBackgroundUDK.restype = c_int

        self.LogiLcdColorResetBackgroundUDK.argtypes = []
        self.LogiLcdColorResetBackgroundUDK.restype = c_int

        self.LogiLcdMonoSetBackgroundUDK.argtypes = [POINTER(c_byte), c_int]
        self.LogiLcdMonoSetBackgroundUDK.restype = c_int

        self.LogiLcdMonoResetBackgroundUDK.argtypes = []
        self.LogiLcdMonoResetBackgroundUDK.restype = c_int
        
        self.LogiLcdInit(c_u_b(applet_name), lcd_type)

    def is_connected(self, lcd_type: int) -> bool:
        return self.LogiLcdIsConnected(lcd_type)

    def is_button_pressed(self, button: int) -> bool:
        return self.LogiLcdIsButtonPressed(button)

    def update(self) -> None:
        self.LogiLcdUpdate()

    def shutdown(self) -> None:
        self.LogiLcdShutdown()

    def mono_set_background(self, background: bytes) -> bool:
        bg_array = (c_byte * len(background))(*background)
        return self.LogiLcdMonoSetBackground(bg_array)

    def mono_set_text(self, row: int, text: str) -> bool:
        return self.LogiLcdMonoSetText(row, c_u_b(text))

    def color_set_background(self, background: bytes) -> bool:
        bg_array = (c_byte * len(background))(*background)
        return self.LogiLcdColorSetBackground(bg_array)

    def color_set_title(self, title: str, r: int, g: int, b: int) -> bool:
        return self.LogiLcdColorSetTitle(c_u_b(title), r, g, b)

    def color_set_text(self, row: int, text: str, r: int, g: int, b: int) -> bool:
        return self.LogiLcdColorSetText(row, c_u_b(text), r, g, b)

    def color_set_background_udk(self, background: bytes, size: int) -> int:
        bg_array = (c_byte * len(background))(*background)
        return self.LogiLcdColorSetBackgroundUDK(bg_array, size)

    def color_reset_background_udk(self) -> int:
        return self.LogiLcdColorResetBackgroundUDK()

    def mono_set_background_udk(self, background: bytes, size: int) -> int:
        bg_array = (c_byte * len(background))(*background)
        return self.LogiLcdMonoSetBackgroundUDK(bg_array, size)

    def mono_reset_background_udk(self) -> int:
        return self.LogiLcdMonoResetBackgroundUDK()

# Testing with monochrome Logitech G15 LCD
if __name__ == "__main__":
    from PIL import Image, ImageDraw, ImageFont
    from time import sleep
    
    #Basic test class for monochrome image with custom text font and size
    class Bg:
        def __init__(self, font:ImageFont):
            self.bg = Image.new('1', (160, 43), 0)
            self.row_height = 43 // 5
            self.draw = ImageDraw.Draw(self.bg)
            self.font = font

        def write(self, row: int, text: str) -> None:
            self.clear_row(row)
            y_position = row * self.row_height + 2
            self.draw.text((5, y_position), text, font=self.font, fill=255)

        def clear_row(self, row: int) -> None:
            y_position = row * self.row_height + 2
            self.draw.rectangle([0, y_position, 160, y_position + self.row_height], fill=0)
        
        def to_bytes(self) -> bytes:
            return self.bg.convert("L").tobytes()
    
    #init LCD
    lcd = Logi_LCD("PYTHON LCD TEST", LOGI_LCD_TYPE_MONO)
    
    #Test native text function
    lcd.mono_set_text(0, "HELLO WORLD")
    lcd.update()
    
    count = 4
    while True:
        lcd.mono_set_text(3, f"GOODBYE WORLD IN {count}...")
        count -= 1
        lcd.update()
        sleep(1)
        if count == 0:
            break
        
    #Clear text or else it will be overlayed in front of proceeding background image test
    lcd.mono_set_text(0, "")
    lcd.mono_set_text(3, "")
    
    #Test monolithic background image solution for custom text size and font, ctrl-c to exit
    bg = Bg(ImageFont.truetype("KernelPanicNbp-LyG3.ttf", size=9))
    while True:
        bg.write(0, "TEST")
        bg.write(1, f"{count}{count}{count}{count}{count}")
        bg.write(2, "FOO BAR")
        bg.write(3, "HELLO FOO")
        bg.write(4, "WORLD BAR")
        lcd.mono_set_background(bg.to_bytes())
        lcd.update()
        
        count += 1
        if count == 11:
            count = 0
        sleep(1)