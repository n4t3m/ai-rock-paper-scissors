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
from apscheduler.schedulers.background import BackgroundScheduler


# --- LOGIN / REGISTERATION ---

def register_user():
    print("Do Something")


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
        self.label0.place(x = 125, y = 40)

        self.label1 = Label(self.login_frame, text = "Username", font = ("yu gothic ui", 18), bg = '#fffded', fg = 'black')
        self.label1.place(x = 56, y = 120)

        self.entry1 = Entry(self.login_frame, textvariable = self.the_user, font = ("yu gothic ui", 18), bg = '#ebedec', fg = 'black')
        self.entry1.place(x = 56, y = 150)

        self.label2 = Label(self.login_frame, text = "Password", font = ("yu gothic ui", 18), bg = '#fffded', fg = 'black')
        self.label2.place(x = 56, y = 200)

        self.entry2 = Entry(self.login_frame, show='*', textvariable = self.the_pass, font = ("yu gothic ui", 18), bg = '#ebedec', fg = 'black')
        self.entry2.place(x = 56, y = 230)

        self.label3 = Button(self.login_frame, text="Login", command = self.validate_login, font = ("yu gothic ui", 18), bg = '#fffded', fg = 'black')
        self.label3.place(x = 140, y = 290)

        self.bad_pass = Label(self.login_frame  , text="Incorrect Username or Password", font = ("yu gothic ui", 16), bg = '#fffded', fg = 'black')

        # --- Register ---

        self.label6 = Label(self.login_frame, text = "Register Here", font = ("yu gothic ui", 15), bg = '#fffded', fg = 'black')
        self.label6.place(x = 135, y = 380)

        self.label7 = Button(self.login_frame, text= "Register", font = ("yu gothic ui", 15))
        self.label7.place(x = 135, y = 410)

        self.main.mainloop()

    # Function to validate login credentials
    def validate_login(self):
        repository.login(self.the_user, self.the_pass)
        # Check if username and password are correct
        if self.the_user.get() == "a" and self.the_pass.get() == "p":
            self.main.destroy()
            LoadingPage()
        else:
            self.bad_pass.place(x = 55, y = 330)


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

        self.Label0L = Label(self.load, text = "Waiting for other players...", font = ("yu gothic ui", 50, 'bold'), bg = '#fffded', fg = 'black')
        self.Label0L.place(x = 120, y = 70)

        loading_timer = threading.Timer(3, self.fun)
        loading_timer.start()

        self.load.mainloop()

    def fun(self) :
        print("In")
        self.Label0L.destroy()
        Game(self.load)

class Game :
    def __init__(self, master):

        self.master = master
        self.master.geometry("1000x800")
        self.master.title("Changed")
        self.master.resizable(0,0)

        # ----- Background Image ----
        self.bgframe= Image.open('images/background.png')
        photo = ImageTk.PhotoImage(self.bgframe)
        self.bg_panel = Label(self.master, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill = 'both', expand = 'yes')

        # ------ Labels and Buttons ------
        self.GLabel = Label(self.master, text="Rock Paper Scissor", font = ("yu gothic ui", 50, 'bold'), bg = '#fff9ff', fg = 'black')
        self.GLabel.place(x = 300, y = 70)

        frame = Frame(self.master, bg = '#fffded', width = '350', height=500)
        frame.place(x = 40, y = 60)
        frame.pack()

        player1_score_label = Label(frame, text="Player 1: 0", font=10)
        vs_label = Label(frame, text="VS", font="normal 10 bold")
        player2_score_label = Label(frame, text="Player 2: 0", font=10)

        player1_score_label.place(x = 120, y = 40)
        vs_label.place(x = 120, y = 70)
        player2_score_label.place(x = 120, y = 20)

        #Score variables
        self.player1_score = 0
        self.player2_score = 0

        video = cv2.VideoCapture(0)

        if not video.isOpened():
            raise IOError("Camera not enabled")

        # Load the model. This should be located within the same directory and labeled the same as it was in the original notebook.
        model = tf.keras.models.load_model("./rock_paper_scissors_mobilenet_v2.h5")
        labels = ['rock', 'paper', 'scissors']

        width = 128
        height = 128

        def capture_video():
            cap = cv2.VideoCapture(0)

            # repository.login(username, password)

            # scheduler = BackgroundScheduler()
            # make_choice_job = scheduler.add_job(repository.make_choice, args=(username, ""), trigger="interval", seconds=10)
            # scheduler.start()
            
            def update_frame():
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
                        # make_choice_job.modify(args=(username, labels[inferred_result]))
                        print(f"Inferred result: {labels[inferred_result]} with confidence {confidence*100}%")

                video_label.after(10, update_frame)

            update_frame()

        # Update score function
        def update_score(player):
            print("Update")


        # Add Labels, Frames, and Buttons
        



        # result_label = Label(self.master, text="", font="normal 20 bold", bg="white", width=15, borderwidth=2, relief="solid")
        # result_label.pack(pady=20)

        # frame1 = Frame(self.master)
        # frame1.pack()

        
        # # b1 = Button(frame1, text="Rock", font='sans 16', width=7)
        # # b2 = Button(frame1, text="Paper", font='sans 16', width=7)
        # # b3 = Button(frame1, text="Scissor", font='sans 16', width=7)

        # # b1..place(x = 120, y = 70)
        # b2.place(x = 120, y = 70)
        # b3.pack(padx=10)

        video_label = Label(self.master, width=400, height=400)
        video_label.pack()

        # Start capturing video frames
        capture_video()


# --- MAIN WINDOW ---
LoadingPage()
cv2.destroyAllWindows()

# Create login frame
# login_frame = Frame(root)

# Label(login_frame, text="Username:").pack()
# username_entry = Entry(login_frame)
# username_entry.pack()

# Label(login_frame, text="Password:").pack()
# password_entry = Entry(login_frame, show="*")
# password_entry.pack()

# Button(login_frame, text="Login", command=validate_login).pack(side=LEFT, padx=10)
# Button(login_frame, text="Register", command=register_user).pack(side=LEFT, padx=10)
# # Create loading frame
# loading_frame = Frame(root)

# # Show the login frame
# login_frame.pack()

# # Execute Tkinter
# root.mainloop()
