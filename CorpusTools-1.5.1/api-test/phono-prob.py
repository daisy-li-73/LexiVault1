from corpustools.phonoprob.phonotactic_probability import phonotactic_probability_vitevitch
from corpustools.contextmanagers import (CanonicalVariantContext,
                                        MostFrequentVariantContext,
                                        SeparatedTokensVariantContext,
                                        WeightedVariantContext)
from corpustools.corpus.io.binary import save_binary

# Loading a corpus from a text file
from corpustools.corpus.io import (load_corpus_csv, load_feature_matrix_csv)

corpus_txt_path = 'api-test/example_corpus.csv'
feature_matrix_txt_path = 'api-test/example_feature_matrix.csv'
feature_matrix_path = 'api-test/example_feature_matrix.feature'

feature_matrix = load_feature_matrix_csv('example_feature', feature_matrix_txt_path, ',')
save_binary(feature_matrix, feature_matrix_path)

corpus = load_corpus_csv('example_corpus', corpus_txt_path,'\t', None, feature_matrix_path)

# Context manager? TODO: try out other types of context managers (e.g. MostFrequentVariantContext)
canonical_variant = CanonicalVariantContext(corpus, 'transcription', 'type')
most_freq_variant = MostFrequentVariantContext(corpus, 'transcription', 'type')
separated_tokens_variant = SeparatedTokensVariantContext(corpus, 'transcription', 'type')

################## PHONOPROB ##################
# Get spellings from corpus and write to output file
wordlist = corpus.wordlist
phon_prob_out = "api-test/phon_prob_out.txt"
with open(phon_prob_out, "w", encoding="utf-8") as file:

  file.write("Canonical variant\n")
  for w in wordlist.values():
    spelling = w.spelling
    phon_prob = phonotactic_probability_vitevitch(canonical_variant, corpus.find(spelling), 'bigram')
    line = "phon_prob of " + spelling + " = " + str(phon_prob) + "\n"
    file.write(line)

  file.write("\nMost frequent variant\n")
  for w in wordlist.values():
    spelling = w.spelling
    phon_prob = phonotactic_probability_vitevitch(most_freq_variant, corpus.find(spelling), 'bigram')
    line = "phon_prob of " + spelling + " = " + str(phon_prob) + "\n"
    file.write(line)
    
  # file.write("Separated tokens variant\n")
  # for w in wordlist.values():
  #   spelling = w.spelling
  #   phon_prob = phonotactic_probability_vitevitch(separated_tokens_variant, corpus.find(spelling), 'bigram')
