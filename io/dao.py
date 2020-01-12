import pymongo


def clearCol(col):
    x = col.delete_many({})
    print(x.deleted_count, " listings deleted")


class DataWriter():
    def __init__(self, box):
        self.client = pymongo.MongoClient("mongodb://192.168.1.6:27017/")
        self.db = self.client["database"]
        self.collection = self.db[box]

    def clearData(self):
        x = self.collection.delete_many({})
        return x.deleted_count

    def writeMany(self, data):
        if len(data) > 0:
            self.collection.insert_many(data)

    def writeOne(self, data):
        self.collection.insert_one(data)

    def getData(self, field, amt, sort, filter):
        return self.collection.find(filter, {"_id": 0}).sort(field, sort).limit(amt)


class GamesDao(DataWriter):
    def lookForMatch(self, matchId):
        return self.collection.find({"match_id": matchId})


class PerformancesDao(DataWriter):
    def getWins(self, match):
        pipeline = [
            match,
            {"$group": {
                "_id": "$account_id",
                "name": {"$last": "$steamName"},
                "wins": {"$sum": "$win"}
            }},
            {"$project": {"_id": 0, "account": "$_id", "wins": 1, "name": 1}},
            {"$sort": {"wins": -1}},
            {"$limit": 10}
        ]
        top = list(self.collection.aggregate(pipeline))
        for player in top:
            player["dotabuff"] = "https://www.dotabuff.com/players/%d" % (player["account"])
        print(top)

# db.performances.aggregate([
#   {$match: {}},
#   {$group: { _id:"$account_id", name:{$last: "$steamName"}, wins: {$sum: "$win"}}},
#   {$project: {_id: 0, account: "$_id", wins: 1, name: 1}},
#   {$sort: {wins: -1}},
#   {$limit: 10}
# ])
