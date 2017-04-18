from sys import argv
from os import listdir
from operator import itemgetter
from re import split
from dictionaries import *
from PorterStemmer import PorterStemmer

def removeSGML(input_string):
	output_string = ''
	bracket_open = False
	for c in input_string:
		if c == '<':
			bracket_open = True
		elif c == '>' and bracket_open == True:
			bracket_open = False
		elif bracket_open == False:
			output_string += c
	return output_string

def is_number(string):
	try:
		float(string.replace(',', ''))
		return True
	except:
		return False

def tokenize(input_word):
	tokens = []
	# apostraphe
	if '\'' in input_word:
		index = input_word.find('\'')
		if contractions.has_key(input_word):
			# contracton
			tokens = contractions[input_word].split(' ')
		elif input_word[len(input_word)-1] == 's':
			#possesive
			token = input_word.split('\'')
	# number
	elif is_number(input_word):
		# do not tokenize numbers
		tokens = []
	# period
	elif '.' in input_word:
		# if it is just a period, it's a sentence ender
		# otherwise, it's allowed
		if len(input_word) != 1:
			tokens = [input_word]
	elif ',' in input_word:
		# if , is at the end of the word, it is naturally occuring in the sentence
		# otherwise it is covered by the number case
		tokens = input_word.split(',')
	elif '-' in input_word:
		# if only a hyphen (aka used in place of commas) don't tokenize
		# otherwise do
		if len(input_word) != 1:
			tokens = [input_word]
	# normal words
	else:
		tokens = [input_word]
	return tokens

def tokenizeText(input_string):
	token_list = []
	words = input_string.replace('\n', ' ').split(' ')
	for index in range(0, len(words)):
		word = words[index].lower()
		tokens = []
		# handle dates in advance
		if word in months:
			# check for month day year
			if len(words[index+1]) == 2 and (len(words[index+2]) == 2 or len(words[index+2]) == 4):
				tokens = [str(word + ' ' + words[index+1] + ' ' + words[index + 2])]
				index += 2
			# check for month year
			elif len(words[index+1]) == 2 or len(words[index+1]) == 4:
				tokens = [str(word + ' ' + words[index + 1])]
				index += 1
			# else just tokenize word
			else:
				tokenize(word)
		else:
			tokens = tokenize(word)
		for token in tokens:
			token_list.append(token)
		index += 1
	while '' in token_list:
		token_list.remove('')
	return token_list

def removeStopwords(tokens):
	i = 0
	while i < len(tokens):
		if tokens[i] in stopwords:
			del tokens[i]
		else:
			i += 1
	return tokens

def stemWords(raw_tokens):
	p = PorterStemmer()
	stemmed_tokens = []
	for token in raw_tokens:
		stemmed_token = p.stem(token, 0, len(token)-1)
		stemmed_tokens.append(stemmed_token)
	return stemmed_tokens

def main():
	folder = argv[1]
	num_words = 0
	word_dict = {}
	for filename in listdir(folder):
		datafile = open(str(folder + '/' + filename), 'r')
		data = datafile.read()
		data = removeSGML(data)
		tokens = tokenizeText(data)
		tokens = removeStopwords(tokens)
		tokens = stemWords(tokens)
		datafile.close()

		num_words += len(tokens)
		for token in tokens:
			if word_dict.has_key(token):
				word_dict[token] += 1
			else:
				word_dict[token] = 1

	with open('preprocess.output', 'w') as output:
		output.write('Words' + ' ' + str(num_words) + '\n')
		output.write('Vocabulary' + ' ' + str(len(word_dict.keys())) + '\n')
		output.write('Top 50 words\n')
		frequent_words = sorted(word_dict.items(), key=itemgetter(1))
		frequent_words = list(reversed(frequent_words))

		# # used to calculate up to 25% of total words
		# sum = 0
		# index = 0
		# while sum < 34887:
		# 	sum += (frequent_words[index])[1]
		# 	index += 1
		# print index


		frequent_words = frequent_words[:50]

		for word in frequent_words:
			output.write(word[0] + ' ' + str(word[1]) + '\n')

	return

if __name__ == '__main__':
	main()
