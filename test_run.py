import pyautogui
import time
import subprocess

subprocess.call("fg", shell=True)
print("got here after fg!")
time.sleep(2)

# tests exiting game
# press down 5 times to get to exit, then enter to exit
pyautogui.press(['down', 'down', 'down', 'down', 'down'])
print("got here!")
time.sleep(2)
pyautogui.press('enter')

