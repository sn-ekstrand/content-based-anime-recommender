import pandas as pd
import numpy as np

import requests
import json
from difflib import get_close_matches
from difflib import SequenceMatcher

from sklearn.metrics.pairwise import cosine_similarity

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class Recommender():

    def __init__(self):
        pass
    
    def search(self, initial_search):
        '''Search the AniList API for a show based on a query.
        
        Returns the user preferred title as defined by Anilist
        '''
        query = '''
        query ($search: String) {
        Media (type: ANIME, search: $search) {
            id
            title {
            romaji
            english
            native
            userPreferred
            }
        }
        }
        '''
        variables = {'search': initial_search}

        url = 'https://graphql.anilist.co'
        response = requests.post(url, 
                                json={'query': query, 
                                    'variables': variables})
        self.user_preferred_title = response.json()['data']['Media']['title']['userPreferred']

        return self

    def get_similarity_matrix(self):
        


    def get_top_n_recommendations(self, dataframe, similarity_matrix, n=5):        
        anime_id = title_df[title_df['userPreferred'].isin(self.user_preferred_title)].index

        # get position of anime (id in index)
        positional_idx = dataframe.index.get_loc(int(anime_id.values))
        
        # get top n indicies. The top match will always be the initial item.
        top_n = np.argsort(similarity_matrix[positional_idx,:])[-n-1:-1]

        self.recom_titles = []
        for idx, row in title_df.iloc[top_n,:].iterrows():
            if type(row['english']) != float:
                self.recom_titles.append(row['english'])
            else:
                self.recom_titles.append(row['userPreferred'])
        
        return self.recom_titles
