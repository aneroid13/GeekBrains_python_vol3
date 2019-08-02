import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["new_test_db"]
mycol = mydb["mycollection"]

#myquery = {"address": "Park Lane 38" }

# mydoc = mycol.find()

'''
mydict = { "town": "Klyzma", "population": 400000 }
x = mycol.insert_one(mydict)
'''

myquery = {"town": "Klyzma"}
newvalues = { "$set": { "telefon_code": "8348"} }

mycol.update_one(myquery, newvalues)


'''
mydoc = mycol.find()

for x in mydoc:
  #print(x['town']) 
  print(x)
'''
