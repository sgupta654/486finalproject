import commentCompile
import os
import json
import pickle
import sys

"""Call this file to process saved json files into pickle files.
If an argument is provided, will only process said subreddit."""

DBList = dict()

jsonlist = dict() # lists the path and json file name for all files in ./r/

subreddit = ""
if len(sys.argv) > 1:
    subreddit = sys.argv[1]
    if subreddit[-4] == ".":
        subreddit = subreddit[:-4]    


# Only walk directory for one subreddit if applicable.
for path, dirs, files in os.walk("r/" + subreddit):
    for f in files:
        #print path + "/" + f
        if not path in jsonlist:
            jsonlist[path] = list()
        jsonlist[path].append(f)

for directory in jsonlist:
    if not directory in DBList:
        DBList[directory] = dict()
    for filename in jsonlist[directory]:
        commentCompile.parseJSON(DBList[directory], directory + "/" + filename)

for key in DBList:
    name = key[2:] # Strip the r/ from the path.
    save = open("DBs/" + name + "_db.pickle", "w")
    pickle.dump(DBList[key], save)
    save.close()
