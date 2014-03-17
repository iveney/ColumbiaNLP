#!/usr/bin/env python
# simple baseline tagger that always produce:
# y* = arg max e(x|y)

import sys
import hmmtagger

def main():
	if len(sys.argv) < 3:
		print "usage: ./p1tagger.py count_file test_file"
		exit(1)

	# read the wordtag and ngrams from the count file
	# wordtag, grams, tag_count = hmmtagger.read_freq(sys.argv[1])
	tagger = hmmtagger.HMMtagger(sys.argv[1])

	# tag each word using baseline tagger
	with open(sys.argv[2]) as tf:
		data = tf.read()
		sentences = data.split('\n\n')
		tagged = (tagger.unigram(sentence.split()) for sentence in sentences)
		output = '\n'.join(tagged)
		print output

	# emmision parameter e(x|y) is just wordtag[x][y] / count[y]

if __name__ == '__main__':
	main()