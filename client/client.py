import tensorflow as tf
import cv2
import numpy as np
import sys
import repository
from apscheduler.schedulers.background import BackgroundScheduler

video = cv2.VideoCapture(0)

if not video.isOpened():
    raise IOError("Camera not enabled")

# Load the model. This should be located within the same directory and labeled the same as it was in the original notebook.
model = tf.keras.models.load_model("./rock_paper_scissors_mobilenet_v2.h5")
labels = ['rock', 'paper', 'scissors']

width = 128
height = 128

# TODO: Change from system variable to TKinter prompt
if len(sys.argv) < 3:
    raise Exception("Less than 2 arguments provided after Python script. Please enter username as the first variable, and password as the 2nd.")

username = sys.argv[1]
password = sys.argv[2]

repository.login(username, password)

scheduler = BackgroundScheduler()
make_choice_job = scheduler.add_job(repository.make_choice, args=(username, ""), trigger="interval", seconds=10)
scheduler.start()

while(True):
    ret, frame = video.read()
    cv2.imshow('frame', frame)

    # Preprocess data in the same way as it was in the original notebook.
    frame_tensor = tf.expand_dims(frame, 0)
    image = tf.cast(frame_tensor, tf.float32)
    image = image/255
    image = tf.image.resize(image, [width, height])
    
    result = model.predict(image)
    inferred_result = np.argmax(result)
    confidence = result[0][inferred_result]

    if confidence < 0.5:
        print("Rejected result - confidence too low.")
    else:
        make_choice_job.modify(args=(username, labels[inferred_result]))
        print(f"Inferred result: {labels[inferred_result]} with confidence {confidence*100}%")


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()