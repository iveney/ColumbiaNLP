#!/usr/bin/env python

import sys
import pcfg

def main():
  if len(sys.argv) < 2:
    print "usage: ./replace_infrequent.py training_data"
    exit(1)

  p = pcfg.RareWordReplacer(sys.argv[1])
  p.replace_infrequent()
  p.dump_trees()

if __name__ == '__main__':
  main()