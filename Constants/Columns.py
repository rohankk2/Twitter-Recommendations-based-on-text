
class ColumnConstants:
    def __init__(self):
         self.userColumnList = ["user_id","user_id_str","name","screen_name","followers_count","friends_count","statuses_count"]
         self.userColumnMapping = {"user_id":"id","user_id_str":"id_str"}

    def getColumnMapping(self,tableName):
        returnedlist = []
        if(tableName == "userTable"):
            returnedlist = self.userColumnList
        return returnedlist
    def getColumnDict(self,tableName):
        returnedDict = {}
        if(tableName == "userTable"):
            returnedDict = self.userColumnMapping
        return returnedDict


