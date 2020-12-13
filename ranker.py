import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
stop_words = set(stopwords.words('english'))


from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

class reduce_by_lemma:
    """
    reduction of words down to their lemma
    """
    not_needed_punctuations = [',', '.', ';', ':', '"', '``', "''", '`']

    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)
                if t not in self.not_needed_punctuations]


# Load tweet data into tweets_data
with open('data/tweets.json') as tweets_file:
    tweets_data = json.load(tweets_file)

# load users data into user_data
with open('data/users.json') as users:
    user_data = json.load(users)

# obtain the tweet text and pop into array_data, map that maps the tweet to an author ID
tweet_data= []
user_id = {}
for tweet in tweets_data:
    tweet_data.append(tweet['text'])
    user_id[tweet['text']]= tweet['author_id']

# map created to map a user ID to a screen name
user_screen= {}
for user in user_data:
    user_screen[user['id_str']] = user['screen_name']

# create first word of tweet the title
title_array = []
for tweet in tweet_data:
    title = tweet.split()[0]
    title_array.append(title)



print('# of tweets:',len(tweet_data))

for index in range(5):
    # print(idx, " \t ", title_array[idx], " : \t", tweet_data[index][:100])
    print(index, " : \t", tweet_data[index][:100])

# query we will use as an example to show ranking
tweet_query = ' heat is cranking'

#use reduce_by_lemma to reduce words to its lemma
lemma = reduce_by_lemma()
stop_lemma = lemma(' '.join(stop_words))
vectorize = TfidfVectorizer(stop_words=stop_lemma, tokenizer=lemma)

vectors = vectorize.fit_transform([tweet_query] + tweet_data)

# Calculate the word frequency, and calculate the cosine similarity of the search terms to the documents
similarities_w_cosine = linear_kernel(vectors[0:1], vectors).flatten()
tweet_scores = [item.item() for item in similarities_w_cosine[1:]]  # convert back to native Python dtypes

# Print the top-scoring results and their titles
score_titles = [(score, title) for score, title in zip(tweet_scores, tweet_data)]

index_of_sim = 0
for score, title in (sorted(score_titles, reverse=True, key=lambda x: x[0])[:10]):
    index_of_sim += 1
    print(index_of_sim, 'Top tweets with similarity:',score, title)

index_of_user = 0
for score, title in (sorted(score_titles, reverse=True, key=lambda x: x[0])[:10]):
    index_of_user += 1
    id =user_id[title]
    print(index_of_user, 'Top Users with similar content:', score, user_screen[id])


