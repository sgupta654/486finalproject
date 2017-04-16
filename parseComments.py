import json
import os


# Recursive function to read comments
def readComments(obj, commentCount):
	newComments = 0
	existingComments = 0
	for i in obj:

		if 'data' not in i:
			return

		# Basic info, present both in Title and Comment
		commentId = i['data']['id']
		content = ""
		author = ""
		url = ""
		score = 0
		created = 0
		if 'created_utc' in i['data']:
			created = i['data']['created_utc']
		else:
			print "*** WARNING: created_utc not found in this record -> " + commentId

		# Is it a comment?
		if 'body' in i['data']:

			content = i['data']['body']
			ups = int(i['data']['ups'])
			downs = int(i['data']['downs'])
			author = i['data']['author']

			score = ups - downs

		# Or is it the title post?
		elif 'selftext' in i['data']:

			url = i['data']['url']
			content = i['data']['selftext']
			score = i['data']['score']


		print author + ' ' + content + '\n'
		commentCount = commentCount + 1
		print commentCount

		# Does it have a reply?
		if 'replies' in i['data']: 
			if len(i['data']['replies']) > 0:
				readComments(i['data']['replies']['data']['children'], commentCount)
directory = '/Users/sandeepgupta/Desktop/EECS_486/final_project/get-comments-json/RedditSocialGrapher/r'
for subreddit in os.listdir(directory):
	if subreddit != '.DS_Store':
		for my_file in os.listdir(directory+'/'+subreddit):
			print subreddit + ' ' + my_file
			json_data = open(directory+'/'+subreddit+'/'+my_file)
			commentThread = json.load(json_data)
			commentCount = 0
			readComments(commentThread[1]['data']['children'], commentCount)

