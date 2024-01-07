from phonemizer import phonemize
import sys

def main():
    # Access command-line arguments
    args = sys.argv
    if len(args) != 2:
        print("Usage: bengali_espeak.py filename.txt")
    else:
        filename = args[1]

    # Open input file
        file = open(filename, "r")
    # Read file lines into a list
        lines = file.readlines()

    # Create output file names 
        parts = filename.split('.')
        transFilename = ""
        if len(parts) > 1 and parts[-1] == 'txt':
            # Create new file with word transcriptions
            transFilename = parts[0] + '_trans.' + parts[-1]
            transFile = open(transFilename, "w")

            # Create new file with delimited word transcriptions 
            delimFilename = parts[0]+"_delim." + parts[-1]
            delimFile = open(delimFilename, "w")

    # Transcribe words and lemmas to IPA, delimit transcriptions, and write to output files
        transcripts = transcribe(lines)
        writeTrans(transFile, delimFile, transcripts)

     # Close input file
        file.close()

        # Close output files
        transFile.close()
        delimFile.close()

def transcribe(lines):
    # Set backend for phonemize
    backend='espeak'

    # Declare word list
    words = []

    # Read first line
    line = lines[0]
    # Parse word and lemma from line; add to word list
    tokens = line.split("\t")
    for word in tokens:
        words.append(word)

    # Create transcriptions for word list
    words_trans = phonemize(words, 'bn', backend)

    return words_trans

def writeTrans(transFile, delimFile, transcripts):
    # Write (delimited) transcriptions to output file
    for word in transcripts:
        transFile.write(word+"\t")
        delimTrans = delimit(word)
        delimFile.write(delimTrans+"\t")

def delimit(input):
    # Add '.' between every character, unless it is part of a digraph
    delimTrans = ""
    # Iterate through input by pairs of characters 
    for c in range(len(input)-1):
        curr = input[c]
        delimTrans += curr + '.'            
    return delimTrans[:-1] # Remove trailing dot

main()