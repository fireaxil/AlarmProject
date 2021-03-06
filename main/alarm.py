from tkinter import *
from time import strftime, strptime
from time import sleep
from functools import partial
from builtins import print
import pyglet
import pywapi
from datetime import datetime, timedelta
from PIL import  Image, ImageTk
import pygame
# pyglet.lib.load_library('avbin')
# pyglet.have_avbin =True


#
# things to fix:
#     add 24 hours to alarm when turn off is clicked
#     update button if snooze is clicked and then off is clicked
#

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

        self.nextAlarm = "Next Alarm: Not Set"

        now = datetime.now()
        self.timeText = Label(self.root, text= '{:%H:%M:%S}'.format(now), font=("Helvetica", 40), bg='white')
        self.timeText.pack(side = TOP)


        self.nextAlarmLabel = Label(self.root, text= self.nextAlarm, font=("Helvetica", 40), bg='white')
        self.nextAlarmLabel.pack()

        self.alarmTime = Label(self.root, text="", font=("Helvetica", 40), bg='white')

        self.alarm1 = ""
        self.alarm1Time = ""
        self.alarm1ActualTime = datetime.now()

        self.currentTime = 0

        # self.player = pyglet.media.Player()
        # self.music = pyglet.media.load('BlankSpace.wav')  #pyglet.resource.media('BlankSpace.wma')
        # self.player.queue(self.music)
        pygame.mixer.init()
        pygame.mixer.music.load('BlankSpace.ogg')
        self.isMusicPlaying = 0

        self.canvas = Canvas(self.root, width=100, height=100)

        self.my_images = []
        self.my_images.append(Image.open("res/clear.jpg").resize((110,110), Image.ANTIALIAS))
        self.my_images.append(Image.open("res/cloudy.jpg").resize((110,110), Image.ANTIALIAS))
        self.my_images.append(Image.open("res/drizzle.jpg").resize((110,110), Image.ANTIALIAS))
        self.my_images.append(Image.open("res/snow_showers.jpg").resize((110,110), Image.ANTIALIAS))

        # img = Image.open("res/clear.jpg").resize((100,100), Image.ANTIALIAS)
        # img1 = Image.open("res/cloudy.jpg").resize((100,100), Image.ANTIALIAS)
        self.clear = ImageTk.PhotoImage(self.my_images[0])
        self.cloudy = ImageTk.PhotoImage(self.my_images[1])
        self.rain = ImageTk.PhotoImage(self.my_images[2])
        self.snow = ImageTk.PhotoImage(self.my_images[3])
        # self.image_on_canvas = self.canvas.create_image(50, 50, image=tk_img)

        self.currentWeather = Label(self.root, text=self.getWeather(),font=("Helvetica", 10), bg='white' )
        self.currentWeather.pack()
        self.canvas.pack()

        self.setAlarm = Button(self.root, text= "Set Alarm", command=self.callback,  bg='white')
        self.setAlarm.pack(pady=20)

        self.snoozeButton = Button(self.root, text="SNOOZE",font=("Helvetica", 10), bg='white', command=self.snooze)

        self.offButton = Button(self.root, text= "TURN OFF", font=("Helvetica", 10), bg='white', command=self.turnOff)

        self.root.after(1000, self.update_time)
        self.root.mainloop()

    def update_time(self):
        now = datetime.now()
        self.currentTime = '{:%H:%M}'.format(now)
        self.timeText.configure(text='{:%H:%M:%S}'.format(now))
        self.root.after(1000, self.update_time)
        self.checkAlarmTime()

    def checkAlarmTime(self):
        if str(self.currentTime) == str(self.alarm1Time):
            if self.isMusicPlaying == 0:
                # self.player.play()
                pygame.mixer.music.play()
                self.isMusicPlaying = 1
            self.snoozeButton.pack(side= LEFT)
            self.offButton.pack(side=RIGHT)
            self.setAlarmPack()
            self.timeText.pack()


    def getWeather(self):
        city="Buffalo"
        lookup = pywapi.get_location_ids(city)

        for i in lookup:
            location_id = i
        weather_com_result = pywapi.get_weather_from_weather_com(location_id, units="imperial")
        current_conditions = weather_com_result['current_conditions']['text'].lower()
        if "cloudy" in current_conditions:
            self.canvas.create_image(50, 50, image=self.cloudy)
        elif "rain" in current_conditions :
            self.canvas.create_image(50, 50, image=self.rain)
        elif "clear" in current_conditions :
            self.canvas.create_image(50, 50, image=self.clear)
        elif "snow" in current_conditions :
            self.canvas.create_image(50, 50, image=self.snow)
        else:
            self.canvas.create_image(50, 50, image=self.clear)

        return "Currently the weather is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "°F in " + city + "."


    def callback(self):
        self.setAlarmPack()
        self.alarmTime.pack()
        self.addKeyboard()

    def addKeyboard(self):
        self.lf = LabelFrame(self.root, text="Enter Alarm Time", bd=3,  bg='white')
        self.lf.pack(padx=15, pady=10)
        # typical calculator button layout
        btn_list = [
        '7',  '8',  '9',
        '4',  '5',  '6',
        '1',  '2',  '3',
        '0',  '<-',  'Enter']
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
            btn[n] = Button(self.lf, text=label, width=5, command=cmd,  bg='white')
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
        elif btn in ['<-']:
            self.alarm1 = self.alarm1[:-1]
            # self.alarm1+=':'
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
            # self.alarm1Time = int(self.alarm1.split()[0])
            self.alarm1Time = datetime.strptime(self.alarm1, '%H%M')
            self.alarm1Time = '{:%H:%M}'.format(self.alarm1Time)
            self.nextAlarm = "Next Alarm: " +str(self.alarm1Time)
            self.nextAlarmLabel.configure(text=self.nextAlarm)
            self.timePack()

    def snooze(self):
        timePlusTen = datetime.now() + timedelta(minutes=10)
        self.alarm1Time = '{:%H:%M}'.format(timePlusTen)
        self.nextAlarmLabel.configure(text= "Snoozing until: " + self.alarm1Time)
        self.timePack()
        self.isMusicPlaying = 0
        pygame.mixer.music.rewind()
        pygame.mixer.music.stop()
        self.player.seek(0)
        self.player.pause()
        self.snoozeButton.pack_forget()
        self.offButton.pack_forget()

    def turnOff(self):
        pygame.mixer.music.rewind()
        pygame.mixer.music.stop()
        self.isMusicPlaying = 0
        self.timePack()
        self.player.seek(0)
        self.player.pause()
        self.snoozeButton.pack_forget()
        self.offButton.pack_forget()
        self.nextAlarm = "Next Alarm: Not Set"
        self.alarm1Time = ""
        self.nextAlarmLabel.configure(text=self.nextAlarm)
        print(self.alarm1Time)
    # removes the main widgets
    def setAlarmPack(self):
        self.timeText.pack_forget()
        self.setAlarm.pack_forget()
        self.nextAlarmLabel.pack_forget()
        self.currentWeather.pack_forget()
        self.canvas.pack_forget()
    # removes the keyboard label and widgets
    def timePack(self):
        self.lf.pack_forget()
        self.alarmTime.pack_forget()
        self.timeText.pack()
        self.nextAlarmLabel.pack()
        self.currentWeather.pack()
        self.setAlarm.pack(pady=20)
        self.canvas.pack()


app = App()


