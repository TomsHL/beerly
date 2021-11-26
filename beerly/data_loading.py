from enum import Enum, unique
import ast
import pandas as pd

# A changer plus tard pas propre ce truc
file_users = 'new_users.csv'
df_path = '../raw_data/kaggle_v2.csv'

@unique
class Atrib(Enum):
    TASTE = 'taste'
    APPEARANCE = 'appearance'
    PALATE = 'palate'
    AROMA = 'aroma'
    OVERALL = 'overall'
    
    def val(self):
        return self.value

class new_users(object):
	"""New users for the data_base"""
	def __init__(self, id:int , name:str, ratings: dict):
		self.id = id
		self.name = name
		self.ratings = ratings
	
	def get_ratings(self):
		return self.ratings

	def get_id(self):
		return self.id

	def get_name(self):
		return self.name

def preproc_data(df_path) -> pd.DataFrame:
    '''
    Preprocessing of the data frame
    df_path : full path to the data_set 
    1. fill Na with ' ' to avoid fuzzy matching pb
    2. Create the correct columns beer + brewery
    3. NOT inplemented : Cleaning of beer with low rating count
    4. NOT inplemented : Cleaning of beer with comment not in english
    5. append new user 
    '''
    
    df = pd.read_csv(df_path)
    
    # Step 1 & 2
    if 'beer_name' and 'brewery_name' in df:
        df['brewery_name'].fillna(value= ' ', inplace=True )
        df['beer_brewery'] = df['beer_name'] + ' ' + df['brewery_name']
        
    else :
        return print('Wrong format of dataset')
    
    return df

def load_new_users(file_name):
	'''
	load all the Hnad crated users from the new_users.csv
	'''
    with open(file_name) as f:
        list_new_users = []
        for line in f:
            temp = line.split(";")
            list_new_users.append(new_users(
                                            name= temp[0], 
                                            ratings = ast.literal_eval(temp[1]), 
                                            id =int(temp[2]))
                                 )
    return list_new_users

def create_review(beer_id : int, user : int, rating :int , df_beer ,text : str =None):
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

def update_dataset(df,list_new_users):
    list_reviews = []
    for user in list_new_users:
        for key in user.get_ratings():
            list_reviews.append(create_review(beer_id = key, 
                                              user = user.get_id(), 
                                              rating = user.get_ratings()[key], 
                                              df_beer=df))
    for new in list_reviews:
        df = df.append(new, ignore_index=True)
    
    return df


if __name__ == '__main__':
    list_new_users = load_new_users(file_users)
    df = preproc_data(df_path)
    df = update_dataset(df,list_new_users)
    