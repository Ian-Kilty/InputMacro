'''
TODO
clean up aka. speedup function
'''
from curses import noecho
from pynput import mouse
from pynput import keyboard
import os
import sys
import time
import csv
import termcolor
os.system('color')
while 1:
    input_ = input(termcolor.colored("=+ ", "red"))
    if input_ == "new":
        name = input("Name: ")
        while 1:
            if name + ".csv" in os.listdir('Data'):
                print(name + " already exists")
                name = input("Name: ")
            else:
                break
        os.chdir("Data")
        input("Press enter to record in 3 seconds")
        print("1")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("3")
        time.sleep(1)
        global starttime
        starttime = time.time()
        global count
        count = 0
        def on_move(x, y):
            pass

        def on_click(x, y, button, pressed):
            global starttime
            f.writerow(["{0}".format('MousePressed' if pressed else 'MouseReleased'), (x, y), button, (time.time()-starttime)])
            starttime = time.time()

        def on_scroll(x, y, dx, dy):
            f.writerow(["Scroll", (x, y), (dx, dy)])
        
        def on_press(key):
            try:
                f.writerow(["KeyPressed", "{0}".format(key.char)])
            except AttributeError:
                f.writerow(["KeyPressed", "{0}".format(key)])

        def on_release(key):
            try:
                f.writerow(["KeyReleased", "{0}".format(key.char)])
                if key.char == "`":
                    mouseListener.stop()
                    keyboardListener.stop()
                    print("\nStopped Recording\nPress enter to procede")

            except AttributeError:
                f.writerow(["KeyReleased", "{0}".format(key)])

        mouseListener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll)
        keyboardListener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)

        with open(name + ".csv", "w", newline="") as f:
            f = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            mouseListener.start()
            keyboardListener.start()
            starttime = time.time()
            t = ""
            while not t == "`":
                t = input("Recording, press ` (in terminal window) to stop")
                if t == "`":
                    break
        os.chdir("..")
        

    if input_ == "run":
        while 1:
            name = input("Name: ")
            if name + ".csv" not in os.listdir("Data"):
                print("Please pick a macro that exists")
            else:
                break
        timer = input("Timer (blank for none): ")
        if timer == "":
            timer = "0"
        for i in range(int(timer), 0, -1):
            print(i)
            time.sleep(1)
        from pynput.keyboard import Key, Controller
        from pynput.mouse import Button, Controller
        import pyautogui
        mouseController = Controller()
        keyboardController = Controller()
        os.chdir("Data")
        with open(name +".csv", "r", newline="") as f:
            f = csv.reader(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in f:
                if row[0] == "MousePressed":
                    time.sleep(float(row[3]))
                    mouseController.position = eval(row[1])
                    pyautogui.mouseUp(button=row[2][7:])
                if row[0] == "MouseReleased":
                    time.sleep(float(row[3]))
                    mouseController.position = eval(row[1])
                    pyautogui.mouseDown(button=row[2][7:])
                if row[0] == "Scroll":
                    mouseController.position = eval(row[1])
                    mouseController.scroll(eval(row[2][0]), eval(row[2][1]))
                if row[0] == "KeyPressed":
                    if len(row[1]) > 1:
                        pyautogui.keyDown(row[1][4:])
                    else:
                        pyautogui.keyDown(row[1])
                if row[0] == "KeyReleased":
                    if len(row[1]) > 1:
                        pyautogui.keyUp(row[1][4:])
                    else:
                        pyautogui.keyUp(row[1])
        os.chdir("..")

    if input_ == "macros":
        for i in os.listdir("Data"):
            print(i[:-4])
    if input_ == "quit":
        sys.exit()
        
