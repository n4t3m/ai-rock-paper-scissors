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

global username_entry, password_entry

def register_user():
    global username_entry, password_entry
    username = username_entry.get()
    password = password_entry.get()

    res = repository.register(session, username, password)

    # Check if username and password are correct
    if res[0] == 200:
        messagebox.showinfo("Success", res[1])
    else:
        messagebox.showerror("Error", res[1])

# Function to validate login credentials
def validate_login():
    global username_entry, password_entry
    username = username_entry.get()
    password = password_entry.get()

    res = repository.login(session, username, password)

    # Check if username and password are correct
    if res == 200 or username == 'a':
        login_frame.pack_forget()  # Hide the login frame
        show_game_interface()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def show_loading_screen():
    Label(loading_frame, text="WAITING FOR OTHER PLAYERS...", font="normal 20 bold").pack(pady=50)
    loading_frame.pack()  # Show the loading frame

def show_game_interface():
    loading_frame.pack_forget()  # Hide the loading frame

    # Create game frame
    game_frame = Frame(root)

    video = cv2.VideoCapture(0)

    if not video.isOpened():
        raise IOError("Camera not enabled")

    # Load the model. This should be located within the same directory and labeled the same as it was in the original notebook.
    model = tf.keras.models.load_model("client/rock_paper_scissors_mobilenet_v2.h5")
    labels = ['rock', 'paper', 'scissors']

    width = 128
    height = 128

    match_history = repository.get_sats(session)

    def capture_video():

        scheduler = BackgroundScheduler()
        make_choice_job = scheduler.add_job(repository.make_choice, args=(session, ""), trigger="interval", seconds=10)
        scheduler.start()
        
        def update_frame():
            ret, frame = video.read()
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
                    make_choice_job.modify(args=(session, labels[inferred_result]))
                    print(f"Inferred result: {labels[inferred_result]} with confidence {confidence*100}%")

            video_label.after(10, update_frame)

        update_frame()

    def select_button():
        if b1.cget('fg') == 'red':
            res = repository.make_choice(session, "rock")
        elif b2.cget('fg') == 'red':
            res = repository.make_choice(session, "paper" )
        elif b3.cget('fg') == 'red':
            res = repository.make_choice(session, "scissors")
            
        video.release()
        cv2.destroyAllWindows()
        game_frame.pack_forget()
        show_loading_screen()
        get_results()
    
    def get_results():
        while True:
            new_match_history = repository.get_sats(session)

            if new_match_history != NONE:
                if new_match_history['matches'][0] and match_history['matches'][0] and new_match_history['matches'][0]['id'] == match_history['matches'][0]['id']:
                    loading_frame.pack_forget()
                    opp = new_match_history['matches'][0]["opponent_name"]
                    if new_match_history['matches'][0]['result'] == 'Win':
                        result_label = Label(root, text="Win! You won over {}".format(new_match_history['matches'][0]['opponent_name']), font="normal 30 bold", bg="white", borderwidth=2, relief="solid")
                        result_label.pack(pady=20)
                    elif new_match_history['matches'][0]['result'] == 'Tie':
                        result_label = Label(root, text="You tied with {}".format(new_match_history['matches'][0]['opponent_name']), font="normal 30 bold", bg="white", borderwidth=2, relief="solid")
                        result_label.pack(pady=20)
                    else:
                        result_label = Label(root, text="You lost to {}".format(new_match_history['matches'][0]['opponent_name']), font="normal 30 bold", bg="white", borderwidth=2, relief="solid")
                        result_label.pack(pady=20)
                break
        Button(root, text= "Play Again!").pack()
        Button(root, text= "Logout", command=logout).pack()

    def logout():
        for widget in root.winfo_children():
            widget.pack_forget()
        repository.logout(session)
        username_entry.configure(text = "")
        password_entry.configure(text = "")
        login_frame.pack()



        
    # Add Labels, Frames, and Buttons
    prev = Button(root, text="View Previous Games", font='sans 16', command=select_button).pack(anchor="ne")
    title = Label(root, text="Rock Paper Scissor", font="sans 20 bold", fg="blue").pack(pady=20)

    frame = Frame(game_frame)
    frame.pack()

    losses = match_history['losses']
    wins = match_history['wins']
    ties = match_history['ties']

    player1_score_label = Label(frame, text="{}:".format(username_entry.get()), font="sans 15")
    vs_label = Label(frame, text="Wins: {}   Ties: {}   Losses: {}".format(wins, losses, ties), font="sans 15")
    

    player1_score_label.pack(side=LEFT)
    vs_label.pack(side=LEFT)
    

    # result_label = Label(game_frame, text="", font="normal 20 bold", bg="white", width=15, borderwidth=2, relief="solid")
    # result_label.pack(pady=20)

    frame1 = Frame(game_frame)
    frame1.pack()

    
    b1 = Button(frame1, text="Rock", font='sans 16', width=7)
    b2 = Button(frame1, text="Paper", font='sans 16', width=7)
    b3 = Button(frame1, text="Scissor", font='sans 16', width=7)


    b1.pack(side=LEFT, padx=10)
    b2.pack(side=LEFT, padx=10)
    b3.pack(padx=10)

    video_label = Label(game_frame, width= 500, height=500)
    video_label.pack()

    frame2 = Frame(game_frame)
    frame2.pack()
    b5 = Button(frame2, text="Select Option", font='sans 16', width=7, command=select_button)
    b5.pack(pady=20)

    # Start capturing video frames
    capture_video()

    game_frame.pack()

def create_login_screen():
    global username_entry, password_entry
    Label(login_frame, text="Username:").pack()
    username_entry = Entry(login_frame)
    username_entry.pack()

    Label(login_frame, text="Password:").pack()
    password_entry = Entry(login_frame, show="*")
    password_entry.pack()

    Button(login_frame, text="Login", command=validate_login).pack(side=LEFT, padx=10)
    Button(login_frame, text="Register", command=register_user).pack(side=LEFT, padx=10)
    login_frame.pack()
# Create main window
root = Tk()
root.geometry("800x800")
root.title("Rock Paper Scissor Game")

session = requests.session()

# Create login frame
login_frame = Frame(root)

# Create loading frame
loading_frame = Frame(root)

create_login_screen()

# # Show the login frame
# login_frame.pack()

# Execute Tkinter
root.mainloop()
