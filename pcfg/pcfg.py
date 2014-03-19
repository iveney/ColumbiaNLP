import sys, json
import count_cfg_freq
from collections import defaultdict

class PCFG:
  def __init__(self, fn):
    "Read all the trees from file and get counts"
    self.trees = []
    self.counter = count_cfg_freq.Counts()
    self.wordcount = defaultdict(int)
    self.rarewords = {}

    for l in open(fn):
      t = json.loads(l)
      self.counter.count(t)
      self.trees.append(t)

  def count_words(self):
    for k, v in self.counter.unary.iteritems():
      word = k[1]
      self.wordcount[word] += v

      self.rarewords = {word for word, count in self.wordcount.iteritems()
                              if count < 5}

  def replace_infrequent(self):
    "Replace infrequent word in the trees and print the tree out"
    self.count_words()
    self.trees = [self.replace_infrequent_tree(tree) for tree in self.trees]

  def replace_infrequent_tree(self, tree):
    if isinstance(tree, basestring): return

    if len(tree) == 3:
      # It is a binary rule
      # Recursively replace the children.
      self.replace_infrequent_tree(tree[1])
      self.replace_infrequent_tree(tree[2])
    elif len(tree) == 2:
      # It is a unary rule.
      y1 = tree[1]
      if y1 in self.rarewords:
        tree[1] = '_RARE_'

    return tree

  def dump_trees(self, stream = sys.stdout):
    for t in self.trees:
      stream.write(json.dumps(t) + '\n')

    stream.write('\n')