import pandas as pd
import numpy as np
import requests
import json
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
db = client.anime
collection = db.content_features

df = pd.read_csv('AnimeList.csv')
df = df[['anime_id', 'type', 'title', 'title_english', 'score', 'premiered']]
df = df.sort_values('score', ascending=False)

anime_titles = list(df['title'])

query = '''
query ($search: String) {
  Media(type: ANIME, search: $search) {
    id
    title {
      romaji
      english
      native
      userPreferred
    }
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    season
    seasonYear
    type
    format
    status
    episodes
    duration
    chapters
    volumes
    isAdult
    genres
    tags {
      name
      rank
      category
    }
    isLicensed
    averageScore
    popularity
    source
    countryOfOrigin
    format
    duration
    chapters
    volumes
    averageScore
    popularity
    source
    staff {
      edges {
        id
        node {
          id
          name {
            first
            last
            full
            native
          }
        }
        role
      }
    }
    studios {
      edges {
        id
        node {
          id
          name
          isAnimationStudio
        }
        isMain
      }
    }
    characters {
      edges {
        id
        role
        node {
          id
          name {
            first
            last
            full
            native
          }
        }
        voiceActors {
          id
          language
          name {
            first
            last
            full
            native
          }
        }
      }
    }
  }
}

'''

url = 'https://graphql.anilist.co'

for t in anime_titles:
    
    # Define our query variables and values that will be used in the query request
    variables = {
        'search': t
    }
    
    try:
        # Make the HTTP Api request
        r = requests.post(url, json={'query': query, 'variables': variables})
        show_dict = json.loads(r.text)
    except:
        show_dict = None
    with open('log_file.csv','a') as fd:
        fd.write([t, r.status_code])
    time.sleep(10)
    collection.insert_one(show_dict)

