from enum import Enum, unique

#from termcolor import colored

#from surprise import SVD, Dataset, Reader, dump
#from surprise.model_selection import cross_validate

#from beerly.params import PATH_MODEL, RATINGS

@unique
class Atrib(Enum):
    TASTE = 'taste'
    APPEARANCE = 'appearance'
    PALATE = 'palate'
    AROMA = 'aroma'
    OVERALL = 'overall'
    
    def val(self):
        return self.value


class Predictor(object):
    def __init__(self, Atrib='overall'):
        """
            user: TO BE DEFINED
            type_rate : str : ratings to be used for pred / possible value : ['palate', 'overall', 'appearance', 'aroma', 'taste']
            beer_from_ocr = list : obtained from the OCR_Read class
        """
        #self.user = user
        #self.beer_from_ocr = beer_from_ocr
        self.Atrib = Atrib



    def load_model(self, type_rate):
        """
            Load the already trained rating model from a surprise file
            type_rate : str : ratings to be used for pred / possible value : ['palate', 'overall', 'appearance', 'aroma', 'taste']
        """

        #selection & loading of the correct model
        FILE_NAME = f'model_{type_rate}'
        model = dump.load(f'{PATH_MODEL}/{FILE_NAME}')[1]

        # Check
        print(colored("model loaded", "green"))
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
    model = load_model(rating)
    pred = evaluate(user, model)
    resfinal = filter_result(pred)

