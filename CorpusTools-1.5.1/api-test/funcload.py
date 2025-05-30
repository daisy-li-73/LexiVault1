"""
Parameters (hard coding, for now):
	corpus filename
	output filename
"""
from corpustools.contextmanagers import (CanonicalVariantContext,
                                        MostFrequentVariantContext,
                                        SeparatedTokensVariantContext,
                                        WeightedVariantContext)
from corpustools.corpus.io.binary import save_binary
from corpustools.funcload.functional_load import minpair_fl_speed

# Loading a corpus from a text file
from corpustools.corpus.io import (load_corpus_csv, load_feature_matrix_csv)
################## PREPROCESS CORPUS ################
import csv

# Set your file paths
input_csv = 'inputs/sample_ar.csv'
output_csv = 'inputs/sample_ar_clean.csv'

# Set the transcription column you want to keep
main_trans_col = 'Transcription'  # <-- change this if needed (case-sensitive match)

with open(input_csv, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    original_headers = reader.fieldnames

    # Identify which columns to keep
    headers_to_keep = ["Word", main_trans_col]

    with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers_to_keep)
        writer.writeheader()

        for row in reader:
            # Write only the desired columns
            clean_row = {k: v for k, v in row.items() if k in headers_to_keep}
            writer.writerow(clean_row)

corpus_txt_path = output_csv
feature_matrix_txt_path = 'inputs/example_feature_matrix.csv'
feature_matrix_path = 'inputs/example_feature_matrix.feature'
        
feature_matrix = load_feature_matrix_csv('example_feature', feature_matrix_txt_path, ',')
save_binary(feature_matrix, feature_matrix_path)

corpus = load_corpus_csv('example_corpus', corpus_txt_path,',', None, feature_matrix_path)

# Context manager? TODO: try out other types of context managers (e.g. MostFrequentVariantContext)
canonical_variant = CanonicalVariantContext(corpus, main_trans_col, 'type')
most_freq_variant = MostFrequentVariantContext(corpus, main_trans_col, 'type')
separated_tokens_variant = SeparatedTokensVariantContext(corpus, 'Transcription', 'type')
 
################## FUNCTIONAL LOAD ##################
def func_load():
	funcload_out = "outputs/funcload_ar_out.txt"

	with open(funcload_out, "w", encoding="utf-8") as file:
		file.write("CANONICAL VARIANT\n")
		for segment in corpus.inventory.segs:
			file.write("\n")
			segment_pairs = [segment]
			minpair_output_c = minpair_fl_speed(canonical_variant, segment_pairs) 
			# fl_output_s = minpair_fl_speed(separated_tokens_variant, segment_pairs)
			target_segment = minpair_output_c[0][0]
			file.write("target segment = " + target_segment + "\n")
			fl_results = minpair_output_c[0][1]
			file.write("fl_results = " + str(fl_results) + "\n")
			minpairs = minpair_output_c[0][2]
			for seg_pair, word_set in minpairs.items():
				if word_set:  # non-empty set
						file.write(f"{seg_pair}:\n")
						for pair in word_set:
								file.write(f"  {pair}\n")

		file.write("\nMOST FREQUENT VARIANT\n")
		for segment in corpus.inventory.segs:
			file.write("\n")
			segment_pairs = [segment]
			minpair_output_m = minpair_fl_speed(most_freq_variant, segment_pairs)
			target_segment = minpair_output_m[0][0]
			file.write("target segment = " + target_segment + "\n")
			fl_results = minpair_output_m[0][1]
			file.write("fl_results = " + str(fl_results) + "\n")
			minpairs = minpair_output_m[0][2]
			for seg_pair, word_set in minpairs.items():
				if word_set:  # non-empty set
						file.write(f"{seg_pair}:\n")
						for pair in word_set:
								file.write(f"  {pair}\n")

if __name__ == "__main__":
	func_load()

