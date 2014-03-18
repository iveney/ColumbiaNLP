#!/usr/bin/env python
import sys
import hmmtagger

# replace infrequent words x with count(x) < 5 as _RARE_

def main():
	if len(sys.argv) < 2:
		print "usage: ./replace_extended.py training_data"
		exit(1)

	hmmtagger.replace_extended(sys.argv[1])

if __name__ == '__main__':
	main()