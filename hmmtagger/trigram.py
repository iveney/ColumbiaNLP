#!/usr/bin/env python
# simple baseline tagger that always produce:
# y* = arg max e(x|y)

import sys
import hmmtagger

def main():
	if len(sys.argv) < 3:
		print "usage: ./trigram.py count_file test_file"
		exit(1)

	tagger = hmmtagger.HMMtagger(sys.argv[1])

	# tag each word using baseline tagger
	with open(sys.argv[2]) as tf:
		data = tf.read()
		sentences = data.split('\n\n')
		tagged = (tagger.trigram(sentence.strip().split()) for sentence in sentences)
		output = '\n\n'.join(tagged)
		print output

if __name__ == '__main__':
	main()