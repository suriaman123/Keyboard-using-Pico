# custom keyboard by Aman

import time
import board        # to use pin names
import digitalio    # set pins as input-output
import usb_hid      # USB Human Interface Device - lets your device act as a USB device
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode    # to use individual keys


pico = Keyboard(usb_hid.devices)     # Keyboard object (a USB keyboard)
layout = KeyboardLayoutUS(pico)

# Buttons
pins = [board.GP10, board.GP11, board.GP12, board.GP13]
buttons = []
for pin in pins:
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT    # setting button as input           
    button.pull = digitalio.Pull.UP                 # Enables an internal pull-up resistor: Default state = HIGH (True) , Pressed = LOW (False)
    buttons.append(button)

# LED 
led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT
led.value = False

prev = [True] * 4

def mic_mute():                                 # mic mute/unmute
    pico.press(Keycode.WINDOWS, Keycode.ALT, Keycode.K)
    time.sleep(0.05)
    pico.release_all()

def vol_mute():                                 # volume mute/unmute
    pico.press(Keycode.MUTE)
    time.sleep(0.05)
    pico.release_all()

def type_text():
    layout.write("Crazy! Crazy!")
    time.sleep(0.01)

def lock_pc():                                  # lock laptop
    pico.press(Keycode.WINDOWS, Keycode.L)
    time.sleep(0.05)
    pico.release_all()

actions = [mic_mute, vol_mute, type_text, lock_pc]

def flash_led(times=1, on=80, off=60):
    #Flash LED a given number of times
    for _ in range(times):
        led.value = True
        time.sleep(on / 1000)
        led.value = False
        time.sleep(0.01)

# --- Main loop ---
while True:
    for i, btn in enumerate(buttons):
        pressed = not btn.value
        if pressed and not prev[i]:
            try:
                actions[i]()
                flash_led(i + 1)
            except Exception as e:
                print("Error:", e)
                led.value = True         
        prev[i] = pressed
    time.sleep(0.02)
