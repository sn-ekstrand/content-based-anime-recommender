import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import pprint as pp

import requests
import json
from difflib import get_close_matches
from difflib import SequenceMatcher

from sklearn.metrics.pairwise import cosine_similarity

from scipy.spatial.distance import cosine



class Recommender():
    def __init__(self):
        self.id_list = []
        self.sims = None
        self.adjusted_score_df = pd.read_csv('data/adjusted_score_df.csv', index_col='id')
        self._title_df = pd.read_csv('data/title_df.csv', index_col='id')
        self.content_item_matrix = pd.read_csv('data/content_item_matrix.csv', index_col='id')
        self.recommendations = []

    def get_id(self, initial_search):
        '''Takes in anime title as a string. 
        Searches the AniList API for the closest matching anime using GraphQL.
        Prints out the title of the search result.
        Adds show id to a list for getting recommendations
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
        user_preferred_title = response.json()['data']['Media']['title']['userPreferred']
        _id = response.json()['data']['Media']['id']
        self.id_list.append(_id)
        print('Found title:', user_preferred_title)

        return self

    def _calc_similarities(self):
        mean_vector = self.content_item_matrix.loc[self.id_list,:].mean(axis=0)
        sim_mat = cosine_similarity(self.content_item_matrix.append(mean_vector, ignore_index=True).values)
        adjusted_scores = round((self.adjusted_score_df['adjusted_score']), 4)
        self._sims = (sim_mat[-1:] * np.append(adjusted_scores.to_numpy(), 0))[0]
        exclusion_vec = np.ones(len(self._sims))
        for _id in self.id_list:
            exclusion_vec[(self.content_item_matrix.index.get_loc(_id))] = 0
        self._sims *= exclusion_vec

        return self

    def get_recommendations(self, n=10):
        for pos in self._sims.argsort()[:-(n+1):-1]:
            for title in self._title_df.iloc[pos,[1, 3]]:
                self.recommendations.append(title)
        for title in self.recommendations:
            print(title)
        return self

    # def get_top_n_recommendations(self, anime_id, dataframe, similarity_matrix, n=5):
        # positional_idx = dataframe.index.get_loc(anime_id)
        # 
        # top_n = np.argsort(similarity_matrix[positional_idx,:])[-n-1:-1]
        # recom_titles = []
        # for idx, row in _title_df.iloc[top_n,:].iterrows():
            # if type(row['english']) != float:
                # recom_titles.append(row['english'])
            # else:
                # recom_titles.append(row['userPreferred'])
        # 
        # return recom_titles




    # helper functions
    def get_title_from_id(self, _id):
        '''Searches the title dataframe based on an anime id and tries to return the english title. 
        If an english title is not available, the "user preferred" is give. '''
        title = None
        if pd.isna(self._title_df.loc[self._title_df.index == _id, 'english']).values[0]:
            title = self._title_df.loc[self._title_df.index == _id, 'userPreferred'].values[0]
        else:
            title = self._title_df.loc[self._title_df.index == _id, 'english'].values[0]
        
        return title

    def get_title_from_loc(self, loc):
            '''Searches the title dataframe based on the location in an array and tries to return the english title. 
            If an english title is not available, the "user preferred" is give. '''
            title = None
            if pd.isna(self._title_df.iloc[self._title_df.index == loc, 'english']).values[0]:
                title = self._title_df.iloc[self._title_df.index == loc, 'userPreferred'].values[0]
            else:
                title = self._title_df.iloc[self._title_df.index == loc, 'english'].values[0]
            
            return title

    def view_features(self, search_term, df):
        _id = self._title_df[self._title_df['userPreferred'] == search_term].index
        _df = df.loc[_id,:]

        return list(_df.loc[:, (_df != 0).any(axis=0)].columns)

    def view_features_from_id(self, _id, _df):
        single_show = _df.loc[_id,:]
        
        return set(single_show[single_show != 0].index)



if __name__ == "__main__":
    # ask user for title
    # print found title to verify

    # loop: ask to add another title or get recommendations
    # print found title if title given

    # output recommendations
    
    pass