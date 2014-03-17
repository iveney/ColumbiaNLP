#!/usr/bin/env python
from collections import defaultdict, Counter
import operator

# only two type of tags:
# I-GENE
# O

# given an iterable of pairs return the key corresponding to the greatest value
def argmax(pairs):
    return max(pairs, key = operator.itemgetter(1))[0]

class HMMtagger:
	def __init__(self, fn):
		""" read the wordtag and ngrams from the count file """
		# wordtag[word][tag] gives the frequency of 'word' tagged as 'tag'.
		# it is a dict of dict
		self.wordtag = defaultdict(dict)

		self.grams = {1:{}, 2:{}, 3:{}}

		# counts the tag, i.e, count(y)
		self.tag_count = {'I-GENE': 0, 'O': 0}

		with open(fn, 'r') as ff:
			for line in ff:
				line = line.split()
				freq = line[0]
				token = line[1]
				if token == 'WORDTAG':
					word = line[3]
					tag = line[2]
					self.wordtag[word][tag] = int(freq)
					self.tag_count[tag] += int(freq)

				else:
					n = int(token.split('-')[0]);
					# space separated list of tags
					tags = " ".join(line[2:])
					self.grams[n][tags] = freq	

	def replace_sentence(self, sentence):
		return (self.replace_word(word) for word in sentence.split())

	def replace_word(self, word):
		""" Replace word with '_RARE_' """
		if word not in self.wordtag:
			return '_RARE_'
		else:
			return word

	def emission_prob(self, word, tag):
		""" emmision parameter e(x|y) is just wordtag[x][y] / count[y] """
		if tag in ["*", "STOP"] : return 0.0
		return 1.0 * self.wordtag[word][tag] / self.tag_count[tag]

	def trigram_prob(self, u, v, w):
		""" Computes trigram MLE q(w|u,v) """

	def unigram(self, words):
		tagged = []
		for word in words:
			replaced = self.replace_word(word)
			emissions = [(tag, self.emission_prob(replaced, tag)) for tag in self.wordtag[replaced]]
			tag = word + ' ' + argmax(emissions)
			tagged.append(tag)
		return '\n'.join(tagged)

	# computes paramters:
	# - emission e(x|y)
	# - trigram q: q(y[i]|y[i-2], [yi-1])
	# def compute_parameters(wordtag, grams, tag_count):
	# 	emission = defaultdict(dict)
	# 	for word, tagcounts in wordtag.iteritems():
	# 		for tag, count in tagcounts.iteritems():
	# 			emission[word][tag] = 1.0 * count / tag_count[tag]
	# 	return emission


def replace_infrequent(fn):
	""" Replace words in file 'fn' with count(word) < 5 as '_RARE_' """
	count = defaultdict(int)
	with open(fn, 'r') as ff:
		lines = (line.rstrip() for line in ff)   # All lines including the blank ones
		lines = (line for line in lines if line) # Non-blank lines
		words = (line.split()[0] for line in lines)

		# count the words
		wordcount = Counter(words)
		infrequent = {key for key, value in wordcount.iteritems() if value < 5}

		# replace the infrequent words
	with open(fn, 'r') as ff:
		lines = (line.rstrip() for line in ff)   # All lines including the blank ones
		for line in lines:
			if line and line.split()[0] in infrequent:
				print '_RARE_', line.split()[1]
			else:
				print line	

