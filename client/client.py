import tensorflow as tf
from tkinter import *
from tkinter import messagebox
import random
import cv2
import numpy as np
from PIL import Image, ImageTk
import time
import threading
import repository
import requests
from apscheduler.schedulers.background import BackgroundScheduler


# --- GAME ---

class MainPage() :
    def __init__(self) :

        self.main = Tk()
        self.main.geometry("800x700")
        self.main.title("Rock Paper Scissor Game")
        self.main.resizable(0,0)

        # ----- Background Image ----
        self.bgframe= Image.open('images/background.png')
        photo = ImageTk.PhotoImage(self.bgframe)
        self.bg_panel = Label(self.main, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill = 'both', expand = 'yes')

        self.login_frame = Frame(self.main, bg = '#fffded', width = '350', height=500)
        self.login_frame.place(x=225,y=80)

        # ---- Login ----

        self.the_user = StringVar()  # used to retrieve input from entry
        self.the_pass = StringVar()

        self.label0 = Label(self.login_frame, text = "Login", font = ("yu gothic ui", 40, 'bold'), bg = '#fffded', fg = 'black')
        self.label0.place(x = 100, y = 40)

        self.label1 = Label(self.login_frame, text = "Username", font = ("yu gothic ui", 16), bg = '#fffded', fg = 'black')
        self.label1.place(x = 56, y = 120)

        self.entry1 = Entry(self.login_frame, textvariable = self.the_user, font = ("yu gothic ui", 14), bg = '#ebedec', fg = 'black')
        self.entry1.place(x = 56, y = 150)

        self.label2 = Label(self.login_frame, text = "Password", font = ("yu gothic ui", 16), bg = '#fffded', fg = 'black')
        self.label2.place(x = 56, y = 200)

        self.entry2 = Entry(self.login_frame, show='*', textvariable = self.the_pass, font = ("yu gothic ui", 14), bg = '#ebedec', fg = 'black')
        self.entry2.place(x = 56, y = 230)

        self.label3 = Button(self.login_frame, text="Login", command = self.validate_login, font = ("yu gothic ui", 18), bg = '#fffded', fg = 'black')
        self.label3.place(x = 140, y = 290)

        self.bad_pass = Label(self.login_frame  , text="Incorrect Username or Password", font = ("yu gothic ui", 12), bg = '#fffded', fg = 'black')

        # --- Register ---

        self.label6 = Label(self.login_frame, text = "Register Here", font = ("yu gothic ui", 15), bg = '#fffded', fg = 'black')
        self.label6.place(x = 120, y = 380)

        self.label7 = Button(self.login_frame, text= "Register", command = self.register_user, font = ("yu gothic ui", 15))
        self.label7.place(x = 130, y = 410)

        self.main.mainloop()

    # Function to validate login credentials
    def validate_login(self):
        res = repository.login(session, self.the_user.get(), self.the_pass.get())
        self.the_pass.set("")
        # Check if username and password are correct
        if res == 200:
            self.main.destroy()
            LoadingPage()
        else:
            self.bad_pass.place(x = 50, y = 340)
    
    def register_user(self):
        username = self.the_user.get()
        password = self.the_pass.get()

        self.the_pass.set("")

        res = repository.register(session, username, password)

        if res[0] == 200:
            messagebox.showinfo("Success", res[1])
        
        else :
            messagebox.showerror("Error", res[1])


class LoadingPage() :
    def __init__(self) :
        self.load = Tk()
        self.load.geometry("800x700")
        self.load.title("Rock Paper Scissor Game")
        self.load.resizable(0,0)

        # ----- Background Image ----
        self.bgframe = Image.open('images/background.png')
        photo = ImageTk.PhotoImage(self.bgframe)
        self.bg_panel = Label(self.load, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill = 'both', expand = 'yes')

        self.Label0L = Label(self.load, text = "Waiting for other players...", font = ("yu gothic ui", 35, 'bold'), bg = '#ebe4d3', fg = 'black')
        self.Label0L.place(x = 40, y = 70)

        loading_timer = threading.Timer(3, self.fun)
        loading_timer.start()

        self.load.mainloop()

    def fun(self) :
        self.Label0L.destroy()
        Game(self.load)

