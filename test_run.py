import pyautogui
import time

time.sleep(2)

# tests exiting game
# press down 5 times to get to exit, then enter to exit
pyautogui.press(['down', 'down', 'down', 'down', 'down'])
time.sleep(2)
pyautogui.press('enter')

