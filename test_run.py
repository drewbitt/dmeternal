import pyautogui
import time

time.sleep(2)

# tests exiting game
# press down 5 times to get to exit, then enter to exit
pyautogui.press(['down', 'down', 'down', 'down', 'down'])
pyautogui.press('enter')

