from termcolor import colored

from surprise import SVD, Dataset, Reader, dump
from surprise.model_selection import cross_validate

from beerly.params import PATH, RATE


class Predictor(object):
    def __init__(self, user, type_rate, beer_from_ocr):
        """
            user: pandas Series
        """
        self.user = user
        self.type_rate = type_rate
        self.beer_from_ocr = beer_from_ocr


    def load_model(self, type_rate):
        """Save the model into a file in surprise format"""

        #add mean to select correct model from rating param
        #FILE_NAME = RATE['rating']

        model = dump.load('$PATH/$FILE_NAME')[1]
        print(colored("model loaded", "green"))
        return model

    def evaluate(self, user, model):
        """evaluates the pipeline on df_test and return the RMSE"""
        y_pred = model.predict(user)
        return y_pred

    def filter_result(y_pred, beer_from_ocr):
        #
        return filtered_list_of_beer

if __name__ == "__main__":
    
    # return prediction
    model = load_model(rating)
    pred = evaluate(user, model)
    resfinal = filter_result(pred)

