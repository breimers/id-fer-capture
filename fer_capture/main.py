import sys, os
import numpy as np
import cv2
from keras.models import load_model
import uuid
import base64
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)


#variables
emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}
DEF_MODELPATH = "./special/keras/models/cnn/model.h5"
DEF_FACE_CASC = "./special/open_cv/cascades/haarcascade_frontalface_default.xml"

def face_check(image_path):
    model_path = os.getenv("ID_FER_MODELPATH", default = DEF_MODELPATH)
    face_casc = os.getenv("ID_FER_FACE_CASC", default = DEF_FACE_CASC)
    model = load_model(model_path)
    frame = cv2.imread(image_path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(face_casc)
    faces = face_cascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(48, 48),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    data = {"id" : uuid.uuid4(), "faces" : []}
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
        prediction = model.predict(cropped_img)
        retval, buffer = cv2.imencode('.jpg', roi_gray)
        img_as_text = base64.b64encode(buffer)
        data["faces"].append({
            "id" : str(uuid.uuid4()),
            "as_b4_str" : img_as_text,
            "prediction" : emotion_dict[int(np.argmax(prediction))]
        })
    return data
