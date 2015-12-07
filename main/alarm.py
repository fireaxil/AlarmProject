from tkinter import *
from time import strftime
from time import sleep
from functools import partial
from builtins import print
import pyglet
class App:
    def __init__(self):

        self.root = Tk()
        self.root['bg'] = 'white'

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (w, h))

        self.root.focus_set() # <-- move focus to this widget
        self.root.bind("<Escape>", lambda e: e.widget.quit())

        frame = Frame(self.root)
        frame.pack()
        frame['bg']= 'white'

        self.timeText = Label(self.root, text= strftime("%H:%M:%S"), font=("Helvetica", 40), bg='white')
        self.timeText.pack(side = TOP)

        self.setAlarm = Button(frame, text= "Set Alarm", command=self.callback,  bg='white')
        self.setAlarm.pack(side= LEFT)

        self.alarmTime = Label(self.root, text="", font=("Helvetica", 40), bg='white')

        self.alarm1 = ""
        self.alarm1Time = -1

        self.currentTime = 0

        self.music = pyglet.resource.media('BlankSpace.wma')
        self.isMusicPlaying = 0

        self.root.after(1000, self.update_time)
        self.root.mainloop()

    def update_time(self):
        now =  strftime("%H:%M:%S")
        self.currentTime = int(strftime("%H%M"))
        # print(self.currentTime)
        self.timeText.configure(text=now)
        self.root.after(1000, self.update_time)
        self.checkAlarmTime()

    def checkAlarmTime(self):
        if(self.currentTime == self.alarm1Time):
            if self.isMusicPlaying == 0:
                self.music.play()
                self.isMusicPlaying = 1
            print("ALARMTIMEEEEEEEEE!")

    def callback(self):
        self.timeText.pack_forget()
        self.setAlarm.pack_forget()
        self.alarmTime.pack()
        self.addKeyboard()

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
        elif btn in ['3']:
            self.alarm1+='3'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['4']:
            self.alarm1+='4'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['5']:
            self.alarm1+='5'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['6']:
            self.alarm1+='6'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['7']:
            self.alarm1+='7'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['8']:
            self.alarm1+='8'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['9']:
            self.alarm1+='9'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['0']:
            self.alarm1+='0'
            self.alarmTime.configure(text=self.alarm1)
        elif btn in ['Enter']:
            self.checkAlarm()

    def checkAlarm(self):
        if(len(self.alarm1) != 4 and len(self.alarm1) != 5):
            self.alarm1 = ""
            self.alarmTime.configure(text=self.alarm1)
            print("Invalid time listed")
        else:
            self.alarm1Time = int(self.alarm1.split()[0])


app = App()


