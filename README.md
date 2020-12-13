# Twitter Recommendations Based on Text


###Team Members: 
Rohan Khanna (Team Captain) - rohank2@illinois.edu
Tyler Wong - tylercw3@illinois.edu
Cesia Bulnes - cbulnes2@illinois.edu



##Introduction

Twitter is a social media platform allowing users to connect and share thoughts and information. A notable example of Twitter and content shared was seen in 2020, with the presidency and election. There are currently recommendations on who to follow in general for Twitter users. However, when a tweet is made, that tweet does not have suggested/similar tweets that a user can react to or retweet. The purpose of this project is to give users the ability to get recommendations based on their tweets. Suppose you write “love hamburgers and fries”, you should expect to get back a topic, and if you run that same query with our ranker, you will get a list of 10 tweets that are closest in similarity, along with the 10 users that have tweets that are closest to the content of this query. 


##Obtaining Twitter Data
You will need Python installed and all the required packages installed.
>pip install -r requirements.txt

Obtain a Twitter developer account through the Twitter Developer Portal if you haven’t already. Add the consumer key, consumer secret, access token, access token secret, and bearer token to the “twitter_utils.py” main method’s variables. These will be used to interact with the Twitter API.

Run the code to get the users and tweets. The code will check to make sure not to regenerate these, so if you run it multiple times you will need to delete the files in the “data” directory of the repository.
>python src/twitter_utils.py

##Data Extraction
For topic extraction we use the nltk toolkits and gensim. As we learnt in class LDA is an unsupervised machine learning algorithm that uses a mixture model to generate documents. Each topic can be assigned some prior probability and each topic consists of probabilities for generating a particular word from the vocabulary.


##Data Retrieval/Cleaning:
We developed a few different functions to perform data retrieval and cleaning of the tweets:

>remove_emoji(text)

>remove_links(text)

>remove_users(text)

>clean_tweet(tweet)

All of these functions are meant to clean up the data so that we can perform better analysis of the data with better accuracy. We process all of our original tweets from the SQLite database through these functions.

The remove_emoji(text)method removes any emojis that are found in the tweet because we found that emojis didn’t provide much meaningful information. The remove_links(text) method removes any HTTP or HTTPs links that are found in the tweet text since that data isn’t useful when determining category. The remove_users(text)method removes any “@” mentions for any other user. The clean_tweet(tweet)method makes the tweet all lowercase, removes punctuation, removes any stopwords, and removes any words that 2 characters or less. 
###How to run Topic Extraction: 
To run the code a user can put test tweets in the test tweets.json file and just execute the python3.8 topicdeterminant.py this will classify the tweet into the most likely topic. Using this topic modelling you can draw a relationship between people who have similar tweets.

Execute the following command on the terminal
>python3.8 topicdeterminant.py 

##Ranker of tweets and users
After loading the tweet data and creating a map of the author id’s to the author’s screen name, the tweets are then using tf-idf weights per word to score shared words. 

Given the following tweet_query “heat is cranking” I want to return a recommendation of tweets that are similar to the tweet_query, along with the % of their similarity.
1) To begin with, once git cloned, go to data and unzip tweets.tar.gz, this will unzip tweets.json.
tar -xzvf tweets.tar.gz 
2) You can choose a query to substitute into tweet_query in the ranker.py code. You may replace the writing within this query to obtain similarities with different queries. 
3) To execute simply write the following in the terminal: python ranker.py



##Sources 
1. https://medium.com/@osas.usen/topic-extraction-from-tweets-using-lda-a997e4eb0985
2. http://blog.echen.me/2011/08/22/introduction-to-latent-dirichlet-allocation/
3. https://github.com/enoreese/topic-modelling/blob/master/preprocessor.py
4. https://github.com/4OH4/doc-similarity/blob/master/examples.ipynb

