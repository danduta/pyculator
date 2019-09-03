import getpass
import sys
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import webbrowser as web
from math import ceil
from os import path
from time import ctime, time

from PIL import Image, ImageTk

RESOLUTION = "302x500"
PADDING = 10
BUTTON_WIDTH = 9
BUTTON_HEIGHT = 2

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


class Button(tk.Button):
    pass


class Calculator:
    expression = ""
    history = ""

    def __init__(self, master):
        print("Calculator Started at", ctime(time()))
        try:
            self.file = open('calculator_history.txt', 'w+')
        except:
            print("ERROR ALERTA NATIONALA")
        print("History filed openned successfully")
        self.history = "Calculator started at " + ctime(time()) + '\n'
        self.equation = tk.StringVar()

        self.frame = tk.Frame(master, bg="#3eb5a7")
        self.frame.place(height=450, width=302, rely=0.12)

        originalIcon = Image.open(resource_path("download.png"))
        resized = originalIcon.resize((32, 32), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(resized)
        logoButton = tk.Button(self.frame, image=self.icon, command=self.saveHistory,
                               width=68, height=34)
        logoButton.grid(row=0, column=0, pady=2)

        clearButton = tk.Button(self.frame, text="Clear", command=self.clear, bg="light blue",
                                width=2 * BUTTON_WIDTH + 2, height=BUTTON_HEIGHT)
        clearButton.grid(row=6, column=2, padx=2, pady=2, columnspan=2)

        quitButton = tk.Button(self.frame, text="Quit", command=lambda: self.dialogQuit(master),
                               width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        quitButton.grid(row=0, column=1, pady=2)

        gitButton = tk.Button(self.frame, text="Git", command=lambda: web.open('https://github.com/danduta'),
                              width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        gitButton.grid(row=0, column=2, padx=2, pady=2)

        instaButton = tk.Button(self.frame, text="Instagram", font=("Billabong", 13), bg="#db1a64",
                                command=lambda: web.open('https://instagram.com/danduta1'), width=BUTTON_WIDTH)
        instaButton.grid(row=0, column=3, pady=2)

        display = tk.Entry(self.frame, textvariable=self.equation, font=("Courier New", 15, "bold"), state="disabled",
                           bg="light gray")
        display.grid(row=1, columnspan=4, ipadx=7)

        for i in range(9):
            button = Button(self.frame, text=str(i+1), command=lambda i=i: self.press(str(i+1)),
                            width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            button.grid(row=(4-(i//3)), column=(i%3), padx=2, pady=2)

        button0 = tk.Button(self.frame, text="0", command=lambda: self.press("0"),
                            width=2 * BUTTON_WIDTH + 2, height=BUTTON_HEIGHT)
        button0.grid(row=5, column=0, pady=2, columnspan=2)

        buttonComma = tk.Button(self.frame, text=".", command=lambda: self.press("."),
                                width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        buttonComma.grid(row=5, column=2, padx=2)

        operatorsList = ['+', '-', '*', '/']

        for operator, i in zip(operatorsList, range(2, 6)):
            button = Button(self.frame, text=operator, command=lambda operator=operator: self.press(operator),
                            width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            button.grid(row=i, column=3, padx=2, pady=2)

        buttonEqual = tk.Button(self.frame, text="=", command=self.pressEqual, bg="gray",
                                width=2 * BUTTON_WIDTH + 2, height=BUTTON_HEIGHT)
        buttonEqual.grid(row=6, column=0, padx=2, columnspan=2)

        additionalOperatorsDict = {"x²": "**2=", "x³": "**3=", "%": "*0.01=", "xⁿ": "**",
                                   "(": "(", ")": ")", "√": "sqrt("}

        for (operator, operation), i in zip(additionalOperatorsDict.items(), range(8)):
            if operation[-1] == '=':
                operation = operation[:-1]
                command = lambda operation=operation:[self.press(operation), self.pressEqual()]
            else:
                command = lambda operation=operation:self.press(operation)

            button = Button(self.frame, text=operator, command=command, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            button.grid(row=7+(i//4), column=(i%4), padx=2, pady=10)

        self.equation.set("Calculate..")


    def press(self, buttonPressed):
        self.expression = self.expression + str(buttonPressed)
        self.equation.set(self.expression)

    def pressEqual(self):
        try:
            total = str(eval(self.expression))
            print(self.expression)
            self.history = self.history + self.expression + "=" + total + "\n"
            self.expression = total
            self.equation.set(total)

        except:
            self.equation.set("ERROR")

    def tip(self):
        self.pressEqual()
        total = eval(self.expression)
        total = ceil(0.1 * total)
        self.expression = str(total)
        self.equation.set(self.expression)

    def clear(self):
        self.expression = ""
        self.equation.set(self.expression)

    def dialogQuit(self, window):
        if tk.messagebox.askokcancel("Quitting", "Are you sure you want to quit?"):
            print("Calculator Quitting at", ctime(time()))
            self.history = self.history + "Calculator closed at " + ctime(time()) + '\n'
            self.file.write(self.history)
            self.file.close()
            print("History file closed successfully")
            window.destroy()

    def saveHistory(self):
        try:
            filename = simpledialog.askstring(title="Save file", prompt="Enter desired filename:")
            title = simpledialog.askstring(title="Title of file", prompt="Enter file title:")
            username = getpass.getuser()
            savefile = open('C:\\Users\\' + username + '\\Desktop\\' + filename + '.txt', "w")
            savefile.write(title + '\n')
            savefile.write(self.history + "Saved at " + ctime(time()) + '\n')
            savefile.close()
            print("Saved history successfully")
        except:
            print("History save failed")


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Pyculator")
    window.geometry(RESOLUTION)
    window.resizable(0, 0)
    window.iconbitmap(resource_path("favicon.png"))
    window.configure(background="#3eb5a7")

    calc = Calculator(window)

    topLabel = tk.Label(window, text="PYCULATOR", font=("Courier New", 30, "bold"), bg="#3eb5a7")
    topLabel.pack(side="top")
    copyLabel = tk.Label(window, text="Copyright Dan Duta, ACS UPB, 2019", bg="#3eb5a7")
    copyLabel.pack(side="bottom")

    window.protocol("WM_DELETE_WINDOW", lambda: calc.dialogQuit(window))
    window.mainloop()