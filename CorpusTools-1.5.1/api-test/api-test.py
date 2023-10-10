import sys
import os

from corpustools.phonoprob.phonotactic_probability import phonotactic_probability_vitevitch
from corpustools.contextmanagers import CanonicalVariantContext, MostFrequentVariantContext, WeightedVariantContext
from corpustools.corpus.io.binary import load_binary, save_binary
from corpustools.transprob.transitional_probability import calc_trans_prob

# Loading a corpus from a text file
from corpustools.corpus.io import (load_corpus_csv, load_feature_matrix_csv)

corpus_txt_path = 'api-test/example_corpus.csv'
features_matrix_txt_path = 'api-test/example_feature_matrix.csv'
features_matrix_path = 'api-test/example_feature_matrix.features'

features_matrix = load_feature_matrix_csv('example_features', features_matrix_txt_path, ',')
save_binary(features_matrix, features_matrix_path)

corpus = load_corpus_csv('example_corpus', corpus_txt_path,'\t', None, features_matrix_path)

# Context manager?
c = CanonicalVariantContext(corpus, 'transcription', 'token')

# Get spellings from corpus and write to output file
wordlist = corpus.wordlist
phon_prob_out = "api-test/phon_prob_out.txt"
with open(phon_prob_out, "w", encoding="utf-8") as file:
  for w in wordlist.values():
    spelling = w.spelling
    phon_prob = phonotactic_probability_vitevitch(c, corpus.find(spelling), 'bigram')
    line = "phon_prob of " + spelling + " = " + str(phon_prob) + "\n"
    file.write(line)

# Transitional Probability
bigram = ('t', 'ɑ')
word_boundaries = 'Ignored'
direction = 'forward'

trans_prob_out = "api-test/trans_prob_out.txt"
with open(trans_prob_out, "w", encoding="utf-8") as file:
  res = calc_trans_prob(c, bigram, word_boundaries, direction)
  line = "trans prob of " + str(bigram) + " = " + str(res) + "\n"
  file.write(line)

# print(list(map(str,corpus.attributes)))