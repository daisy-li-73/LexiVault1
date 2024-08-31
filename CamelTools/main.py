# Author: Daisy Li
# Date: Aug 7 2024
# Purpose: Use CamelTools to generate a corpus from a text file of Arabic script

from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.charmap import CharMapper
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.disambig.bert import BERTUnfactoredDisambiguator
import sys

# Initialize the components
ar2bw = CharMapper.builtin_mapper('ar2bw')
db = MorphologyDB.builtin_db('calima-egy-r13')
analyzer = Analyzer(db)
mle = MLEDisambiguator.pretrained(model_name='calima-egy-r13', analyzer=analyzer)
bert = BERTUnfactoredDisambiguator.pretrained(model_name='egy')

# Function to process a single word
def process_word(word):
    # Normalize the word
    word_norm = normalize_unicode(word)
    
    # Analyze the word
    analyses = analyzer.analyze(word_norm)
    
    # Disambiguate the analyses
    mle_disambig = mle.disambiguate([word_norm])
    bert_disambig = bert.disambiguate([word_norm])
    
    if len(analyses) == 0:
        return None

    # Select the best analysis
    mle_best_analysis = mle_disambig[0].analyses[0]
    bert_best_analysis = bert_disambig[0].analyses[0]

    # Extract the required information
    if 'lex' not in mle_best_analysis.analysis:
        mle_lemma = 'None'
    if 'lex' not in bert_best_analysis.analysis:
        bert_lemma = 'None'
    else : 
        mle_lemma = mle_best_analysis.analysis['lex']
        bert_lemma = bert_best_analysis.analysis['lex']

    if 'root' not in mle_best_analysis.analysis:
        mle_root = 'None'
    if 'root' not in bert_best_analysis.analysis:
        bert_root = 'None'
    else:
        mle_root = mle_best_analysis.analysis['root']
        bert_root = bert_best_analysis.analysis['root']

    if 'stem' not in mle_best_analysis.analysis:
        mle_stem = 'None'
    if 'stem' not in bert_best_analysis.analysis:
        bert_stem = 'None'
    else:
        mle_stem = mle_best_analysis.analysis['stem']
        bert_stem = bert_best_analysis.analysis['stem']

    if 'gloss' not in mle_best_analysis.analysis:
        mle_gloss = 'None'
    if 'gloss' not in bert_best_analysis.analysis:
        bert_gloss = 'None'
    else:
        mle_gloss = mle_best_analysis.analysis['gloss']
        bert_gloss = bert_best_analysis.analysis['gloss']

    if 'pos' not in mle_best_analysis.analysis:
        mle_pos = 'None'
    if 'pos' not in bert_best_analysis.analysis:
        bert_pos = 'None'
    else:
        mle_pos = mle_best_analysis.analysis['pos']
        bert_pos = bert_best_analysis.analysis['pos']

    # Transliterate the original word, lemma, root, and stem
    word_translit = ar2bw(word_norm)
    mle_lemma_translit = ar2bw(mle_lemma)
    bert_lemma_translit = ar2bw(bert_lemma)
    mle_root_translit = ar2bw(mle_root)
    bert_root_translit = ar2bw(bert_root)
    mle_stem_translit = ar2bw(mle_stem)
    bert_stem_translit = ar2bw(bert_stem)

    return {
        'word': word,
        'word_translit': word_translit,
        'mle_lemma': mle_lemma,
        'mle_lemma_translit': mle_lemma_translit,
        'mle_root': mle_root,
        'mle_root_translit': mle_root_translit,
        'mle_stem': mle_stem,
        'mle_stem_translit': mle_stem_translit,
        'mle_gloss': mle_gloss,
        'mle_pos': mle_pos,
        'bert_lemma': bert_lemma,
        'bert_lemma_translit': bert_lemma_translit,
        'bert_root': bert_root,
        'bert_root_translit': bert_root_translit,
        'bert_stem': bert_stem,
        'bert_stem_translit': bert_stem_translit,
        'bert_gloss': bert_gloss,
        'bert_pos': bert_pos
    }

# Function to process a corpus of text
def process_corpus(text):
    results = []
    words = simple_word_tokenize(text)
    
    for word in words:
        processed_word = process_word(word)
        if processed_word is not None:
            results.append(processed_word)
    
    return results

# Function to read text from a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Main function
def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python main.py <input_file>")
        sys.exit(1)
    file_path = args[0]
    mle_output_path = 'output/' + 'mle-' + file_path[6:]
    bert_output_path = 'output/' +  'bert-' + file_path[6:]

    # Read the text from the file
    corpus = read_file(file_path)

    # Process the corpus
    results = process_corpus(corpus)

		# Write the results to respective output files
    with open(mle_output_path, 'w', encoding='utf-8') as mle_file, \
         open(bert_output_path, 'w', encoding='utf-8') as bert_file:
        mle_file.write("word_bw\tword_ar\tlemma_bw\tlemma_ar\tpos\tstem_bw\tstem_ar\tgloss\troot_bw\troot_ar\n")
        bert_file.write("word_bw\tword_ar\tlemma_bw\tlemma_ar\tpos\tstem_bw\tstem_ar\tgloss\troot_bw\troot_ar\n")
        for result in results:
			# ignore punctuation
            if result['mle_pos'] != 'punc':
                mle_file.write(f"{result['word_translit']}\t")
                mle_file.write(f"{result['word']}\t")
                mle_file.write(f"{result['mle_lemma_translit']}\t")
                mle_file.write(f"{result['mle_lemma']}\t")
                mle_file.write(f"{result['mle_pos']}\t")
                mle_file.write(f"{result['mle_stem_translit']}\t")
                mle_file.write(f"{result['mle_stem']}\t")
                mle_file.write(f"{result['mle_gloss']}\t")
                mle_file.write(f"{result['mle_root_translit']}\t")
                mle_file.write(f"{result['mle_root']}\n")      

            if result['bert_pos'] != 'punc':
                bert_file.write(f"{result['word_translit']}\t")
                bert_file.write(f"{result['word']}\t")
                bert_file.write(f"{result['bert_lemma_translit']}\t")
                bert_file.write(f"{result['bert_lemma']}\t")
                bert_file.write(f"{result['bert_pos']}\t")
                bert_file.write(f"{result['bert_stem_translit']}\t")
                bert_file.write(f"{result['bert_stem']}\t")
                bert_file.write(f"{result['bert_gloss']}\t")
                bert_file.write(f"{result['bert_root_translit']}\t")
                bert_file.write(f"{result['bert_root']}\n")                   
                                    
if __name__ == "__main__":
    main()