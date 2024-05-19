from pymongo import MongoClient
import datetime
import time
import os

db_instance = MongoClient(os.getenv("DB_CONNECTION_STRING"))

database = db_instance['drive_api']

folder_cache_collection = database['folderCache']
file_cache_collection = database['fileCache']

#Creating indexes for easy expiry
folder_cache_collection.create_index("addedOn", expireAfterSeconds=10*24*60*60) #expires after 10 days
file_cache_collection.create_index("addedOn", expireAfterSeconds=10*24*60*60) #expires after 10 days


def addToFileCache(uid,data):
    file_cache_collection.insert_one({
        "_id":uid,
        "response":data,
        "addedOn":datetime.datetime.now(datetime.timezone.utc)
    })


def addToFolderCache(uid,data):
    folder_cache_collection.insert_one({
        "_id":uid,
        "response": data,
        "addedOn": datetime.datetime.now(datetime.timezone.utc)
    })

def findFromFileCache(uid):
    return file_cache_collection.find_one({"_id":uid})

def findFromFolderCache(uid):
    return folder_cache_collection.find_one({"_id":uid})

if __name__=="__main__":
    start = time.time()
    # addToFolderCache("1mURYosXIDbqSzDYlnlqRtoKJzbv1KJ5M",{
    #     "success": False,
    #     "msg": "Provided Folder is not publicly shared",
    #     "err": "FOLDER_NOT_ACCESSIBLE"
    # })
    print(findFromFolderCache("1mURYosXIDbqSzDYlnlqRtoKJzbv1KJ5X"))
    print(time.time() - start)