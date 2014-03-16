#!/usr/bin/env python
import sys
import os

# def compute_emission():

def read_freq(fn):
	with open(fn, 'r') as ff:
		wordtag = dict()	# wordtag[word] gives the frequency and tag
		grams = [{}, {}, {}, {}] # index 0 is dummy, rest are n-grams
		for line in ff:
			line = line.split()
			freq = line[0]
			tag = line[1]
			if tag == 'WORDTAG':
				wordtag[line[3]] = {'freq': freq, 'tag': line[2]}
			else:
				n = int(tag.split('-')[0]);
				# space separated list of tags
				tags = " ".join(line[2:])
				grams[n][tags] = freq	

	return wordtag, grams

def main():
	if len(sys.argv) < 2:
		print "usage: ./tagger.py frequency_file"
		exit(1)

	# read the wordtag and ngrams from the count file
	wordtag, grams = read_freq(sys.argv[1])

	# now that we have wordtag and ngrams, compute emission parameters e(x|y)


if __name__ == '__main__':
	main()