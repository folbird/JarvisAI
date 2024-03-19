import time
import pyautogui
import pyperclip
import os
import sys
sys.path.append("..")
from functions import *


def mapping_img(img, click):
    box_location = pyautogui.locateOnScreen(img)
    center = pyautogui.center(box_location)
    if click == "double":
        pyautogui.doubleClick(center)
    else:
        pyautogui.click(center)
    time.sleep(1)


def chat_user(user):

    """选择聊天对象"""

    if user != "":

        mapping_img("search.png", 'single')
        pyautogui.typewrite(user)
        time.sleep(2)
        pyautogui.moveRel(xOffset=0, yOffset=80)
        pyautogui.click()
        time.sleep(1)
    else:
        mapping_img("jundiao.png", "single")


def read_txt(txt):

    dialogfile = open(txt, "r", encoding="utf-8")
    dialog = dialogfile.readlines()
    dialog = ''.join(dialog)
    # dialog = "hello"
    pyperclip.copy(dialog)
    print("done1")
    pyautogui.hotkey('ctrl', 'v')
    print("done2")
    dialogfile.close()


def send_message():
    os.chdir("C:/Users/JUN/Desktop/JarvisAI/wechat/wechats")
    mapping_img('wechat.png', "double")
    chat_user('JJ')
    read_txt("C:/Users/JUN/Desktop/JarvisAI/Openai/1.txt")
    print("done3")
    pyautogui.press("enter")
    print("done4")
    time.sleep(1)


if __name__ == '__main__':
    send_message()