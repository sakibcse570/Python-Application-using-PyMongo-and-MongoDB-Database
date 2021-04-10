import pymongo as pm
import datetime

fh = open("Vocabulary_set.csv","r")   #opening the file 
wd_list = fh.readlines()   #reading the file

wd_list.pop(0)   #removing header which is at 0th index

vocab_list = [] 

for rawstring in wd_list:   #taking raw data from the list
    word, defination = rawstring.split(',', 1)   #this will split the word apart from the defination and put them in the tuple word and defination
    defination = defination.rstrip()   #Strip off the new lines from the defination part
    vocab_list.append({'word': word, 'defination': defination})   #adding defination to our list
    #print(vocab_list)   #output: list of word and their definations on JSON style format

client = pm.MongoClient("mongodb://localhost:27017/")   #set connection string url (localhost)
db = client["vocab"]   #Creating the database 

dbs = client.list_database_names()   #list of the databases
vocab_collection = db["vocab_list"]   #Creating vocab collection
vocab_collection.drop()   #drop / delete database 

vocab_dict = {'word':'cryptic', 'defination':'secrect with hidden meaning'}
result = vocab_collection.insert_one(vocab_dict)   #insert a single document in database so that our database exists
print('inserted_id: ', result.inserted_id)   #print inserted id (though it is optional , MongoDB assigns one upon insert)

if "vocab" in dbs:           #checking that our created databse is listed / exists or not!
    print("Database Exists!")
result = vocab_collection.insert_many(vocab_list)   #insert list of documents
#print(result.inserted_ids)
data = vocab_collection.find_one()    #Retrieve one document from the collection
print(data)

for data in vocab_collection.find({}, {"_id":0, "defination":0}):  #Retrieve all document from the collection excluding id and defination  
    print(data)

data = vocab_collection.find_one({'word':'boisterous'})   #Query one data by filtering 
print(data)

update = vocab_collection.update_one({'word':'boisterous'},   #update 1 document in database
 {"$set": {"defination": "rowdy; noisy"}})     #setting updated value 

print("modified count: ", update.modified_count)   #checking modified count
data = vocab_collection.find_one({'word':'boisterous'})   #checking updated document in database
print(data)

update = vocab_collection.update_many({}, {"$set":{"last_updated UTC:":   #update all document in database
datetime.datetime.utcnow().strftime('%Y-%m-%d%H%M%SZ')}})                 #adding date time for each document in update
print('modified_count:', update.modified_count)
for data in vocab_collection.find({}, {"_id":0, "defination":0}):
    print(data)


