#!/usr/bin/env python
import sys
import hmmtagger

def main():
	if len(sys.argv) < 2:
		print "usage: ./tagger.py frequency_file"
		exit(1)

	# read the wordtag and ngrams from the count file
	wordtag, grams, tag_count = hmmtagger.read_freq(sys.argv[1])

	# emmision parameter e(x|y) is just wordtag[x][y] / count[y]

if __name__ == '__main__':
	main()