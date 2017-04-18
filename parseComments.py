import json
import os
import sets
import operator
import re
from stemmer import PorterStemmer
from preprocess import removeSGML, tokenizeText, removeStopwords, stemWords

def tokeText(input_text):
  prewords = input_text.split()
  prev = -1
  tokens = []
  months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
    'september', 'october', 'november', 'december']
  words = []
  skip = 0

  contractions = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what shall have / what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }

  for word in prewords:
    if skip != 0:
      skip = skip - 1
      continue

    pot_date = re.search('[0-9].*', word)
    if pot_date:
      next_word = prewords[prev+1].replace(',','')
      if next_word in months:
        continue

    temp = word.replace(',', '')
    if temp in months:
      date = ''
      if prewords[prev]:
        num = re.search('[0-9].*', prewords[prev])
        if num:
          date = prewords[prev] + word
          if prewords[prev+2]:
            year = re.search('[0-9]+', prewords[prev+2])
            if year:
              date += prewords[prev+2]
              skip += 1
      else:
        date = word
        if prewords[prev+2]:
          day = re.search('[0-9].*', prewords[prev+2])
          if day:
            date += prewords[prev+2]
            skip += 1
        if prewords[prev+3]:
          year = re.search('[0-9]+', prewords[prev+3])
          if year:
            date += prewords[prev+3]
            skip += 1
      words.append(date)
    else:
      words.append(word)

  for word in words:
    added = True
    # check for periods
    period = re.search('.*\..*', word)
    if period:
      added = False
      if len(word) != 1:
        tokens.append(word.lower())

    # check if date
    date = re.search('[0-9]+.[0-9]+.[0-9]+', word)
    if date:
     tokens.append(word.lower())
     added = False

    else:
      for m in months:
        if m in word:
          tokens.append(word.lower())
          added = False

    # handle apostrophes
    apos = re.search('.*\'.*', word)
    if apos:
      added = False
      if word in contractions:
        expanded = contractions[word]
        ex = expanded.split()
        for w in ex:
          tokens.append(w.lower())
      else:
        sep = word.split('\'')
        for w in sep:
          tokens.append(w.lower())

    # handle commas
    comma = re.search('.*,.*', word)
    num = re.search('.*[0-9].*', word)

    if comma and num:
      tokens.append(word.lower())
      added = False
    elif comma:
      sep = word.split(',')
      for w in sep:
        tokens.append(w.lower())
      added = False

    if added:
      if word == '.':
        print word
      tokens.append(word.lower())

  tokens = [x for x in tokens if x != '']
  return tokens


# Recursive function to read comments
def readComments(obj, commentCount, subreddit, comment_corpus, user_links, comment_counts):
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

		# add contents to the comment corpus
		if subreddit in comment_corpus:
			temp_content = ' ' + content
			comment_corpus[subreddit] += temp_content
			comment_counts[subreddit] += 1
		else:
			comment_corpus[subreddit] = content
			comment_counts[subreddit] = 1

		# Update user links
		if author in user_links:
			user_links[author].add(subreddit)
		else:
			user_links[author] = {subreddit}

		#print author + ' ' + content + '\n'
		#commentCount = commentCount + 1
		#print commentCount
		if comment_counts[subreddit] > 200:
			return

		# Does it have a reply?
		if 'replies' in i['data']:
			if len(i['data']['replies']) > 0:
				readComments(i['data']['replies']['data']['children'], commentCount, subreddit, comment_corpus, user_links, comment_counts)

directory = './r'
comment_corpus = {}
comment_counts = {}
user_links = {}
for subreddit in os.listdir(directory):
	if subreddit != '.DS_Store':
		print(subreddit)
		for my_file in os.listdir(directory+'/'+subreddit):
			#print subreddit + ' ' + my_file
			try:
				json_data = open(directory+'/'+subreddit+'/'+my_file)
				commentThread = json.load(json_data)
				commentCount = 0
				readComments(commentThread[1]['data']['children'], commentCount, subreddit, comment_corpus, user_links, comment_counts)
			except ValueError:
				continue
		#print('comments: ' + str(comment_counts[subreddit]))

tokenized_comments = {}
print('Tokenizing text...')
for key, value in comment_corpus.items():
	print(key)
	tokenizedText = tokeText(value)
	removedStopWords = removeStopwords(tokenizedText)
	tokenized_comments[key] = tokenizedText

json_out = open('comments.json', 'w')
json.dump(tokenized_comments, json_out)
json_out.close()
# for key, value in tokenized_comments.items():
# 	if key != "announcements":
# 		for it in value:
# 			if '/r/' in it:
# 				temp = re.search('(?<=\/r\/)[A-Za-z]+(?=\/)', it)
# 				subr = temp.group(0)
# 				if subr != key and comment_corpus.has_key(subr):
# 					print 'true ' + key + ' ' + subr


# Format user link output to file
# in format:
#		subreddit1 subreddit2
# This represents two links, one going each direction.
ul = open('userLinks.txt', 'w')
subreddit = set()

for user in user_links:
	subs = list(user_links[user])
	for x in xrange(len(subs)):
		for y in range(x+1, len(subs)):
			temp = [subs[x], subs[y]]
			temp.sort()
			tmp = (temp[0], temp[1])
			subreddit.add(tmp)

for pair in subreddit:
	line = pair[0] + ' ' + pair[1] + '\n'
	ul.write(line)
