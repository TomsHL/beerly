from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from beerly import OCR, collab_predict

from PIL import Image
from pydantic import BaseModel

import base64
import pickle
import numpy as np
import cv2

default_db = '/home/tom/code/TomsHL/beerly/raw_data/dataset_light.csv'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class Item(BaseModel):
    image: str
    user: int
    height : int
    width : int
    channel : int


@app.get("/")
def index():
    return {"greeting": "Status OK"}


@app.post("/predict")
def predict(item : Item):
    decoded_string = base64.b64decode(bytes(item.image, 'utf-8'))
    img = np.frombuffer(decoded_string, dtype='uint8')
    img = img.reshape((item.height, item.width, item.channel))
    with open('img.pickle', 'wb') as f:
        pickle.dump(img, f)

    with open('img.pickle', 'rb') as f:
        img3 = pickle.load(f)
        cv2.imwrite("im_for_ocr.png", img3)


    img = "im_for_ocr.png"
    extract = OCR.raw_extract(img)
    raw_list = OCR.list_from_ocr(extract)
    beer_df = OCR.match_all_beers(raw_list, df=default_db)

    user = int(item.user)
    ratings = collab_predict.predict_collab(beer_df, user)

    dict_response = ratings.to_json()

    return dict_response
