# A Content-Based Anime Recommender

For those that aren't familiar, anime is style of animation originating from Japan. There are millions of fans world wide and in the 2017, the anime industry brought in more than [$19 Billion in revenue](https://www.hollywoodreporter.com/news/2017-anime-industry-revenue-hits-a-record-19-billion-1167382).  
There are millions of fans worldwide that can expect between 150 to 200 new shows coming out per year to be added to the thousands already in existance. It's a blessing and a curse. It can be overwhelming trying to find your next anime. It is not uncommon for shows to be prematurely canceled or to go more than a few years between season, both of which leave fans hungry for more.  
This recommender aims to help fans discovery new shows and find similar replacements to the shows they can't get enough of.  

## Data Wrangling

I used GraphQL to query the API at [AniList](https://anilist.co) and collect data for over 10,000 shows and movies, which will be refered to as items going forth. While collecting, this data was stored in a MongoDB database on an AWS EC2. The query returned a JSON object for each item. The genres and tags were extracted and placed in a Pandas dataframe. Duplicates and anything described as "hentai" was dropped. I'm not trying to build that sort of recommender.  

## Exploratory Data Analysis

"Genre" described general things like action, comedy, drama and was represented in my data as 1's and 0's (Trues and Falses). "Tags" also described the show but weren't quite at the level of genre, such as samurai, robots, or historical. Tags on AniList are user inputted and they come with a "rank" value of 0 to 100 representing how likely that tag describes that show.  
My initial instinct was to draw a cutoff point and say anything below 60 is a 0 in my dataframe and anything above is 1. Doing this ended up cutting out too much information and provided poor recommendations. I doubled back and kept the rank as a value from 0 to 1 and saw a significant improvement. Below is the histogram and box plot of the data afterwards.  

![anime_feature_counts](<https://github.com/sn-ekstrand/content-based-anime-recommender/blob/master/images/anime_feature_counts.png> "Anime Feature Counts")

## Model

## Exploring Dimensionality Reduction and Topics

## Refining Results

## Future Steps
