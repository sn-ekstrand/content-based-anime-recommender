# A Content-Based Anime Recommender

For those that aren't familiar, anime is style of animation originating from Japan. There are millions of fans world wide and in the 2017, the anime industry brought in more than [$19 Billion in revenue](https://www.hollywoodreporter.com/news/2017-anime-industry-revenue-hits-a-record-19-billion-1167382).  
There are millions of fans worldwide that can expect between 150 to 200 new shows coming out per year to be added to the thousands already in existance. It's a blessing and a curse. It can be overwhelming trying to find your next anime. It is not uncommon for shows to be prematurely canceled or to go more than a few years between season, both of which leave fans hungry for more.  
This recommender aims to help fans discovery new shows and find similar replacements to the shows they can't get enough of.  

## Data Wrangling

I used GraphQL to query the API at [AniList](https://anilist.co) and collect data for over 10,000 shows and movies, which will be refered to as items going forth. While collecting, this data was stored in a MongoDB database on an AWS EC2. The query returned a JSON object for each item. The genres and tags were extracted and placed in a Pandas dataframe to create a total of 265 features. Duplicate items and anything described as "hentai" was dropped. I'm not trying to build a hentai recommender so they just add noise.  

## Exploratory Data Analysis

"Genre" described general things like action, comedy, drama and was represented in my data as 1's and 0's (Trues and Falses). "Tags" also described the show but weren't quite at the level of genre, such as samurai, robots, or historical. Tags on AniList are user inputted and they come with a "rank" value of 0 to 100 representing how likely that tag describes that show.  

My initial instinct was to draw a cutoff point and say anything below 60 is a 0 in my dataframe and anything above is 1. Doing this ended up cutting out too much information and provided poor recommendations. I doubled back and kept the rank as a value from 0 to 1 and saw a significant improvement. Below is the histogram and box plot of the data afterwards.  

![anime_feature_counts](<https://github.com/sn-ekstrand/content-based-anime-recommender/blob/master/images/anime_feature_counts.png?raw=true> "Anime Feature Counts")

<p align="center">
  <img height="400" src="https://github.com/sn-ekstrand/content-based-anime-recommender/blob/master/images/common_genres.png?raw=true">
  <img height="400" src="https://github.com/sn-ekstrand/content-based-anime-recommender/blob/master/images/common_tags.png?raw=true">
</p>

## Initial Model

When my data was still binary I was able to use cosine similarity and Jaccard index to measure the similarity between items but when I changed how I handled rank I could only use cosine similarity because Jaccard index requires binary data. Cosine measures the angle between items from the origin, giving a value of 1 for an angle of 0 degrees (same location) and a value of 0 for an angle of 180 degrees (opposite location). At this point we can get some recommendations for a single title by finding which items have the highest similarity scores.  

## Exploring Dimensionality Reduction and Clusters

Dimensionality reduction can be beneficial if you need to make recommendations quick which we may need if this recommender goes online and gets used by many people. Dimensionality reduction can also reveal themes in your data which is worth exploring. We're working with 265 features and we'd like to get that number as low as possible while retaining a necessary amount of accuracy.  

For this I tried an [NMF](<https://en.wikipedia.org/wiki/Non-negative_matrix_factorization>) model and I tried a [PCA](<https://en.wikipedia.org/wiki/Principal_component_analysis>) model. With both models, the features struggled to be compressed. Using a standard scaler on the data and running PCA revealed that 209 principal components (a 20% drop) were required to explain 90% of variation in the data. Not really worth it. NMF had a similar story. <b>Disclaimer: </b> You should use a standard scaler on your data before running PCA. Out of curiosity, I tried a robust scaler. After running PCA on this, it showed that it only needed 71 principal components. I found this interesting and decided to explore the principal components more. We find some principal components that actually are informative. For example, one is associated with comedy, adventure, action, and fantasy and describes titles like Dragonball Z, Fairy Tail, and The Seven Deadly Sins, all of which make sense to me. More examples can be found in my dimensionality reduction notebook. 

![PCA](<https://github.com/sn-ekstrand/content-based-anime-recommender/blob/master/images/pca_chart.png?raw=true> "PCA Comparison")  

In the end, I felt the data did not form into a few clear topics. The best results were with a non-standard approach. Because of this and considering the model does not take long to make recommendations right now so speed is not a major concern I opted to leave the data in its original form to gain accuracy in my recommendations.  

## Refining Results

So thus far, we've cleaned our data, we've decided how to work with tag rank, and we've decided to not pursue dimensionality reduction at this time. We're getting results but they still need work. To many poorly rated titles are at the top of our list of recommendations. For example, while trying to get recommendations for ["Wolf's Rain"](<https://myanimelist.net/anime/202/Wolfs_Rain?q=wolf%27s%20rain>) we get ["Wan Wan Chuushingura"](<https://myanimelist.net/anime/9228/Wan_Wan_Chuushingura?q=wan%20wan>) in our top 5, which has mean score of 0.5 on aniList.co and a 5.74 out of 10 on myanimelist.com. The assumption is that we can find other similar shows that fans will actually want to watch. But how do we do that?  

Aside from genres and tags, each show in the dataset has a mean score and a popularity rating. We combine these to account for highly rated shows that don't have a lot of ratings. Starting with a show to get recommendations, we find the similarity score with every item. We then find the product of the similarity score and a shows rating to find a new kind of score. The similarity scores of poorly rated shows drop a lot more than highly rated shows, giving us more valuable results.  

We've made a lot of progress but there's another limitation that can be addressed. We're only accepting one input but in reality a user will have multiple titles they like. To handle this, we take in the multiple shows, find their vectors in our dataframe, find the mean vector, and use that mean vector to find similar items. For example, let's put in a few of my favorite shows, "Ergo Proxy", "Wolf's Rain", and "Texhnolyze", all of a more serious nature (drama, psychological, distopian, post-apocalyptic, sci-fy, or fantasy.) We get some results that I've seen and agree with and some results I haven't seen but will be adding to my watch list.  

![example results](<https://github.com/sn-ekstrand/content-based-anime-recommender/blob/master/images/example_results-1.jpg?raw=true>)

## Future Steps

There's a lot more that makes a good recommender than what has been done here. I would like to add more features to get a more accurate feel for a show. For example, I would like to add the main staff and studios involved in making the anime. They have a large impact on the quality and character of a show. Two shows can have the same genres and tags but they won't feel the same if they were done by different people. I would like to capture this.  

I would like to incorporate collaborative-based recommendations which can help increase the diversity of my results. The main idea there is that we find users that have rated content similar to user A, find content that user A hasn't seen but is highly rated by these users, and then we recommend user A look into that content.  

Finally, I would like to build a Flask app in order to get this recommender online for everyone to use. 