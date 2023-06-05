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


def register_user():
    print("Do Something")

# Function to validate login credentials
def validate_login():
    global username, password
    username = username_entry.get()
    password = password_entry.get()

    repository.login(username, password)

    # Check if username and password are correct
    if username == "a" and password == "p":
        login_frame.pack_forget()  # Hide the login frame
        show_loading_screen()
    else:
        messagebox.showerror("Login Error", "Invalid username or password")

def show_loading_screen():
    Label(loading_frame, text="WAITING FOR OTHER PLAYERS...", font="normal 20 bold").pack(pady=50)
    loading_frame.pack()  # Show the loading frame
    loading_timer = threading.Timer(3, show_game_interface)
    loading_timer.start()

def show_game_interface():
    loading_frame.pack_forget()  # Hide the loading frame

    # Create game frame
    game_frame = Frame(root)

    # Score variables
    player1_score = 0
    player2_score = 0

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

        repository.login(username, password)

        scheduler = BackgroundScheduler()
        make_choice_job = scheduler.add_job(repository.make_choice, args=(username, ""), trigger="interval", seconds=10)
        scheduler.start()
        
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
                    make_choice_job.modify(args=(username, labels[inferred_result]))
                    print(f"Inferred result: {labels[inferred_result]} with confidence {confidence*100}%")

            video_label.after(10, update_frame)

        update_frame()

    # Update score function
    def update_score(player):
        print("Update")


    # Add Labels, Frames, and Buttons
    Label(root, text="Rock Paper Scissor", font="normal 20 bold", fg="blue").pack(pady=20)

    frame = Frame(game_frame)
    frame.pack()

    player1_score_label = Label(frame, text="Player 1: 0", font=10)
    vs_label = Label(frame, text="VS", font="normal 10 bold")
    player2_score_label = Label(frame, text="Player 2: 0", font=10)

    player1_score_label.pack(side=LEFT)
    vs_label.pack(side=LEFT)
    player2_score_label.pack()

    result_label = Label(game_frame, text="", font="normal 20 bold", bg="white", width=15, borderwidth=2, relief="solid")
    result_label.pack(pady=20)

    frame1 = Frame(game_frame)
    frame1.pack()

    
    b1 = Button(frame1, text="Rock", font='sans 16', width=7)
    b2 = Button(frame1, text="Paper", font='sans 16', width=7)
    b3 = Button(frame1, text="Scissor", font='sans 16', width=7)

    b1.pack(side=LEFT, padx=10)
    b2.pack(side=LEFT, padx=10)
    b3.pack(padx=10)

    video_label = Label(game_frame, width=400, height=400)
    video_label.pack()

    # Start capturing video frames
    capture_video()

    game_frame.pack()

# Create main window
root = Tk()
root.geometry("800x600")
root.title("Rock Paper Scissor Game")

# Create login frame
login_frame = Frame(root)

Label(login_frame, text="Username:").pack()
username_entry = Entry(login_frame)
username_entry.pack()

Label(login_frame, text="Password:").pack()
password_entry = Entry(login_frame, show="*")
password_entry.pack()

Button(login_frame, text="Login", command=validate_login).pack(side=LEFT, padx=10)
Button(login_frame, text="Register", command=register_user).pack(side=LEFT, padx=10)
# Create loading frame
loading_frame = Frame(root)

# Show the login frame
login_frame.pack()

# Execute Tkinter
root.mainloop()
