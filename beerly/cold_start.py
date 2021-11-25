from enum import Enum, unique

@unique
class Atrib(Enum):
    TASTE = 'taste'
    APPEARANCE = 'appearance'
    PALATE = 'palate'
    AROMA = 'aroma'
    OVERALL = 'overall'
    
    def val(self):
        return self.value

#class user():

def create_review(beer_id : int, user : int, rating :int ,text : str =None):
    ''' 
    create clean review for a specific user and beer with all info and fill the ratings
    beer_name : str, from the list of beer // id ?
    user : int , user_if for the table
    rating : int from 1-5
    '''
    # Copy of a review of the selected beer
    review = df_beer[df_beer['beer_id']== beer_id].iloc[0:1]
    review['user_id'] = user
    
    #filling of the ratings
    if text:
        review['review_text'] = text
    else:
        review['review_text'] = None

    for atrib in Atrib:
            review[atrib.val()] = rating
    return review


def create_user(ratings: dict, user_name: str, user_id=None):
    '''
    Return for a dict of ratings, the reviews to be appened in the database and the new user_id
    '''
    if user_id:
        user_id = user_id
    else:
        user_id = df_beer['user_id'].max() + 1

    reviews =[]
    for beer in ratings:
        reviews.append(create_review(beer_id=beer, rating=ratings[beer], user = user_id))

    return (user_id,user_name) , reviews

    

def append_user(reviews, dataset):
    
    for i in reviews:
        dataset = dataset.append(i,ignore_index=True)
        
    return dataset