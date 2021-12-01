import pandas as pd

# from collab_predict import predict_collab
from data_loading import Atrib

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

    beer_ranking["ranking"] = (beer_ranking.score * 10 * mixing_parameters['content'] +
                               beer_ranking.rating_aroma * mixing_parameters['aroma'] +
                               beer_ranking.rating_taste * mixing_parameters['taste'] +
                               beer_ranking.rating_palate * mixing_parameters['palate'] +
                               beer_ranking.rating_overall * mixing_parameters['overall'] +
                               beer_ranking.rating_appearance * mixing_parameters['appearance']
                              )/ sum(mixing_parameters.values())

    beer_ranking = beer_ranking[['beer_id','beer_name','ranking']]
    beer_ranking.sort_values(
        by=["ranking"], ascending=False, ignore_index=True, inplace=True
    )

if __name__ == "__main__":
    pass
