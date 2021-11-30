import pandas as pd
import numpy as np

# from collab_predict import predict_collab
from beerly.data_loading import Atrib

def global_pred(
    result_collab: pd.DataFrame,
    result_content: pd.DataFrame,
    mixing_parameters= {'taste': 1,
                        'appearance': 1,
                        'palate': 1,
                        'aroma': 1,
                        'overall': 1,
                        'content': 5}) -> pd.DataFrame:

    beer_ranking = pd.merge(result_collab,result_content,on='beer_id')

    temp = pd.Series(data=np.zeros((len(mixing_parameters))), dtype="float32")

    for atrib in Atrib:
        temp = beer_ranking[f"rating_{atrib.val()}"]* mixing_parameters[atrib.val()] + temp
        beer_ranking.drop(columns=[f"rating_{atrib.val()}"], inplace=True)

    beer_ranking["ranking"] = (temp + beer_ranking.score *10* mixing_parameters['content'])/ sum(mixing_parameters.values())
    beer_ranking.drop(columns='score',inplace=True)
    beer_ranking.sort_values(
        by=["ranking"], ascending=False, ignore_index=True, inplace=True
    )

    return beer_ranking

if __name__ == "__main__":
    pass
