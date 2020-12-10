import json
import numpy as np
import math
import nltk
from nltk.corpus import stopwords
import gensim
from gensim import models
import string
import re


class Corpus(object):

    """
    A collection of documents.
    """

    def __init__(self, documents_path):
        """
        Initialize empty document list.
        """
        nltk.download('stopwords')

        self.documents = []
        self.vocabulary = []
        self.likelihoods = []
        self.documents_path = documents_path
        self.term_doc_matrix = None
        self.dictionary ={}
        self.stop_words = stopwords.words("english")
        self.number_of_documents = 0
        self.vocabulary_size = 0
        self.sw = ["i'm","i’m","lol","much","like","dont","know","pst","amp","don't","need","like","de","go","still","get",'','you\'re']

    ## Function  taken from https://github.com/enoreese/topic-modelling/blob/master/preprocessor.py
    def remove_emoji(self,text):
        emoji_pattern = re.compile("[" u"\U0001F600-\U0001F64F"
                      u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        return text
    ## Function  taken from https://github.com/enoreese/topic-modelling/blob/master/preprocessor.py
    def remove_links(self,text):
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'bit.ly/\S+', '', text)
        text = text.strip('[link]')
        return text
    ## Function  taken from https://github.com/enoreese/topic-modelling/blob/master/preprocessor.py
    def remove_users(self,text):
        text = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', text)
        text = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', text)
        return text

    ## Function  taken from https://github.com/enoreese/topic-modelling/blob/master/preprocessor.py
    def clean_tweet(self,tweet):
        tweet = tweet.lower()
        tweet = self.remove_users(tweet)
        tweet = self.remove_links(tweet)
        tweet = self.remove_emoji(tweet)
        my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'
        tweet = re.sub('['+my_punctuation + ']+',' ', tweet)
        tweet = re.sub('\s+', ' ', tweet)
        tweet = re.sub('([0-9]+)', '', tweet)
        stop_words = stopwords.words('english') + stopwords.words('spanish')
        print("here")
        tweet_token_list = [word for word in tweet.split(' ') if word not in stop_words and word not in self.sw and len(word) > 2]
        return tweet_token_list
    def build_corpus(self):
        """
        Read document, fill in self.documents, a list of list of word
        self.documents = [["the", "day", "is", "nice", "the", ...], [], []...]

        Update self.number_of_documents
        """
        # #############################
        # your code here
        # #############################
        data =[]
        with open(self.documents_path) as f:
            data = json.load(f)
        self.number_of_documents = 10001
        i=0
        for tweet in data:
            words =self.clean_tweet(tweet['text'])
            finalwords = [word for word in words if  word not in self.sw and word != '']
            self.documents.append(finalwords)
            i=i+1
            if(i>10000):
                break
        self.dictionary = gensim.corpora.Dictionary(self.documents)

    def build_vocabulary(self):
        """
        Construct a list of unique words in the whole corpus. Put it in self.vocabulary
        for example: ["rain", "the", ...]

        Update self.vocabulary_size
        """
        # #############################
        # your code here
        # #############################
        seen = {}
        uniquewords=0
        for words in self.documents:
            for word in words:
                if(word in seen.keys()):
                    continue
                else:
                    seen[word]=1
                    self.vocabulary.append(word)
                    uniquewords=uniquewords+1
        self.vocabulary_size=uniquewords

    def build_term_doc_matrix(self):
        """
        Construct the term-document matrix where each row represents a document,
        and each column represents a vocabulary term.

        self.term_doc_matrix[i][j] is the count of term j in document i
        """
        # ############################
        # your code here
        # ############################
        self.term_doc_matrix = np.zeros((self.number_of_documents, self.vocabulary_size), dtype=np.int16)
        mappingdict={}
        i=0
        for word in self.vocabulary:
            mappingdict[word]=i
            i=i+1
        documentnumber =0
        for words in self.documents:
            for word in words:
                wordinvocab=mappingdict[word]
                self.term_doc_matrix[documentnumber][wordinvocab]= self.term_doc_matrix[documentnumber][wordinvocab]+1
            documentnumber = documentnumber+1
    def run_lda(self):
        corpus = [self.dictionary.doc2bow(list_of_tokens) for list_of_tokens in self.documents]
        num_topics = 26
        Lda = models.LdaMulticore
        self.lda= Lda(corpus,num_topics,id2word = self.dictionary,passes=20,chunksize=2000,random_state=3)
        print(self.documents[0])
        print(corpus[0])

        for idx, topic in self.lda.print_topics(-1):
            print("Topic: {} \nWords: {}".format(idx, topic ))
            print("\n")
        return self.lda
    def tweet_topic(self,lda):
        corpus = [self.dictionary.doc2bow(list_of_tokens) for list_of_tokens in self.documents]

        print(lda.get_document_topics(corpus[0]))






def main():
    documents_path = 'data/tweets.json'
    corpus = Corpus(documents_path)  # instantiate corpus
    corpus.build_corpus()
    corpus.build_vocabulary()
    print(corpus.vocabulary)
    print("Vocabulary size:" + str(len(corpus.vocabulary)))
    print("Number of documents:" + str(len(corpus.documents)))
    lda =corpus.run_lda()
    corpus2 = Corpus('data/testtweets.json')
    corpus2.build_corpus()
    corpus2.build_vocabulary()
    corpus2.tweet_topic(lda)




if __name__ == '__main__':
    main()
