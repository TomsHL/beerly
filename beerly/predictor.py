from enum import Enum, unique
import pandas as pd
from data_loading import Atrib
from surprise import dump

#from termcolor import colored
#from surprise import SVD, Dataset, Reader, dump
#from surprise.model_selection import cross_validate
#from beerly.params import PATH_MODEL, RATINGS
PATH_MODEL = '../models'

class Predictor(object):
    def __init__(self, Atrib='overall' : Atrib):
        """
            Atrib : ratings to be used for pred / possible value : ['palate', 'overall', 'appearance', 'aroma', 'taste']
            beer_from_ocr = list : obtained from the OCR_Read class
        """
        self.Atrib = Atrib

    def get_atrib(self):
        return self.Atrib


def load_model(self, type_rate):
    """
        Load the already trained rating model from a surprise file
        type_rate : str : ratings to be used for pred / possible value : ['palate', 'overall', 'appearance', 'aroma', 'taste']
    """

    #selection & loading of the correct model
    FILE_NAME = f"model_{self.get_atrib()}"
    model = dump.load(f"{PATH_MODEL}/{FILE_NAME}")[1]

    # Check
    return model

def evaluate_user(self, user, model):
    """
        Make a prediction for a user based on the chosen rating and return the prediction for ALL beers
        user : TO BE DEFINED
        model :  result from load_model() function
    """
    y_pred = model.predict(user)
    return y_pred

def filter_result(y_pred, beer_from_ocr):
    """
        Filter the predictions from the chosen model by the of beer coming from OCR
        y_pred : result from evaluate() function
        beer_from_ocr = list : obtained from the OCR_Read class
    """

    return filtered_list_of_beer

if __name__ == "__main__":

    # return prediction
    #model = load_model(rating)
    #pred = evaluate(user, model)
    #resfinal = filter_result(pred)
