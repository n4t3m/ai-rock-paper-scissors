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

        self.label7 = Button(self.login_frame, text= "Register", font = ("yu gothic ui", 15))
        self.label7.place(x = 130, y = 410)

        self.main.mainloop()

    # Function to validate login credentials
    def validate_login(self):
        res = repository.login(session, self.the_user, self.the_pass)
        # Check if username and password are correct
        if res == 200:
            self.main.destroy()
            LoadingPage()
        else:
            self.bad_pass.place(x = 55, y = 330)
    
    def register_user(self):
        username = self.the_user.get()
        password = self.the_user.get()

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

        self.Label0L = Label(self.load, text = "Waiting for other players...", font = ("yu gothic ui", 40, 'bold'), bg = '#ebe4d3', fg = 'black')
        self.Label0L.place(x = 70, y = 70)

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
        photo = ImageTk.PhotoImage(self.bgframe)
        self.bg_panel = Label(self.master, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill = 'both', expand = 'yes')

        # ------ Labels and Buttons ------

        frame = Frame(self.master, bg = '#ebe4d3', width = '580', height=180)
        frame.place(x = 125, y = 60)

        self.GLabel = Label(self.master, text="Rock Paper Scissor", font = ("yu gothic ui", 40, 'bold'), bg = '#ebe4d3', fg = 'black')
        self.GLabel.place(x = 125, y = 60) #300

        player1_score_label = Label(self.master, text="Player 1: 0", font = ("yu gothic ui", 20), bg = '#ebe4d3', fg = 'black')
        player1_score_label.place(x = 200, y = 150)

        vs_label = Label(self.master, text="VS", font = ("yu gothic ui", 20), bg = '#ebe4d3', fg ='black')
        vs_label.place(x = 380, y = 200)

        player2_score_label = Label(self.master, text="Player 2: 0", font = ("yu gothic ui", 20), bg = '#ebe4d3',  fg = 'black')
        player2_score_label.place(x = 420, y = 150)

        result_label = Label(self.master, text="", font="normal 20 bold", bg="white", width=15, borderwidth=2, relief="solid")
        result_label.pack(pady=20)

        
        b1 = Button(self.master, text="Rock", font= ("yu gothic ui", 15))
        b2 = Button(self.master, text="Paper", font=("yu gothic ui", 15))
        b3 = Button(self.master, text="Scissor", font=("yu gothic ui", 15))

        b1.place(x = 290, y = 200)
        b2.place(x = 370, y = 200)
        b3.place(x = 455, y = 200)

        #Score variables
        self.player1_score = 0
        self.player2_score = 0

        video = cv2.VideoCapture(-1)

        if not video.isOpened():
            raise IOError("Camera not enabled")

        # Load the model. This should be located within the same directory and labeled the same as it was in the original notebook.
        model = tf.keras.models.load_model("./rock_paper_scissors_mobilenet_v2.h5")
        labels = ['rock', 'paper', 'scissors']

        width = 128
        height = 128

        def capture_video():
            cap = cv2.VideoCapture(0)

            scheduler = BackgroundScheduler()
            make_choice_job = scheduler.add_job(repository.make_choice, args=(session, ""), trigger="interval", seconds=10)
            scheduler.start()
            
            def update_frame():
                cap = cv2.VideoCapture(0)

                ret, frame = cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)  # Flip frame horizontally
                    frame_tensor = tf.expand_dims(frame, 0)
                    image = tf.cast(frame_tensor, tf.float32)
                    image = image/255
                    image = tf.image.resize(image, [width, height])
                    result = model.predict(image)
                    inferred_result = np.argmax(result)
                    confidence = result[0][inferred_result]

                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2image)
                    imgtk = ImageTk.PhotoImage(image=img)
                    video_label.imgtk = imgtk
                    video_label.configure(image=imgtk)
                    if confidence < 0.5:
                        print("Rejected result - confidence too low.")
                    else:
                        b1.configure(font='sans 16', fg='black')
                        b2.configure(font='sans 16', fg='black')
                        b3.configure(font='sans 16', fg='black')
                        
                        if labels[inferred_result] == 'rock':
                            b1.configure(font='sans 16 bold', fg='red')
                        elif labels[inferred_result] == 'paper':
                            b2.configure(font='sans 16 bold', fg='red')
                        else:
                            b3.configure(font='sans 16 bold', fg='red')
                        # TODO: Switch to button from scheduler
                        # make_choice_job.modify(args=(username, labels[inferred_result]))
                        print(f"Inferred result: {labels[inferred_result]} with confidence {confidence*100}%")

                video_label.after(10, update_frame)

            update_frame()

        # Update score function
        def update_score(player):
            print("Update")


        # Add Labels, Frames, and Buttons


        video_label = Label(self.master, width=400, height=400)
        video_label.place(x = 220, y = 250)

        # Start capturing video frames
        capture_video()
        self.master.mainloop()


# --- MAIN WINDOW ---
global username 
session = requests.session()
MainPage()
cv2.destroyAllWindows()