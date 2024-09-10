from pynput.keyboard import Key, Controller
import time

class controller():
    keyboard = Controller()

    def press_a(self):
        self.keyboard.press('x')
        time.sleep(0.1)
        self.keyboard.release('x')
        time.sleep(0.1)

    def press_b(self):
        self.keyboard.press('z')
        time.sleep(0.1)
        self.keyboard.release('z')
        time.sleep(0.1)
    
    def press_select(self):
        self.keyboard.press(Key.backspace)
        time.sleep(0.1)
        self.keyboard.release(Key.backspace)
        time.sleep(0.1)
    
    def press_start(self):
        self.keyboard.press(Key.enter)
        time.sleep(0.1)
        self.keyboard.release(Key.enter)
        time.sleep(0.1)
    
    def press_l(self):
        self.keyboard.press('a')
        time.sleep(0.1)
        self.keyboard.release('a')
        time.sleep(0.1)
    
    def press_r(self):
        self.keyboard.press('s')
        time.sleep(0.1)
        self.keyboard.release('s')
        time.sleep(0.1)

    def press_left(self):
        self.keyboard.press(Key.left)
        time.sleep(0.1)
        self.keyboard.release(Key.left)
        time.sleep(0.1)
    
    def press_right(self):
        self.keyboard.press(Key.right)
        time.sleep(0.1)
        self.keyboard.release(Key.right)
        time.sleep(0.1)
    
    def press_up(self):
        self.keyboard.press(Key.up)
        time.sleep(0.1)
        self.keyboard.release(Key.up)
        time.sleep(0.1)
    
    def press_down(self):
        self.keyboard.press(Key.down)
        time.sleep(0.1)
        self.keyboard.release(Key.down)
        time.sleep(0.1)

    def press_reset(self):
        self.keyboard.press('x')
        self.keyboard.press('z')
        self.keyboard.press(Key.backspace)
        self.keyboard.press(Key.enter)
        time.sleep(0.1)
        self.keyboard.release('x')
        self.keyboard.release('z')
        self.keyboard.release(Key.backspace)
        self.keyboard.release(Key.enter)
