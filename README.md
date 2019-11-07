# IntrospectData's OpenSource FER Application

Give the function an image and it will return a dictionary of detected faces and emotion predictions.


---

## Install

### Using pip

`$ pip3 install id_fer_capture`

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

`$ fer_capture --model path/to/model --image path/to/image` --> returns a python-dict to stdout

`$ fer_capture --model path/to/model --image path/to/image --out json` --> returns a json doc

---

## Why:
Democratizing facial recognition and emotion recognition technology is essential.

By making this technology available to everyone at least we can use it too :)
