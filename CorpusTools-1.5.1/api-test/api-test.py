import sys
import os

from corpustools.phonoprob.phonotactic_probability import phonotactic_probability_vitevitch
from corpustools.contextmanagers import CanonicalVariantContext, MostFrequentVariantContext, WeightedVariantContext
from corpustools.corpus.io.binary import load_binary, save_binary

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

# Get spellings from corpus
wordlist = corpus.wordlist
for w in wordlist.values():
  spelling = w.spelling
  phon_prob = phonotactic_probability_vitevitch(c, corpus.find(spelling), 'bigram')
  print("phon_prob of ", spelling, " = ", phon_prob)
# print(list(map(str,corpus.attributes)))