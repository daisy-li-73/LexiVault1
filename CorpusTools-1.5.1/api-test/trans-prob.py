from corpustools.contextmanagers import (CanonicalVariantContext,
                                        MostFrequentVariantContext,
                                        SeparatedTokensVariantContext,
                                        WeightedVariantContext)
from corpustools.corpus.io.binary import save_binary
from corpustools.transprob.transitional_probability import calc_trans_prob

# Loading a corpus from a text file
from corpustools.corpus.io import (load_corpus_csv, load_feature_matrix_csv)

corpus_txt_path = 'api-test/example_corpus.csv'
feature_matrix_txt_path = 'api-test/example_feature_matrix.csv'
feature_matrix_path = 'api-test/example_feature_matrix.feature'

feature_matrix = load_feature_matrix_csv('example_feature', feature_matrix_txt_path, ',')
save_binary(feature_matrix, feature_matrix_path)

corpus = load_corpus_csv('example_corpus', corpus_txt_path,'\t', None, feature_matrix_path)

# Context manager?
canonical_variant = CanonicalVariantContext(corpus, 'transcription', 'type')
most_freq_variant = MostFrequentVariantContext(corpus, 'transcription', 'type')
separated_tokens_variant = SeparatedTokensVariantContext(corpus, 'transcription', 'type')

# ################## TRANSITIONAL PROBABILITY ##################
bigrams = [('t', 'ɑ'), ('o', 'm'), ('s', 'ɑ'), ('s', 'i')]

trans_prob_out = "api-test/trans_prob_out.txt"
with open(trans_prob_out, "w", encoding="utf-8") as file:

  file.write("\nCanonical variant\n")
  for b in bigrams:
    res_ignored_forward = calc_trans_prob(canonical_variant, b, 'Ignored', 'forward')
    line = "forward ignored trans prob of " + str(b) + " = " + str(res_ignored_forward) + "\n"
    file.write(line)
    res_ignored_backward = calc_trans_prob(canonical_variant, b, 'Ignored', 'backward')
    line = "backward ignored trans prob of " + str(b) + " = " + str(res_ignored_backward) + "\n"
    file.write(line)
    res_halved_forward = calc_trans_prob(canonical_variant, b, 'Halved', 'forward')
    line = "forward halved trans prob of " + str(b) + " = " + str(res_halved_forward) + "\n"
    file.write(line)
    res_halved_backward = calc_trans_prob(canonical_variant, b, 'Halved', 'backward')
    line = "backward halved trans prob of " + str(b) + " = " + str(res_halved_backward) + "\n"
    file.write(line)
    res_both_forward = calc_trans_prob(canonical_variant, b, 'Both sides', 'forward')
    line = "forward both sides trans prob of " + str(b) + " = " + str(res_both_forward) + "\n"
    file.write(line)
    res_both_backward = calc_trans_prob(canonical_variant, b, 'Both sides', 'backward')
    line = "backward both sides trans prob of " + str(b) + " = " + str(res_both_backward) + "\n"
    file.write(line)

  file.write("\nMost frequent variant\n")
  for b in bigrams:
    res_ignored_forward = calc_trans_prob(most_freq_variant, b, 'Ignored', 'forward')
    line = "forward ignored trans prob of " + str(b) + " = " + str(res_ignored_forward) + "\n"
    file.write(line)
    res_ignored_backward = calc_trans_prob(most_freq_variant, b, 'Ignored', 'backward')
    line = "backward ignored trans prob of " + str(b) + " = " + str(res_ignored_backward) + "\n"
    file.write(line)
    res_halved_forward = calc_trans_prob(most_freq_variant, b, 'Halved', 'forward')
    line = "forward halved trans prob of " + str(b) + " = " + str(res_halved_forward) + "\n"
    file.write(line)
    res_halved_backward = calc_trans_prob(most_freq_variant, b, 'Halved', 'backward')
    line = "backward halved trans prob of " + str(b) + " = " + str(res_halved_backward) + "\n"
    file.write(line)
    res_both_forward = calc_trans_prob(most_freq_variant, b, 'Both sides', 'forward')
    line = "forward both sides trans prob of " + str(b) + " = " + str(res_both_forward) + "\n"
    file.write(line)
    res_both_backward = calc_trans_prob(most_freq_variant, b, 'Both sides', 'backward')
    line = "backward both sides trans prob of " + str(b) + " = " + str(res_both_backward) + "\n"
    file.write(line)

  # file.write("\nSeparated tokens variant\n")
  # for b in bigrams:
  #   res_ignored_forward = calc_trans_prob(separated_tokens_variant, b, 'Ignored', 'forward')
  #   line = "forward ignored trans prob of " + str(b) + " = " + str(res_ignored_forward) + "\n"
  #   file.write(line)
  #   res_ignored_backward = calc_trans_prob(separated_tokens_variant, b, 'Ignored', 'backward')
  #   line = "backward ignored trans prob of " + str(b) + " = " + str(res_ignored_backward) + "\n"
  #   file.write(line)
  #   res_halved_forward = calc_trans_prob(separated_tokens_variant, b, 'Halved', 'forward')
  #   line = "forward halved trans prob of " + str(b) + " = " + str(res_halved_forward) + "\n"
  #   file.write(line)
  #   res_halved_backward = calc_trans_prob(separated_tokens_variant, b, 'Halved', 'backward')
  #   line = "backward halved trans prob of " + str(b) + " = " + str(res_halved_backward) + "\n"
  #   file.write(line)
  #   res_both_forward = calc_trans_prob(separated_tokens_variant, b, 'Both sides', 'forward')
  #   line = "forward both sides trans prob of " + str(b) + " = " + str(res_both_forward) + "\n"
  #   file.write(line)
  #   res_both_backward = calc_trans_prob(separated_tokens_variant, b, 'Both sides', 'backward')
  #   line = "backward both sides trans prob of " + str(b) + " = " + str(res_both_backward) + "\n"
  #   file.write(line)