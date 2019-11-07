import base64
import json
import os
import sys
import uuid

import click
import magic
import logging

import cv2
import numpy as np
from keras.models import load_model
from tensorflow.compat.v1 import ConfigProto, InteractiveSession
from tensorflow import get_logger


#logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("fer-capture-log")

def face_check(image_path, model_path):
    #tensorflow
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    get_logger().setLevel('ERROR')
    emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}
    face_casc = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")
    model = load_model(model_path)
    log.info("Loaded model: {}".format(model_path))
    face_cascade = cv2.CascadeClassifier(face_casc)
    log.info("Loaded cv2 cascade: {}".format(face_casc))
    log.info("Preparing image for processing: {}".format(image_path))
    frame = cv2.imread(image_path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    log.info("Beginning facial detection.")
    faces = face_cascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(48, 48),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    log.info("Detected {} faces.".format(len(faces)))
    data = {"id" : str(uuid.uuid4()), "faces" : []}
    log.info("Beginning emotion recognition.")
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
        prediction = model.predict(cropped_img)
        retval, buffer = cv2.imencode('.jpg', roi_gray)
        img_as_text = base64.b64encode(buffer)
        data["faces"].append({
            "id" : str(uuid.uuid4()),
            "as_b64_utf8_str" : str(img_as_text, "utf-8"),
            "prediction" : {str(int(np.argmax(prediction))) : emotion_dict[int(np.argmax(prediction))]}
        })
    log.info("Detection completed successfully!")
    return data

@click.command()
@click.option("--model", default = "model.h5", help = "Path to model binary.")
@click.option("--image", help = "Path to JPEG image.")
@click.option("--out", default = "raw", help = " 'raw': print dictionary to stdout, 'json': json to file ")
def cli(model, image, out):
    mime = magic.Magic(mime=True)
    if not mime.from_file(model) == "application/x-hdf":
        log.error("{} is not a valid application/x-hdf!".format(model))
        return 1
    if not mime.from_file(image) == "image/jpeg":
        log.error("{} is not a valid image/jpeg!".format(image))
        return 1
    try:
        data = face_check(image, model)
    except Exception as e:
        log.error(e)
        return 1
    if out == "json":
        with open(str(image.split("/")[-1].replace(".", "-") + ".json"), "w") as f:
            f.write(json.dumps(data))
            return 0
    print(data)
    return data
