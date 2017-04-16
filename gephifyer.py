import commentCompile
import sys
import pickle

"""Run this file to take a pickled database and extract one subreddit's data into a Gephi-compatible file"""


#subreddit = "programming"
subreddit = sys.argv[1]
if len(sys.argv) > 2:
    cutoff = int(sys.argv[2])
else:
    cutoff = 2

if subreddit[-4:] == ".svg":
    subreddit = subreddit[:-4]

path = "./r/" + subreddit

try:
    load = open("DBs/" + subreddit + "_db.pickle", "r")
    DB = pickle.load(load)
    load.close()
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)    
    quit()

archive = DB

output = open("out/" + subreddit + str(cutoff) + ".csv", "w")

for person in archive:
        if (person == "[deleted]"):
            continue #skip [deleted]
        bufferstr = archive[person].ID + ","
        for repliedTo in archive[person].replies:  
            if repliedTo == "[deleted]":
                continue
            for x in range(0, archive[person].replies[repliedTo]): # append the number of times person replied to.
                bufferstr += repliedTo + ","
        bufferstr = bufferstr[:-1] # strip the trailing comma
        bufferstr += "\n"

        """ skips if the user only replied to one person, once """
        if len(bufferstr.split(",")) > cutoff:
            output.write(bufferstr) 
