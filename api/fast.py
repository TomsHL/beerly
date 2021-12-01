import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel
from surprise import dump

from beerly import OCR, collab_predict, content_predict, global_predict

import base64
import numpy as np
import pandas as pd

# Preload datasets and models to speed up API calls
default_db = pd.read_csv('raw_data/dataset_light.csv')
dataset = pd.read_csv('raw_data/dataset_cleaned.csv')
dataset_reviews = pd.read_csv('raw_data/dataset_reviews.csv')

models = {
    'appearance': dump.load('models/model_appearance')[1],
    'aroma': dump.load('models/model_aroma')[1],
    'overall': dump.load('models/model_overall')[1],
    'palate': dump.load('models/model_palate')[1],
    'taste': dump.load('models/model_taste')[1]
}

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
    height: int
    width: int
    channel: int
    taste : float
    appearance: float
    palate: float
    aroma: float
    overall: float
    content: float


# root method
@app.get("/")
def index():
    return {"greeting": "Status OK"}


# predict method, get parameters from front-end and send back a dataframe with ratings
@app.post("/predict")
def predict(item: Item):
    # get mix params
    mix_params = {
        'taste': item.taste,
        'appearance': item.appearance,
        'palate': item.palate,
        'aroma': item.aroma,
        'overall': item.overall ,
        'content': item.content
    }
    t = time.time()
    times= {}

    times.update({'start': 0})

    # decode base64-formatted image from front-end
    decoded_string = base64.b64decode(bytes(item.image, 'utf-8'))
    img = np.frombuffer(decoded_string, dtype='uint8')

    times.update({'decode': time.time()-t})

    img = img.reshape((item.height, item.width, item.channel))
    img = Image.fromarray(img)

    extract = OCR.raw_extract(img)
    times.update( {'raw_extract': time.time()-t})
    raw_list = OCR.list_from_ocr(extract)
    times.update( {'list_from': time.time()-t})
    beer_df = OCR.match_all_beers(raw_list, df=default_db)
    times.update( {'match_all': time.time()-t})
    # apply recommendation methods
    user = int(item.user)
    collab = collab_predict.predict_collab(beer_df, user, models)
    times.update( {'collab': time.time()-t})
    content = content_predict.predict_content(dataset, dataset_reviews,
                                              beer_df, user)
    times.update( {'content': time.time()-t})
    glob = global_predict.global_pred(collab, content, mix_params)
    times.update( {'gloabl': time.time()-t})
    # send back the df with beers and ratings
    dict_response = glob.to_json()
    times.update( {'end': time.time()-t})
    print(times)
    return dict_response