class Game :
    def __init__(self, master):

        self.master = master
        self.master.geometry("800x700")
        self.master.title("Lets Play!")
        self.master.resizable(0,0)

        # ----- Background Image ----
        self.bgframe= Image.open('images/background.png')
        self.photo = ImageTk.PhotoImage(self.bgframe)
        self.bg_panel = Label(self.master, image=self.photo)
        self.bg_panel.image = self.photo
        self.bg_panel.pack(fill = 'both', expand = 'yes')

        # ------ Labels and Buttons ------

        self.frame = Frame(self.master, bg = '#ebe4d3', width = '610', height=180)
        self.frame.place(x = 100, y = 60)

        self.GLabel = Label(self.master, text="Rock Paper Scissor", font = ("yu gothic ui", 40, 'bold'), bg = '#ebe4d3', fg = 'black')
        self.GLabel.place(x = 100, y = 60) #300

        self.player1_score_label = Label(self.master, text="Wins: 0", font = ("yu gothic ui", 20), bg = '#ebe4d3', fg = 'black')
        self.player1_score_label.place(x = 210, y = 150)

        self.ties_label = Label(self.master, text="Ties: 0", font = ("yu gothic ui", 20), bg = '#ebe4d3', fg ='black')
        self.ties_label.place(x = 340, y = 150)

        self.player2_score_label = Label(self.master, text="Losses: 0", font = ("yu gothic ui", 20), bg = '#ebe4d3',  fg = 'black')
        self.player2_score_label.place(x = 450, y = 150)

        self.result_label = Label(self.master, text="", font="normal 20 bold", bg="white", width=15, borderwidth=2, relief="solid")
        self.result_label.pack(pady=20)

        
        self.b1 = Button(self.master, text="Rock", font= ("yu gothic ui", 15))
        self.b2 = Button(self.master, text="Paper", font=("yu gothic ui", 15))
        self.b3 = Button(self.master, text="Scissors", font=("yu gothic ui", 15))

        self.b4 = Button(self.master, text="Play!", command = self.select, font=("yu gothic ui", 15))
        self.b4.place(x = 550, y = 200)

        self.b1.place(x = 250, y = 200)
        self.b2.place(x = 330, y = 200)
        self.b3.place(x = 420, y = 200)

        #Score variables
        self.player1_score = 0
        self.player2_score = 0

        self.current_choice = ""

        # Load the model. This should be located within the same directory and labeled the same as it was in the original notebook.
        self.model = tf.keras.models.load_model("./rock_paper_scissors_mobilenet_v2.h5")
        self.labels = ['rock', 'paper', 'scissors']

        self.width = 128
        self.height = 128

        # Add Labels, Frames, and Buttons
        self.video_label = Label(self.master, width=400, height=400)
        self.video_label.place(x = 220, y = 250)

        # Start capturing video frames
        self.cap = cv2.VideoCapture(0)
        self.update_frame()
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Flip frame horizontally
            frame_tensor = tf.expand_dims(frame, 0)
            image = tf.cast(frame_tensor, tf.float32)
            image = image/255
            image = tf.image.resize(image, [self.width, self.height])
            result = self.model.predict(image)
            inferred_result = np.argmax(result)
            confidence = result[0][inferred_result]

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            if confidence < 0.5:
                print("Rejected result - confidence too low.")
            else:
                self.b1.configure(font='sans 16', fg='black')
                self.b2.configure(font='sans 16', fg='black')
                self.b3.configure(font='sans 16', fg='black')
                
                if self.labels[inferred_result] == 'rock':
                    self.b1.configure(font='sans 16 bold', fg='red')
                    self.current_choice = "rock"
                    print()
                elif self.labels[inferred_result] == 'paper':
                    self.b2.configure(font='sans 16 bold', fg='red')
                    self.current_choice = "paper"
                else:
                    self.b3.configure(font='sans 16 bold', fg='red')
                    self.current_choice = "scissors"
                # TODO: Switch to button from scheduler
                # make_choice_job.modify(args=(username, labels[inferred_result]))
                # print(f"Inferred result: {self.labels[inferred_result]} with confidence {confidence*100}%")
            self.master.after(10, self.update_frame)


    # Update score function
    def update_score(self):
        res = repository.retrieve_stats(session)
        if res != None:
            self.player1_score_label.config(text=f"Wins: {res['wins']}")
            self.player2_score_label.config(text=f"Losses: {res['losses']}")
        # ties key also exists

    
    def select(self):
        print("here")
        if self.current_choice == "":
            print("LOOOK HERE", self.current_choice)
            return
        res = repository.make_choice(session, self.current_choice)

        loading_screen = Toplevel()
        loading_screen.title("Loading...")
        loading_screen.geometry("200x100")

        def check_and_destroy():
            if repository.check_queue(session):
                loading_screen.destroy()
                self.update_score()
            else:
                loading_screen.after(100, check_and_destroy)
    
        label = Label(loading_screen, text="Loading...")
        label.pack(pady=30)

        loading_screen.after(100, check_and_destroy)

# --- MAIN WINDOW ---
global username 
session = requests.session()
MainPage()
cv2.destroyAllWindows()