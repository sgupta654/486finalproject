# Sandeep Gupta
# sandgupt
# UMID: 28195600
# EECS 486
# 1/24/17

import re
import sys
from stemmer import PorterStemmer

words = {}


# Function that SGML tags
def removeSGML(inputString):
	# Removes instances of SGML tags with A-Z or / in them
	outputString = re.sub('<[A-Z/]*>', '', inputString)
	return outputString

contractions = { 
	"ain't": "am not", # are not; is not; has not; have not
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
	"he'd": "he had", # he would
	"he'd've": "he would have",
	"he'll": "he will", # he shall
	"he'll've": "he will have", # he shall have
	"he's": "he is", # he has
	"how'd": "how did",
	"how'd'y": "how do you",
	"how'll": "how will",
	"how's": "how is", # how has; how does
	"I'd": "I would", # I had
	"I'd've": "I would have",
	"I'll": "I will", # I shall
	"I'll've": "I will have", # I shall have
	"I'm": "I am",
	"I've": "I have",
	"isn't": "is not",
	"it'd": "it would", # it had
	"it'd've": "it would have",
	"it'll": "it will", # it shall
	"it'll've": "it will have", # it shall have
	"it's": "it is", # it has
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
	"she'd": "she would", # she had
	"she'd've": "she would have",
	"she'll": "she will", # she shall
	"she'll've": "she will have", # she shall have
	"she's": "she is", # she has
	"should've": "should have",
	"shouldn't": "should not",
	"shouldn't've": "should not have",
	"so've": "so have",
	"so's": "so is", # so as
	"that'd": "that would", # that had
	"that'd've": "that would have",
	"that's": "that is", # that has
	"there'd": "there would", # there had
	"there'd've": "there would have",
	"there's": "there is", # there has
	"they'd": "they would", # they had
	"they'd've": "they would have",
	"they'll": "they will", # they shall
	"they'll've": "they will have", # they shall have
	"they're": "they are",
	"they've": "they have",
	"to've": "to have",
	"wasn't": "was not",
	"we'd": "we would", # we had
	"we'd've": "we would have",
	"we'll": "we will",
	"we'll've": "we will have",
	"we're": "we are",
	"we've": "we have",
	"weren't": "were not",
	"what'll": "what will", # what shall
	"what'll've": "what will have", # what shall have
	"what're": "what are",
	"what's": "what is", # what has
	"what've": "what have",
	"when's": "when is", # when has
	"when've": "when have",
	"where'd": "where did",
	"where's": "where is", # where has
	"where've": "where have",
	"who'll": "who will", # who shall
	"who'll've": "who will have", # who shall have
	"who's": "who is", # who has
	"who've": "who have",
	"why's": "why is", # why has
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
	"you'd": "you would", # you had
	"you'd've": "you would have",
	"you'll": "you will", # you shall
	"you'll've": "you will have", # you shall have
	"you're": "you are",
	"you've": "you have"
}

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

stopwords = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'but', 'by', 'few', 'from', 'for', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its', 'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their', 'them', 'there', 'they', 'that', 'this', 'to', 'us', 'was', 'what', 'when', 'where', 'which', 'who', 'why', 'will', 'with', 'you', 'your']

# Function that tokenizes the text
	# tokenization of . (do not tokenize acronyms, abbreviations, numbers)
	# tokenization of ' (expand when needed, e.g., I'm -> I am; tokenize the possessive,
	#					e.g., Sunday's -> Sunday 's)
	# tokenization of dates (keep dates together)
	# tokenization of - (keep phrases separated by - together)
	# tokenization of , (do not tokenize numbers)
