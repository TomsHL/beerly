import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS


def predict_content(dataset: pd.core.frame.DataFrame,
                    dataset_reviews: pd.core.frame.DataFrame,
                    menu_ocr: pd.core.frame.DataFrame, user_id: int, review_size:int=0):
    '''Return a similarity score between two set of beers.
    One from a menu screened by OCR and the other parsed from the user reviewed beers

    Args:
        dataset (DataFrame): reviews of beer.
        dataset_reviews (DataFrame): beers grouped by beer_id
        menu_ocr (DataFrame): Output from OCR screening
        user_id (int): id of user
        review_size (int): number of words to keep for each review, the lower the faster the prediction is.

    Returns:
        Serie: menu beers ranked by similarity.
    '''

    #creation of the menu serie mixing beer_id from ocr and matching reviews from beers

    dataset_reviews.set_index(dataset_reviews['beer_id'], drop=False, inplace=True)
    beers = dataset_reviews.review_text

    menu = beers[beers.index.isin(menu_ocr.beer_id)]
    m = menu.size

    del dataset_reviews, menu_ocr

    #Create liked, the serie containing an user's reviewed beers.
    rated = dataset[(dataset.user_id == user_id) & (dataset.overall > 3) ]['beer_id']
    liked = beers.loc[rated]
    del beers, rated

    #Vectorizing
    custom_words = frozenset([
        'abv', 'adds', 'come', 'comes', 'coming', 'drink', 'drinking', 've',
        'thing', 'things', 'oz', 'think', 'thought', 'll', 'actually', 'bottle'
    ])
    stop_words = ENGLISH_STOP_WORDS.union(custom_words)

    payload = pd.concat([menu, liked])

    if(review_size):
        payload = payload.apply(lambda s : s[:review_size])

    vectorizer = CountVectorizer(stop_words=stop_words,
                                 min_df=5,
                                 max_df=40,
                                 max_features=400,
                                 token_pattern=r'(?u)\b[a-z]{2,}\b')
    count_matrix = vectorizer.fit_transform(payload)

    #similarity
    cosine_sim = cosine_similarity(count_matrix[:m], count_matrix[m:])
    similarity = pd.DataFrame(cosine_sim)
    similarity.index = menu.index
    similarity.columns = liked.index
    del liked, menu

    #ranking
    ranking = similarity.mean(axis=1).sort_values(ascending=False)
    ranking.index.name = 'beer_id'
    ranking.name = 'score'
    return ranking
