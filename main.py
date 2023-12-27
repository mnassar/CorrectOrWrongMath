import tkinter as tk
from PIL import Image, ImageTk
from scoreboard import *
# import simpleaudio as sa
import winsound
import re
import math


# import tkinter.font as tkFont

import random
import time

class game(tk.Tk):
    def __init__(self):
        self.username = "Guest"
        self.started = False
        self.quitted = False
        self.nb_correct = {
            "level 1": 0,
            "level 2": 0,
            "level 3": 0,
            "level 4": 0,
            "level 5": 0,
            "level 6": 0,
            "level 7": 0,
            "level 8": 0,
            "level 9": 0
        }
        self.nb_total = 0
        self.limit = 10
        self.curr_mode = "level 1"
        self.modes = {
            "level 1":5,
            "level 2":10,
            "level 3":50,
            "level 4":100,
            "level 5":250,
            "level 6":400,
            "level 7":500,
            "level 8":1000,
            "level 9":5000
        }

        self.locks = {
            "level 1": False,
            "level 2": True,
            "level 3": True,
            "level 4": True,
            "level 5": True,
            "level 6": True,
            "level 7": True,
            "level 8": True,
            "level 9": True
        }

        # fontStyle = tkFont.Font(family="Lucida Grande", size=30)
        labeltxt = "Welcome to My Math Questions \n You can do math in here!"
        # with open("banner.txt", 'r') as f:
        # labeltxt = f.read()

        tk.Tk.__init__(self)
        self.configure(background='blue')
        self.title("Correct Math or Wrong Math?")
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.geometry(str(self.w)+'x'+str(self.h)) #'600x400'
        # self.grid_rowconfigure(20)
        # self.grid_columnconfigure(10)
        # self.attributes('-fullscreen', True)
        img = Image.open('winter.jpg')
        new_img = img.resize((self.w, self.h))
        bg_img = ImageTk.PhotoImage(new_img)
        # bg_img = ImageTk.PhotoImage(img)

        background_label = tk.Label(self, image=bg_img)
        background_label.image = bg_img
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        bannerLabel = tk.Label(self, text=labeltxt, width=50, font=("Courrier", 24), background='green')
        bannerLabel.pack()
        # bannerLabel.grid(row=0, column=0)

        self.scoreboard = populate()
        scoreboard_Str = "Leaderboard \n __________ \n"
        for k, v in self.scoreboard.items():
            scoreboard_Str += k + "\t" + str(v) + "\n"

        self.scoreboardLabel = tk.Label(self, foreground='blue', text=scoreboard_Str, font=("courrier", 20))
        self.scoreboardLabel.place(relx=0.8, rely=0.5)


        self.usernameLabel = tk.Label(self, foreground='blue', text="enter username", font=("courrier", 20))
        self.usernameLabel.pack()
        self.usernameEntry = tk.Entry(font=("Courrier", 30))
        self.usernameEntry.pack()
        self.usernameEntry.focus_set()
        self.usernameEntry.bind('<Return>', self.setUsername)

        self.startButton = tk.Button(text="start", background='yellow', command=self.run, width=10, height=3, font=("Courrier", 30))
        self.startButton.pack()

        self.settingsImg = tk.PhotoImage(file="settings.gif").subsample(3,3)
        self.settingsButton = tk.Button(image=self.settingsImg, command=self.settings)
        self.settingsButton.place(relx=0, rely=1, anchor='sw')
        self.settings = None

        self.achievementFr = None
        self.musicPlaying = False
        self.musicButton = tk.Button(text="Music", background='gray', command=self.play, width=10, height=3,
                                     font=("Courrier", 30), anchor=tk.CENTER)
        self.musicButton.place(relx=0.9, rely=0.1, anchor='ne')
        self.achievement("Welcome!", "Achievement")

        self.quitButton = tk.Button(text="Quit", background='green', foreground='purple', command=self.quit, width=7, height=2,
                                    font=("Courrier", 20), anchor=tk.CENTER)
        self.quitButton.place(relx=0.5, rely=0.8)
    def writeYourOwn(self):

        self.equation = tk.Entry(font=("Courrier", 30))
        self.equation.place(relx=0, rely=0.5)
        self.equation.focus_set()
        self.equation.bind('<Return>', self.setEquation)

    def setUsername(self, event):
        self.username = event.widget.get()
        print (self.username)
        if not self.username in self.scoreboard:
            self.scoreboard[self.username] = 0
        self.usernameEntry.destroy()
        self.usernameLabel.destroy()
        self.usernameLabel = tk.Label(self, text = "*" + self.username + "*", font=("Lucida", 20), background="black", foreground="white")
        self.usernameLabel.place(relx=0.9, rely=0.9, anchor='nw')


    def setEquation(self, event):
        ans = event.widget.get()
        try:
            tokens = ans.split()
            z = int(tokens[0])
            y = int(tokens[2])
            op = tokens[1]
            x = eval(ans)
            print(x)
        except ():
            return
        else:
            print (x,y,z)
            self.question.config(text=str(z) + op + str(y) + "=" + "?")
            self.ansTextBox.focus_set()
            self.ansTextBox.delete(0, tk.END)
            self.ansTextBox.icursor(0)
            # self.ansTextBox.unbind('<Return>')
            self.ansTextBox.bind('<Return>', lambda event: self.show_msg(event, x, y, z, op))
            self.equation.destroy()


    def settings(self):
        if self.settings != None:
            self.settings.destroy()
            self.scrollbar.destroy()
            self.settings = None
            return
        listSettings = tk.Variable(value= list(self.modes.keys()))
        self.settings = tk.Listbox(self, listvariable=listSettings, height=8,
                                   selectmode=tk.SINGLE, background="black", foreground="white"
                                   , font=("Lucida", 20))

        self.scrollbar = tk.Scrollbar(self)

        self.settings.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.settings.yview)

        self.settings.place(relx=0, rely=1, anchor='sw')
        self.scrollbar.pack(side=tk.LEFT, fill=tk.BOTH)
        self.settings.pack(side=tk.LEFT)
        self.settings.bind('<<ListboxSelect>>', self.changeMode)

    def changeMode(self, event):
        self.mode = self.settings.curselection()
        self.curr_mode = self.settings.get(self.mode)
        if self.settings.get(self.mode) in self.modes and not self.locks[self.settings.get(self.mode)]:
            self.limit = self.modes[self.settings.get(self.mode)]
        else:
            self.achievement(self.settings.get(self.mode) + " is locked!", "Error")

        self.settings.destroy()
        self.scrollbar.destroy()
        self.settings = None
        if self.started:
            self.run1()

        # self.settings.destroy()

    def achievement(self, msg, text):
        if self.achievementFr != None:
            self.achievementFr.destroy()
        self.achievementFr = tk.Frame(self, background="blue", width=10, height=3)
        self.achievementFr.place(relx=0., rely=0., anchor='nw')
        self.AchTitle = tk.Label(self.achievementFr, text=text, font=("courrier", 10))
        self.AchTitle.pack()
        self.firstAch = tk.Label(self.achievementFr, foreground="red", text=msg, font=("courrier",30))
        self.firstAch.pack()
        self.after(5000, self.disappear)
        self.frame = tk.Frame()
        self.frame.pack()
    def disappear(self):
        self.achievementFr.destroy()
    def show_msg(self, event, x, y, z, op):
        # ans = event.widget.get("1.0", "end-1c")
        ans = event.widget.get()
        # print(ans)

        try:
            if int(ans) == x:
                print("correct")
                self.congratz.config(text=random.choice(["Awsome!", "Perfect", "You're smart!", "Correct",
                                                   "You are great at math!", "You must be so smart",
                                                   "You're a genius!",
                                                   "you are killing it!"]), font=("Courrier, 20"), fg='green')
                self.nb_correct[self.curr_mode] += 1
                if self.nb_correct[self.curr_mode] == 1:
                    self.achievement("First Correct Answer!", "Achievement")
                if self.nb_correct[self.curr_mode] == 5:
                    print ("level completed")
                    print(self.curr_mode)
                    print(self.nb_correct)

                    self.achievement("Level " + str(int(self.curr_mode[-1]) + 1) + " is unlocked!", "Achievement")
                    self.locks[self.curr_mode[:-1] + str(int (self.curr_mode[-1]) + 1)] = False
                    self.curr_mode = "level " + str(int(self.curr_mode[-1]) + 1)
                    self.limit = self.modes[self.curr_mode]
            else:
                s = random.choice(["You need to practise, Bro!",
                                   "Wrong!",
                                   "Try again!",
                                   "Not that number!",
                                   "nope",
                                   "no but a sus answer!",
                                   "trash"])
                self.congratz.config(text="Sorry, " + str(z) + op + str(y) + "=" + str(x) + "\n" + s,
                                     font=("Courrier, 20"), fg='red')
                if self.nb_total - self.nb_correct[self.curr_mode] == 1:
                    self.achievement("First Wrong Answer!", "Achievement")
            self.run1()
        except:
            pass


    def run(self):
        self.startButton.destroy()
        self.started=True
        self.t_start = time.time()
        x, y, z, op = self.generate_question()
        self.question = tk.Label(self.frame, text=str(z) + op + str(y) + "=" + "?", font=("Courrier, 20"))
        self.question.pack()
        self.nb_total += 1
        # self.ansTextBox = tk.Text(self.frame, width=9, height=2, font=("Courrier, 20"))
        self.ansTextBox = tk.Entry(self.frame, width=9, font=("Courrier, 20"))
        self.ansTextBox.pack()
        self.ansTextBox.focus_set()
        self.ansTextBoxBindID = self.ansTextBox.bind('<Return>', lambda event: self.show_msg(event, x, y, z, op))
        self.congratz = tk.Label(self.frame, text="")
        self.congratz.pack()


        # self.WriteYourOwnQ = tk.Button(text="Write your \n own question!", background='gray', font=("Courrier",20),
        #                                width=12, anchor='w', command=self.writeYourOwn)
        # self.WriteYourOwnQ.place(relx=0, rely=0.4)


    def run1(self):
        x, y, z, op = self.generate_question()

        self.question.config(text=str(z) + op + str(y) + "=" + "?")

        self.nb_total += 1
        # self.ansTextBox.delete('1.0', tk.END)


        self.ansTextBoxBindID = self.ansTextBox.bind('<Return>', lambda event: self.show_msg(event, x, y, z, op))
        self.focus_set()
        self.frame.focus_set()
        self.ansTextBox.focus_set()

        self.ansTextBox.delete(0, tk.END)
        self.ansTextBox.icursor(0)
        print(self.focus_get())
    def generate_question(self):
        z = random.randrange(1,self.limit)
        y = random.randrange(1,self.limit)
        choice = random.randrange(1,6)


        if choice == 1:
            return z, y, z-y, "+"
        elif choice == 2:
            return z, y, z+y, "-"
        elif choice == 3:
            return z, y, z*y, "/"
        elif choice == 4:
            return y * (z//y), z//y, y, "*"
        else:
            x = int(math.sqrt(z))
            return x, ")", "sqrt(", str(x * x)

    def quit(self):
        if self.quitted:
            return
        self.quitted = True
        self.nb_total -= 1
        correct_values = sum(self.nb_correct.values())
        tk.Label(self.frame, text="You got " + str(correct_values) + "/" + str(self.nb_total)
                                  + " correct answers",
                 font=("Lucida Grande", 30), fg='blue').pack()
        update_scoreboard(self.username, correct_values, self.scoreboard)
        tk.Label(self.frame, text="You got " + str(self.nb_total) + " questions in total",
                 font=("Lucida Grande", 30), fg='brown').pack()
        t_end = time.time()
        minutes = (t_end - self.t_start) // 60
        seconds = (t_end - self.t_start) % 60
        tk.Label(self.frame, text="Total time: {} minutes and {:.2f} seconds!".format(minutes, seconds),
                 font=("Lucida Grande", 30), fg='blue').pack()
        tk.Label(self.frame, text="Thank you for playing! Good bye!", font=("Lucida Grande", 20), fg='brown').pack()
        self.question.destroy()
        self.ansTextBox.destroy()
        self.congratz.destroy()
        # input("Press any key to exit!")

    def play(self):
        if self.musicPlaying == False:
            filename = 'No Indication.wav'
            winsound.PlaySound(filename, winsound.SND_ASYNC) # + winsound.SND_LOOP)
            self.musicPlaying = True
        else:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.musicPlaying = False



if __name__ == '__main__':

    # wave_obj = sa.WaveObject.from_wave_file(filename)
    # play_obj = wave_obj.play()
    g = game()

    g.mainloop()
    # play_obj.wait_done()  # Wait until sound has finished playing

# TODO
# Make a settings button with width=3 height=1 bg=white fg=black
