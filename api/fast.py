from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from beerly import OCR, collab_predict

import base64
import pickle
import numpy as np
import cv2

# light db for quick matching
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
    appearance : float
    palate : float
    aroma : float
    overall : float
    content : float

# root method
@app.get("/")
def index():
    return {"greeting": "Status OK"}

# predict method, get parameters from front-end and send back a dataframe with ratings
@app.post("/predict")
def predict(item : Item):

    # decode base64-formatted image from front-end
    decoded_string = base64.b64decode(bytes(item.image, 'utf-8'))
    img = np.frombuffer(decoded_string, dtype='uint8')
    img = img.reshape((item.height, item.width, item.channel))

    # save the decoded image in a png
    with open('img.pickle', 'wb') as f:
        pickle.dump(img, f)

    with open('img.pickle', 'rb') as f:
        img_temp = pickle.load(f)
        cv2.imwrite("im_for_ocr.png", img_temp)

    # open the saved image, apply OCR methods to get a list of beer
    img = "im_for_ocr.png"
    extract = OCR.raw_extract(img)
    raw_list = OCR.list_from_ocr(extract)
    beer_df = OCR.match_all_beers(raw_list, df=default_db)

    # apply recommendation methods
    user = int(item.user)
    ratings = collab_predict.predict_collab(beer_df, user)

    # send back the df with beers and ratings
    dict_response = ratings.to_json()
    return dict_response
