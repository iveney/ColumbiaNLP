#!/usr/bin/env python
from collections import defaultdict, Counter
import itertools
import operator

# only two type of tags:
# I-GENE
# O

# given an iterable of pairs return the key corresponding to the greatest value
def argmax(pairs):
    return max(pairs, key = operator.itemgetter(1))[0]

def argmax_pair(pairs):
    return max(pairs, key = operator.itemgetter(1))

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
				freq = int(line[0])
				token = line[1]
				if token == 'WORDTAG':
					word = line[3]
					tag = line[2]
					self.wordtag[word][tag] = freq
					self.tag_count[tag] += freq

				else:
					n = int(token.split('-')[0]);
					# space separated list of tags
					tags = " ".join(line[2:])
					self.grams[n][tags] = freq

	def replace_words(self, words):
		return (self.replace_word(word) for word in words)

	def replace_word(self, word):
		""" Replace word with '_RARE_' """
		if word == 'STOP' or word in self.wordtag:
			return word
		else:
			return '_RARE_'

	def emission_prob(self, word, tag):
		""" emmision parameter e(x|y) is just wordtag[x][y] / count[y] """
		if tag in ["*", "STOP"] : return 0.0
		self.wordtag[word].setdefault(tag, 0)
		return 1.0 * self.wordtag[word][tag] / self.tag_count[tag]

	def trigram_prob(self, w, u, v):
		""" Computes trigram MLE q(v|w,u) = count(w, u, v) / count(w,u)
			where v could be 'STOP', and w, u could be '*'
		"""
		tri = ' '.join([w, u, v])
		bi = ' '.join([w, u])
		return 1.0 * self.grams[3][tri] / self.grams[2][bi]

	def unigram(self, words):
		if not words:
			return ''

		tagged = []
		for word in words:
			replaced = self.replace_word(word)
			emissions = [(tag, self.emission_prob(replaced, tag))
						  for tag in self.wordtag[replaced]]
			tag = word + ' ' + argmax(emissions)
			tagged.append(tag)
		return '\n'.join(tagged)

	def trigram(self, words):
		def q(w, u, v): return self.trigram_prob(w, u, v)
		def e(x, v): return self.emission_prob(x, v)
		def choose_S(k): return ['*'] if k < 0 else ['O', 'I-GENE']

		if not words:
			return ''

		# nested 3-d dict
		pi = defaultdict(lambda : defaultdict(defaultdict))
		bp = defaultdict(lambda : defaultdict(defaultdict))
		pi[-1]['*']['*'] = 1.0

		n = len(words)
		for k in range(n): # 0 .. n-1
			Sw = choose_S(k-2)
			Su = choose_S(k-1)
			Sv = choose_S(k)
			x = self.replace_word(words[k])
			for u, v in itertools.product(Su, Sv):
				pair = argmax_pair(((w, pi[k-1][w][u] * q(w, u, v) * e(x, v))
									 for w in Sw))
				bp[k][u][v] = pair[0]
				pi[k][u][v] = pair[1]

		tags = [None] * n
		# try:
		tags[n-2:n] = argmax( ( [u,v], pi[n-1][u][v] * q(u, v, 'STOP') )
								for u in choose_S(n-2) for v in choose_S(n-1))
		# except Exception as e:
		# 	print pi
		# 	print pi[n-1]
		# 	print type(e)
		# 	print e.args
		# 	print e
		# 	print choose_S(n-3)
		# 	print choose_S(n-2)
		# 	print n, words

		# trace back
		for k in xrange(n-3, -1, -1):
			tags[k] = bp[k + 2][tags[k + 1]][tags[k + 2]]

		# join as 'word' 'tag' 
		tagged = (' '.join(pair) for pair in zip(words, tags))
		# return each pair at a line
		return '\n'.join(tagged)


def replace_infrequent(fn):
	""" Replace words in file 'fn' with count(word) < 5 as '_RARE_' """
	count = defaultdict(int)
	with open(fn, 'r') as ff:
		# All lines including the blank ones
		lines = (line.rstrip() for line in ff)
		# Non-blank lines
		lines = (line for line in lines if line)
		words = (line.split()[0] for line in lines)

		# count the words
		wordcount = Counter(words)
		infrequent = {key for key, value in wordcount.iteritems() if value < 5}

		# replace the infrequent words
	with open(fn, 'r') as ff:
		lines = (line.rstrip() for line in ff)
		for line in lines:
			if line and line.split()[0] in infrequent:
				print '_RARE_', line.split()[1]
			else:
				print line	

