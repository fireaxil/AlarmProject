from tkinter import *
from time import strftime
from time import sleep
from functools import partial

class App:

    def __init__(self):

        self.root = Tk()
        self.root['bg'] = 'white'
        frame = Frame(self.root)
        frame.pack()
        frame['bg']= 'white'

        self.timeText = Label(self.root, text= strftime("%H:%M:%S"), font=("Helvetica", 30), bg='white')
        self.timeText.pack(side = TOP)

        self.setAlarm = Button(frame, text= "Set Alarm", command=self.callback,  bg='white')
        self.setAlarm.pack(side= LEFT)

        self.alarmTime = Label(self.root, text="", font=("Helvetica", 30), bg='white')

        self.alarm1 = ""

        self.root.after(1000, self.update_time)
        self.root.mainloop()

    def update_time(self):
        now =  strftime("%H:%M:%S")
        self.timeText.configure(text=now)
        self.root.after(1000, self.update_time)

    def callback(self):
        self.timeText.pack_forget()
        self.setAlarm.pack_forget()
        self.alarmTime.pack()
        self.addKeyboard()
        print("Helllo world!!")

    def addKeyboard(self):
        lf = LabelFrame(self.root, text="Enter Alarm Time", bd=3,  bg='white')
        lf.pack(padx=15, pady=10)
        # typical calculator button layout
        btn_list = [
        '7',  '8',  '9',
        '4',  '5',  '6',
        '1',  '2',  '3',
        '0',  ':',  'Enter']
        # create and position all buttons with a for-loop
        # r, c used for row, column grid values
        r = 1
        c = 0
        n = 0
        # list(range()) needed for Python3
        btn = list(range(len(btn_list)))
        for label in btn_list:
            # partial takes care of function and argument
            cmd = partial(self.click, label)
            # create the button
            btn[n] = Button(lf, text=label, width=5, command=cmd,  bg='white')
            # position the button
            btn[n].grid(row=r, column=c)
            # increment button index
            n += 1
            # update row/column position
            c += 1
            if c > 2:
                c = 0
                r += 1


    def click(self, btn):
        # test the button command click
        s = "Button %s clicked" % btn
        if btn in ['1']:
            self.alarm1+='1'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['2']:
            self.alarm1+='2'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in [':']:
            self.alarm1+=':'
            self.alarmTime.configure(text=self.alarm1)
        print(btn)
        # root.title(s)

app = App()


