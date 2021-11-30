import pandas as pd
<<<<<<< HEAD
from surprise import dump
from beerly.data_loading import Atrib
=======
from data_loading import Atrib
>>>>>>> 88b1ed244b15d1e421d2cb34e142e4bf8716d803

def predict_collab(beer_list: pd.DataFrame, uid, models) -> pd.DataFrame:
    """
    Compute all the predictions for the Collab models and append a result Dataframe given a
    beer_list from OCR and a user_id
    beer_list = pd.DataFrame with 4 columns:
    ['name_from_ocr','brewery_name','beer_name','beer_id']
    uid : int / its the user_id
    models :  list of models from
    """

    beer_note = beer_list.copy()
    beer_note.drop(columns=['name_from_ocr', 'brewery_name'], inplace=True)

    for rating_type in Atrib:
<<<<<<< HEAD
        path_loading = f'/home/tom/code/TomsHL/beerly/models/model_{rating_type.val()}'
        model = dump.load(path_loading)[1]
=======
        model = models[rating_type.val()]
>>>>>>> 88b1ed244b15d1e421d2cb34e142e4bf8716d803
        list_note = [model.predict(uid, iid, verbose=False, clip=True)[3] for iid in beer_list['beer_id']];
        beer_note[f"rating_{rating_type.val()}"] = list_note

    return beer_note

if __name__ == '__main__':
    pass
