import pandas as pd
import numpy as np

import requests
import json

from sklearn.metrics.pairwise import cosine_similarity

from scipy.spatial.distance import cosine


class Recommender():
    def __init__(self):
        '''initializes our dataframe and builds our necessary dataframes.'''
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
        '''Performs our calculations. 
        Looks at the id_list to calculate a mean vector.
        Finds cosine similarity between mean vector and all items.
        Reduces the similarity score based on item rating/popularity. 
        Zeros out the similarity score for the mean vector and the item inputted.'''
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
        '''Sorts the similarity scores to print out the top n titles. n is 10 by default.'''
        for pos in self._sims.argsort()[:-(n+1):-1]:
            self.recommendations.append(self._get_title_from_loc(pos))
        for title in self.recommendations:
            print(title)
        return self


    # helper functions
    def _get_title_from_id(self, _id):
        '''Searches the title dataframe based on an anime id and tries to return the english title. 
        If an english title is not available, the "user preferred" title is given. '''
        title = None
        if pd.isna(self._title_df.loc[self._title_df.index == _id, 'english']).values[0]:
            title = self._title_df.loc[self._title_df.index == _id, 'userPreferred'].values[0]
        else:
            title = self._title_df.loc[self._title_df.index == _id, 'english'].values[0]
        
        return title

    def _get_title_from_loc(self, pos):
            '''Searches the title dataframe based on the location in an array and tries to return the english title. 
            If an english title is not available, the "user preferred" title is given. '''
            title = None
            if pd.isna(self._title_df.iloc[pos, 1]):
                title = self._title_df.iloc[pos, 3]
            else:
                title = self._title_df.iloc[pos, 1]
            
            return title


if __name__ == "__main__":
    # ask user for title
    # print found title to verify

    # loop: ask to add another title or get recommendations
    # print found title if title given

    # output recommendations
    
    pass