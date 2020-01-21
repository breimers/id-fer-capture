import logging
import os

import cv2
import numpy as np

import tensorflow as tf

#logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("fer-capture-log")

#global values
emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}
face_casc = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")

def path_to_img(image_path):
    return cv2.imread(image_path)

def detect_faces(frame):
    face_cascade = cv2.CascadeClassifier(face_casc)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    log.info("Beginning facial detection.")
    faces = face_cascade.detectMultiScale(
        frame,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(48, 48),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    log.info("Detected {} faces.".format(len(faces)))
    return gray, faces

def face_check(img, model, show=False):
    """
    This function performs an FER routine on the given image using the specified model.

    Parameters:
        image_path (str): Valid file path to a JPEG image.
        model_path (str): Valid file path to an h5 model.

    Returns:
        data (dict): Dictionary containing detected faces along with the predicted emotion.
    """
    #begin analysis
    frame = img
    gray, faces = detect_faces(frame)
    data = {"faces" : []}
    log.info("Beginning emotion recognition.")

    for i, (x, y, w, h) in enumerate(faces):
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
        prediction = model.predict(cropped_img)[0]
        predictions = {
            "angry": float(prediction[0]),
            "disgusted": float(prediction[1]),
            "fearful": float(prediction[2]),
            "happy": float(prediction[3]),
            "sad": float(prediction[4]),
            "surprised": float(prediction[5]),
            "neutral": float(prediction[6])
        }
        data["faces"].append({
            "id" : i,
            "xywh": (x, y, w, h),
            "predictions": predictions
        })
        if show:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
            cv2.putText(
                frame,
                "id: {}  |  {}: {}".format(
                    i,
                    max(predictions, key=predictions.get),
                    round(
                        predictions[
                            max(predictions, key=predictions.get)
                        ],
                        3
                    )
                ),
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (36,255,12),
                2
            )
    log.info("Detection completed successfully!")
    if show:
        cv2.imshow('Facial Detection', frame)
        cv2.waitKey(0)
    return data

def check_image(image_path, model_path, show=False):
    img = path_to_img(image_path)
    model = tf.keras.models.load_model(model_path)
    return face_check(img, model, show)

def check_stream(model_path, input=0, show=False):
    cap = cv2.VideoCapture(input)
    model = tf.keras.models.load_model(model_path)
    data = []
    while True:
        _, img = cap.read()
        if type(img) is not "NoneType":
            try:
                data.append(face_check(img, model, show))
            except Exception as e:
                log.error(e)
                break
        else:
            break
    cap.release()
    return data
