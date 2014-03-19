import sys, json, operator
import count_cfg_freq
from collections import defaultdict

class CKYDecoder:
  def __init__(self, fn):
    "Read in the frequency file"
    self.nonterm = defaultdict(int)
    self.binary = defaultdict(int)
    self.unary = defaultdict(int)
    self.term = set()

    with open(fn) as f:
      for line in f.readlines():
        line = line.split()
        freq = int(line[0])
        token = line[1]
        key = tuple(line[2:])
        if token == 'NONTERMINAL':
          self.nonterm[key[0]] += freq
        elif token == 'BINARYRULE':
          self.binary[key] += freq
        elif token == 'UNARYRULE':
          self.unary[key] += freq
          self.term.add(key[1])
        else:
          raise Exception('Unknown token', token)

  def binary_prob(self, x, y1, y2):
    """
    Gives q(x->y1 y2) = count(x->y1 y2) / count(x)
    """

    return 1.0 * self.binary[x, y1, y2] / self.nonterm[x]

  def unary_prob(self, x, w):
    """
    Gives q(x->w) = count(x->w) / count(x)
    """
    return 1.0 * self.unary[x, w] / self.nonterm[x]

  def replace_word(self, word):
    return word if word in self.term else '_RARE_'

  def parse_file(self, fn):
    with open(fn) as f:
      for sentence in f.readlines():
        parsed = self.parse_sentence(sentence)
        print json.dumps(parsed)

  def parse_sentence(self, sentence):
    """
    Parse the given sentence using CKY algorithm.
    Returns a parsed tree in JSON format
    Note: replace the unseen words with _RARE_
    """

    def q(x, y, z): return self.binary_prob(x, y, z)

    words = sentence.split()
    pi = defaultdict(float)
    bp = {}

    # initialize pi
    n = len(words)
    for i in range(n):
      for x in self.nonterm.keys():
        word = self.replace_word(words[i])
        pi[i, i, x] = self.unary_prob(x, word)


    # DP part
    for l in range(1, n):
      for i in range(n - l):
        j = i + l
        for X in self.nonterm.keys():
          probs = (((y, z, s),                             # x-> y z, pivot s
                    q(x, y, z) * pi[i, s, y] * pi[s + 1, j, z] # probability
                   ) for x, y, z in self.binary.keys() if x == X
                     for s in range(i, j)
                  )
          try:
            # the list might be empty
            best = argmax_pair(probs)
          except ValueError:
            continue

          pi[i, j, X] = best[1]
          bp[i, j, X] = best[0]

    # backtrack using bp in range [i, j] with symbol 'sym',
    # returns a tree in JSON
    def backtrack(i, j, sym):
      if i == j:
        return [sym, words[i]]

      y, z, s = bp[i, j, sym]
      return [sym, backtrack(i, s, y), backtrack(s + 1, j, z)]

    return backtrack(0, n - 1, 'SBARQ')

class RareWordReplacer:
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

# given an iterable of pairs return the key corresponding to the greatest value
def argmax(pairs):
  return argmax_pair(pairs)[0]

def argmax_pair(pairs):
  return max(pairs, key = operator.itemgetter(1))

def dump_trees(trees, stream = sys.stdout):
  for t in trees:
    stream.write(json.dumps(t) + '\n')
