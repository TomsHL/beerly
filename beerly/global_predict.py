import pandas as pd
import numpy as np

# from collab_predict import predict_collab
from data_loading import Atrib


def global_pred(
    result_collab: pd.DataFrame,
    mixing_parameters: dict,
    result_content: pd.DataFrame = None,
) -> pd.DataFrame:

    beer_ranking = result_collab.copy()

    if "content" in mixing_parameters.keys():
        return print("not implented yet")

    temp = pd.Series(data=np.zeros((len(mixing_parameters))), dtype="float32")

    for atrib in Atrib:
        temp = beer_ranking[f"rating_{atrib.val()}"] + temp
        beer_ranking.drop(columns=[f"rating_{atrib.val()}"], inplace=True)

    beer_ranking["ranking"] = temp / len(mixing_parameters)
    beer_ranking.sort_values(
        by=["ranking"], ascending=False, ignore_index=True, inplace=True
    )

    return beer_ranking


if __name__ == "__main__":
    pass
