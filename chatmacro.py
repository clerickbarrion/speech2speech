from pynput.keyboard import Key, Controller
import time

def chat(input):
    keyboard = Controller()
    keyboard.press('/')
    time.sleep(0.1)
    keyboard.release('/')
    time.sleep(0.1)
    keyboard.type(input)
    time.sleep(0.1)
    keyboard.press(Key.enter)
    time.sleep(0.1)

if __name__ == "__main__":
    chat("Hello, world!")