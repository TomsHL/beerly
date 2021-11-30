from surprise import SVD, Dataset, Reader, dump
import pandas as pd
from data_loading import Atrib
import os

path_data = "../raw_data/dataset_cleaned.csv"
df = pd.read_csv(path_data)

def fit_export(rating_type: Atrib, df) -> None:
    # Scale of notation for Surprise prediction and reading
    reader = Reader(rating_scale=(1, 5))

    # Creation of the dataset for Surprise
    data = Dataset.load_from_df(df[['user_id', 'beer_id', rating_type.val()]], reader)

    model = SVD()

    # Creation of the Trainset needed for fitting by Surprise
    trainset = data.build_full_trainset()
    model.fit(trainset);

    name_model = f"model_{rating_type.val()}"
    dump.dump(f"../models/{name_model}", predictions=None, algo=model, verbose=1)
    print(f"{name_model} exported")

if __name__ == '__main__':
    newpath = f"../models/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for atrib in Atrib:
        fit_export(atrib, df)
