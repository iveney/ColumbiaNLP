#!/usr/bin/env python
from collections import defaultdict, Counter

# only three type of tags:
# I-GENE
# O
# _RARE_

TAGS = ['I-GENE', 'O', '_RARE_']

def read_freq(fn):
	# wordtag[word][tag] gives the frequency of 'word' tagged as 'tag'.
	# it is a dict of dict
	wordtag = collections.defaultdict(dict)

	# index 0 is dummy, rest are n-grams
	grams = [{}, {}, {}, {}]

	# counts the tag, i.e, count(y)
	tag_count = {}
	for tag in TAGS:
		tag_count[tag] = 0

	with open(fn, 'r') as ff:
		for line in ff:
			line = line.split()
			freq = line[0]
			token = line[1]
			if token == 'WORDTAG':
				word = line[3]
				tag = line[2]
				wordtag[word][tag] = int(freq)

			else:
				n = int(token.split('-')[0]);
				# space separated list of tags
				tags = " ".join(line[2:])
				grams[n][tags] = freq	

	return wordtag, grams, tag_count

def replace_infrequent(fn):
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