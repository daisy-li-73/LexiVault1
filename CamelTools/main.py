# Author: Daisy Li
# Date: Aug 7 2024
# Purpose: Use CamelTools to generate a corpus from a text file of Arabic script

from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.charmap import CharMapper
from camel_tools.disambig.mle import MLEDisambiguator

# Initialize the components
ar2bw = CharMapper.builtin_mapper('ar2bw')
db = MorphologyDB.builtin_db()
analyzer = Analyzer(db)
mle = MLEDisambiguator.pretrained()

# Function to process a single word
def process_word(word):
    # Normalize the word
    word_norm = normalize_unicode(word)
    
    # Analyze the word
    analyses = analyzer.analyze(word_norm)
    
    # Disambiguate the analyses
    disambig = mle.disambiguate([word_norm])
    
    if len(analyses) == 0:
        return None

    # Select the best analysis
    best_analysis = disambig[0].analyses[0]

    # Extract the required information
    lemma = best_analysis.analysis['lex']
    root = best_analysis.analysis['root']
    stem = best_analysis.analysis['stem']
    gloss = best_analysis.analysis['gloss']
    pos = best_analysis.analysis['pos']

    # Transliterate the original word, lemma, root, and stem
    word_translit = ar2bw(word_norm)
    lemma_translit = ar2bw(lemma)
    root_translit = ar2bw(root)
    stem_translit = ar2bw(stem)

    return {
        'word': word,
        'word_translit': word_translit,
        'lemma': lemma,
        'lemma_translit': lemma_translit,
        'root': root,
        'root_translit': root_translit,
        'stem': stem,
        'stem_translit': stem_translit,
        'gloss': gloss,
        'pos': pos
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
    # Specify the path to your input file
    file_path = 'input/lorem-ipsum.txt'
    output_path = 'output/lorem-ipsum.out'

    # Read the text from the file
    corpus = read_file(file_path)

    # Process the corpus
    results = process_corpus(corpus)

		# Write the results to an output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("word_bw\tword_ar\tlemma_bw\tlemma_ar\tpos\tstem_bw\tstem_ar\tgloss\troot_bw\troot_ar\n")
        for result in results:
						# ignore punctuation
            if result['pos'] == 'punc':
                continue
            file.write(f"{result['word_translit']}\t")
            file.write(f"{result['word']}\t")
            file.write(f"{result['lemma_translit']}\t")
            file.write(f"{result['lemma']}\t")
            file.write(f"{result['pos']}\t")
            file.write(f"{result['stem_translit']}\t")
            file.write(f"{result['stem']}\t")
            file.write(f"{result['gloss']}\t")
            file.write(f"{result['root_translit']}\t")
            file.write(f"{result['root']}\n")                         
                                    
if __name__ == "__main__":
    main()