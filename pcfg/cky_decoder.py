#!/usr/bin/env python

# Expected development total F1-Scores are 0.79 for part 2 and 0.83 for part 3.

import sys
import pcfg

def main():
  if len(sys.argv) < 3:
    print "usage: ./cky_decoder.py count_file test_file"
    exit(1)

  decoder = pcfg.CKYDecoder(sys.argv[1])
  decoder.parse_file(sys.argv[2])

if __name__ == '__main__':
  main()