def tokenizeText(inputString):
	# Split input string into list
	inputList = inputString.split(' ')

	# Remove periods from list
	inputList[:] = [x for x in inputList if x != '.']
	# Remove whitespaces from list
	inputList[:] = [x for x in inputList if x != '']
	# Remove dashes from list
	inputList[:] = [x for x in inputList if x != '-']
	# Remove '..' from list
	inputList[:] = [x for x in inputList if x != '..']
	# Remove './' from list
	inputList[:] = [x for x in inputList if x != './']

	newList = []
	for x in inputList:
		if '\n' in x:
			listWithoutNewLine = x.split('\n')

			# Remove periods from list
			listWithoutNewLine[:] = [x for x in listWithoutNewLine if x != '.']
			# Remove whitespaces from list
			listWithoutNewLine[:] = [x for x in listWithoutNewLine if x != '']

			for y in listWithoutNewLine:
				newList.append(y)		
		else:
			newList.append(x)

	cleanList = []
	for x in newList:
		newWord = ""
		# If word ends with '..'
		if (x.endswith('..')):
			# Remove period from end of word
			newWord = x[0:len(x) - 2]
			cleanList.append(newWord)
			
		# If word starts with '..'
		elif (x.startswith('..')):
			# Remove period from end of word
			newWord = x[2:len(x)]
			cleanList.append(newWord)
		else:
			cleanList.append(x)

	removingTrailingPeriods = []
	for x in cleanList:
		if (x.endswith('.')):
			#cleanList[cleanList.index(x)] = x[:-1]
			# Remove period from end of word
			withoutPeriod = x[0:len(x) - 1]

			if withoutPeriod.isdigit():
				removingTrailingPeriods.append(withoutPeriod)
			else:
				removingTrailingPeriods.append(x)
		else:
			removingTrailingPeriods.append(x)

	for x in removingTrailingPeriods:
		# Remove commas from 
		if (x.endswith(',')):
			removingTrailingPeriods[removingTrailingPeriods.index(x)] = x[:-1]
	

	for x in removingTrailingPeriods:
		if ',' in x:
			commaList = removingTrailingPeriods[removingTrailingPeriods.index(x)].split(',')
			removingTrailingPeriods.pop(removingTrailingPeriods.index(x))
			for y in commaList:
				removingTrailingPeriods.append(y)


	expandingContractions = []
	for x in removingTrailingPeriods:
		if "'" in x:
			if x in contractions:
				con = contractions[x]
				listOfContractions = con.split(' ')
				for y in listOfContractions:
					expandingContractions.append(y)
			else:
				apostropheInd = x.index("'")
				beforeApostrophe = x[:apostropheInd]
				afterApostrophe = x[apostropheInd:]
				expandingContractions.append(beforeApostrophe)
				expandingContractions.append(afterApostrophe)
		else:
			expandingContractions.append(x)

	keepingDatesTogether = []
	index = 0
	while index < len(expandingContractions):
		if expandingContractions[index] in months:
			date = expandingContractions[index]
			possibleDay = expandingContractions[index - 1]
			if possibleDay.isdigit():
				if int(possibleDay) <= 31:
					date = possibleDay + " " + date
					keepingDatesTogether.pop()
			possibleYear = expandingContractions[index + 1]
			if len(possibleYear) == 4:
				index += 1
				date = date + " " + possibleYear
			elif len(possibleYear) == 2:
				index += 1
				date = date + " " + possibleYear
				possibleYearAgain = expandingContractions[index + 1]
				if len(possibleYearAgain) == 4:
					index += 1
					date = date + " " + possibleYearAgain
			keepingDatesTogether.append(date)
		else:
			keepingDatesTogether.append(expandingContractions[index])
		index += 1

	# Removing /
	removingSlashes = []
	for x in keepingDatesTogether:
		newWord = x
		if (newWord.endswith('/')):
			newWord = newWord[0:len(newWord) - 1]
			
		if (newWord.startswith('/')):
			newWord = newWord[1:len(newWord)]

		removingSlashes.append(newWord)

	removedDashes = []
	for x in removingSlashes:
		newWord = x
		if (newWord.endswith('-')):
			newWord = newWord[0:len(newWord) - 1]

		if (newWord.startswith('-')):
			newWord = newWord[1:len(newWord)]

		removedDashes.append(newWord)

	return removedDashes



# Function that removes the stopwords
def removeStopwords(listTokens):
	returnList = []
	for x in listTokens:
		if x not in stopwords:
			returnList.append(x)

	return returnList

# Function that stems the words
def stemWords(listTokens):
	s = PorterStemmer()
	stemmedTerms = []

	for x in listTokens:
		stemmedTerms.append(s.stem(x, 0, len(x) - 1))

	return stemmedTerms

# cranfieldFolder = sys.argv[1]
# filenum = 1
# while (filenum < 1401):
# 	filename = ""
# 	if(filenum < 10):
# 		filename = cranfieldFolder + 'cranfield000' + str(filenum)
# 	elif(filenum < 100):
# 		filename = cranfieldFolder + 'cranfield00' + str(filenum)
# 	elif(filenum < 1000):
# 		filename = cranfieldFolder + 'cranfield0' + str(filenum)
# 	else:
# 		filename = cranfieldFolder + 'cranfield' + str(filenum)

