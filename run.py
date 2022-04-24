'''
TODO
requierments.txt
clean up aka. speedup function
add the rest of the controlling functions
'''
from pynput import mouse
from pynput import keyboard
import os
import sys
import time
import csv
import termcolor
os.system('color')
while 1:
    input_ = input(termcolor.colored("=+ ", "red", 'on_grey', ['bold', 'blink']))
    if input_ == "new":
        name = input("Name: ")
        while 1:
            if name + ".csv" in os.listdir('Data'):
                print(name + " already exists")
                name = input("Name: ")
            else:
                break
        os.chdir("Data")
        f = open(name + ".csv", "w", newline="")
        f = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        input("Press enter to record in 3 seconds")
        print("1")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("Recording, press > to stop")
        def on_move(x, y):
            f.writerow(["Move", (x, y)]) 

        def on_click(x, y, button, pressed):
            f.writerow(["{0}".format('MousePressed' if pressed else 'MouseReleased'), (x, y)])

        def on_scroll(x, y, dx, dy):
            f.writerow(["{0}".format('down' if dy < 0 else 'up'), (x, y)])
        
        def on_press(key):
            try:
                f.writerow(["KeyPressed", "{0}".format(key.char)])
            except AttributeError:
                f.writerow(["KeyPressed", "{0}".format(key)])

        def on_release(key):
            try:
                f.writerow(["KeyReleased", "{0}".format(key.char)])
                if key.char == ">":
                    mouseListener.stop()
                    keyboardListener.stop()
                    print("\nStopped Recording")
            except AttributeError:
                f.writerow(["KeyReleased", "{0}".format(key)])

        mouseListener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll)
        keyboardListener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        mouseListener.start()
        keyboardListener.start()
        os.chdir("..")
        

    if input_ == "run":
        while 1:
            name = input("Name: ")
            if name + ".csv" not in os.listdir("Data"):
                print("Please pick a macro that exists")
            else:
                break
        from pynput.keyboard import Key, Controller
        from pynput.mouse import Button, Controller
        mouseController = Controller()
        keyboardController = Controller()
        os.chdir("Data")
        f = open(name + ".csv")
        f = csv.reader(f, delimiter=',')
        for row in f:
            if row[0] == "Move":
                mouseController.position = eval(row[1])
        os.chdir("..")

    if input_ == "macros":
        for i in os.listdir("Data"):
            print(i[:-4])
    if input_ == "quit":
        sys.exit()
        
