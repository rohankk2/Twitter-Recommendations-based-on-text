
class ColumnConstants:
    def __init__(self):
         self.userColumnList = ["user_id","user_id_str","name","screen_name","followers_count","friends_count","statuses_count"]
         self.userColumnMapping = {"user_id":"id","user_id_str":"id_str"}
         self.tweetColumnList = ["id","author_id","tweet_text"]
         self.tweetColumnMapping = {"tweet_text":"text"}

    def getColumnMapping(self,tableName):
        returnedlist = []
        if(tableName == "userTable"):
            returnedlist = self.userColumnList
        elif(tableName == "processedTweets"):
            returnedlist = self.tweetColumnList
        return returnedlist
    def getColumnDict(self,tableName):
        returnedDict = {}
        if(tableName == "processedTweets"):
            returnedDict = self.tweetColumnMapping
        elif(tableName == "userTable"):
            returnedDict = self.userColumnMapping
        return returnedDict


