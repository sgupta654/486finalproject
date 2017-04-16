import json
import os

""" This module defines methods and a class to take a Reddit archive and create a representation of who replied to whom."""




class Person:
    def __init__(self, ID):
        self.ID = ID
        self.replies = dict() # The number of replies & to whom this person has made.
        self.parents = list() # Links to comments that were replied to by other people, or that the Person replied to.
        self.commentsMade = 0
        self.commentsRecieved = 0
    
    def addReply(self, repliedTo):
        if repliedTo in self.replies:
            self.replies[repliedTo] += 1
        else:
            self.replies[repliedTo] = 1

    def __str__(self):
        str = "/u/%s replied to:" % (self.ID)
        for k in self.replies:
            str += "\n    /u/%s : %d" % (k, self.replies[k])
        return str

"""A recursive function that traverses the comment tree"""
def readComment(DB, tree, author, authorData, permalink): 
# The author is the  person who the 'current' person replied to;
# that is, this function adds a reply to all the children of that comment
    link = permalink + authorData["id"] # reddit.com/r/subreddit/comments/threadID/threadname/commentID>
    DB[author].parents.append(link);
    
    for reply in tree:
        if not reply["kind"] == "t1":
            continue
        current = reply["data"]["author"]
        if not current in DB:
            DB[current] = Person(current)
        DB[current].addReply(author)
        DB[current].parents.append(link);
        if len(reply["data"]["replies"]) > 0:
            readComment(DB, reply["data"]["replies"]["data"]["children"], current, reply["data"], permalink)
        

"""This is the function to call. 
DB is a dict() of People. filename is a string that represents a path to the json file. parseJSON() must be called once for each json file."""
def parseJSON(DB, filename):
    with open(filename, 'r') as jsonfile:
        rawdata = jsonfile.read()
    data = json.loads(rawdata)

    OP = data[0]["data"]["children"][0]["data"]["author"]
    permalink = data[0]["data"]["children"][0]["data"]["permalink"]
    if not OP in DB:
        DB[OP] = Person(OP);
    for rep in data[1]["data"]["children"]:
        if not rep["kind"] == "t1" or rep["kind"] == "Listing":
            continue
        author = rep["data"]["author"]
        if not author in DB:
            DB[author] = Person(author)
        DB[author].addReply(OP)
        if len(rep["data"]["replies"]) > 0:
            replies = rep["data"]["replies"]["data"]["children"]
            readComment(DB, replies, rep["data"]["author"], rep["data"], permalink)
    
    incomingReplies = dict()
    for key in DB:
        DB[key].commentsMade = len(DB[key].replies);
        # Compile a list of how many times each person recieved a reply.
        for person in DB[key].replies:
            if not person in incomingReplies:
                incomingReplies[person] = DB[key].replies[person]
            else:
                incomingReplies[person] += DB[key].replies[person]
    
    # May cause a problem with people only recieving a reply.
    for person in incomingReplies:
        if not person in DB:
            buffer = Person(person)
            buffer.commentsRecieved = incomingReplies[person]
            DB[person] = buffer
        else:
            DB[person].commentsRecieved = incomingReplies[person]