# 	inputString = ""

# 	with open (filename, "r") as myfile:
# 	    inputString=myfile.read()

# 	listWithoutSGML = removeSGML(inputString)
# 	tokenizedText = tokenizeText(listWithoutSGML)
# 	removedStopWords = removeStopwords(tokenizedText)
# 	stemmedWords = stemWords(removedStopWords)

# 	for x in stemmedWords:
# 		if x in words:
# 			words[x] += 1
# 		else:
# 			words[x] = 1

# 	filenum += 1


# all_words = words.items() 
# all_words.sort(key=lambda x: x[1])

# total = 0
# for x in all_words:
# 	total += x[1]

# f = open('preprocess.output', 'w')
# f.write('Words ' + str(total) + '\n')
# f.write('Vocabulary ' + str(len(all_words)) + '\n')
# f.write('Top 50 words\n')
# x = 1

# all_words_length = len(all_words) - 1

# while (x < 51):
# 	f.write(all_words[all_words_length][0] + ' ' + str(all_words[all_words_length][1]) + '\n')
# 	all_words_length -= 1
# 	x += 1

# Unique Words Accounting For 25%:
# y = 0
# all_words_length = len(all_words) - 1
# twenFive = 147998 * .25 
# # 
# collection = 0
# while collection < twenFive:
# 	collection += all_words[all_words_length][1]
# 	all_words_length -= 1
# 	y += 1

# print collection
# print y


# part4wordssubset1 = {}
# cranfieldFolder = sys.argv[1]
# filenum = 100
# while (filenum < 141):
# 	filename = ""
# 	if(filenum < 10):
# 		filename = cranfieldFolder + 'cranfield000' + str(filenum)
# 	elif(filenum < 100):
# 		filename = cranfieldFolder + 'cranfield00' + str(filenum)
# 	elif(filenum < 1000):
# 		filename = cranfieldFolder + 'cranfield0' + str(filenum)
# 	else:
# 		filename = cranfieldFolder + 'cranfield' + str(filenum)

# 	inputString = ""

# 	with open (filename, "r") as myfile:
# 	    inputString=myfile.read()

# 	listWithoutSGML = removeSGML(inputString)
# 	tokenizedText = tokenizeText(listWithoutSGML)
# 	removedStopWords = removeStopwords(tokenizedText)
# 	stemmedWords = stemWords(removedStopWords)

# 	for x in stemmedWords:
# 		if x in part4wordssubset1:
# 			part4wordssubset1[x] += 1
# 		else:
# 			part4wordssubset1[x] = 1

# 	filenum += 1

# all_words_s1 = part4wordssubset1.items() 
# all_words_s1.sort(key=lambda x: x[1])

# totals1 = 0
# for x in all_words_s1:
# 	totals1 += x[1]

# print ('Words Subset 2 ' + str(totals1) + '\n')
# print('Vocabulary Subset 2 ' + str(len(all_words_s1)) + '\n')



# part4wordssubset2 = {}
# cranfieldFolder = sys.argv[1]
# filenum = 800
# while (filenum < 881):
# 	filename = ""
# 	if(filenum < 10):
# 		filename = cranfieldFolder + 'cranfield000' + str(filenum)
# 	elif(filenum < 100):
# 		filename = cranfieldFolder + 'cranfield00' + str(filenum)
# 	elif(filenum < 1000):
# 		filename = cranfieldFolder + 'cranfield0' + str(filenum)
# 	else:
# 		filename = cranfieldFolder + 'cranfield' + str(filenum)

# 	inputString = ""

# 	with open (filename, "r") as myfile:
# 	    inputString=myfile.read()

# 	listWithoutSGML = removeSGML(inputString)
# 	tokenizedText = tokenizeText(listWithoutSGML)
# 	removedStopWords = removeStopwords(tokenizedText)
# 	stemmedWords = stemWords(removedStopWords)

# 	for x in stemmedWords:
# 		if x in part4wordssubset2:
# 			part4wordssubset2[x] += 1
# 		else:
# 			part4wordssubset2[x] = 1

# 	filenum += 1

# all_words_s2 = part4wordssubset2.items() 
# all_words_s2.sort(key=lambda x: x[1])

# totals2 = 0
# for x in all_words_s2:
# 	totals2 += x[1]

# print ('Words Subset 2 ' + str(totals2) + '\n')
# print('Vocabulary Subset 2 ' + str(len(all_words_s2)) + '\n')




















