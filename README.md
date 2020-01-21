# IntrospectData's OpenSource FER Application

Give the function an image and it will return a dictionary of detected faces (base64 encoded jpeg) and emotion predictions (dictionary of index and prediction).


---

## About

This is a python3 utility for Facial Detection/Emotion Recognition (FER) using Keras and OpenCV.

This project uses the [haarcascade](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml) xml for facial detection.

We recommend using [our model](https://storage.googleapis.com/id-public-read/model.h5) for this application, but you may use your own as well. This project could be easily modified to do other types of object detection if you wish.

If you fork this project, please contribute back with any fixes or features the community may find useful. All PRs will go through a member of our Engineering team.

Please follow GitHub's template for bug reporting.

---

## Install

### Using pip

`$ pip3 install fer-capture`

### From source

`$ git clone git@github.com:IntrospectData/id-fer-capture.git`

`$ python3 -m venv env`

`$ source env/bin/activate`

`(env) $ pip3 install id_fer_capture`
  - To include tensorflow:
      - `id-fer_capture[cpu]` for cpu based tensorflow
      - `id-fer_capture[gpu]` for gpu based tensorflow
---

## Use:

`$ wget -P /path/to/somewhere/ https://storage.googleapis.com/id-public-read/model.h5`

```python3
>>> from fer_capture.main import check_stream
>>> from fer_capture.main import check_image
>>> check_stream("/mnt/storage/model.h5", "/mnt/storage/face_test.mp4")
    [{'faces': {...}}, ...]
>>> check_image("/mnt/storage/model.h5", "/mnt/storage/face.jpeg")
    {'faces': {...}}
```
---

## Why:
Democratizing facial recognition and emotion recognition technology is essential.

By making this technology available to everyone at least we can use it too :)
