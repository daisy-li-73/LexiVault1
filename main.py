from phonemizer import phonemize
import sys

def main():
    # Access command-line arguments
    args = sys.argv
    if len(args) != 3:
        print("Usage: main.py filename.txt language")
    else:
        filename = args[1]
        language = args[2]

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

    # Ask user to input list of digraphs for later processing of transcriptions 
        user_input = input("Enter a list of IPA digraphs in your target language, separated by spaces: ")
        digraphs = user_input.split()

    # Transcribe to words and lemmas IPA, delimit transcriptions, and write to output files
        transcripts = transcribe(lines, language)
        writeTrans(lines, transFile, delimFile, transcripts, digraphs, language)

     # Close input file
        file.close()

        # Close output files
        transFile.close()
        delimFile.close()

def transcribe(lines, language):
    # Set backend for phonemize
    backend='espeak'

    # Declare word list and lemma list
    words = []
    lemmas = []

    # Read file line by line
    for line in lines[1:]:
    # Parse word and lemma from line; add to word list and lemma list
        tokens = line.split("\t")
        if language == "en-us":
            words.append(tokens[0])
            lemmas.append(tokens[1])
        elif language == "ar":
            words.append(tokens[1])
            lemmas.append(tokens[3])

    # Create transcriptions for word list and lemma list 
    words_trans = phonemize(words, language, backend)
    lemmas_trans = phonemize(lemmas, language, backend)

    return [words_trans, lemmas_trans]

def writeTrans(lines, transFile, delimFile, transcripts, digraphs, language):
    words_trans = transcripts[0]
    lemmas_trans = transcripts[1]

    # Read file line by line
    for i in range(len(lines)):
    # Write word and lemma transcripts to new filew
        line = lines[i]
        tokens = line.split("\t")

        if language == "en-us":
            transFile.write(tokens[0]+"\t") # write word (or "word" header) to _trans file
            delimFile.write(tokens[0]+"\t") # write word (or "word" header) to _delim file
        elif language == "ar":
            transFile.write(tokens[0]+"\t"+tokens[1]+"\t") # write Buckwalter + Arabic to _trans file
            delimFile.write(tokens[0]+"\t"+tokens[1]+"\t") # write Buckwalter + Arabic to _delim file

        if (i == 0): # Write "transcription" header
            transFile.write("transcription\t")
            delimFile.write("transcription\t")
        else:
        # Write word's transcription in second column of _trans file 
            wordTrans = words_trans[i-1]
            transFile.write(wordTrans+"\t") 
        # Delimit and write word's transcription in second column of _delim file
            delimTrans = delimit(wordTrans, digraphs)
            delimFile.write(delimTrans+"\t")

        # Write "lemma" column to _trans and _delim file 
        if language == "en-us":
            transFile.write(tokens[1]+"\t") 
            delimFile.write(tokens[1]+"\t")
        elif language == "ar":
            transFile.write(tokens[2]+"\t"+tokens[3]+"\t") 
            delimFile.write(tokens[2]+"\t"+tokens[3]+"\t") 

        if (i == 0): # Write "lem_trans" header to _trans and _delim file
            transFile.write("lem_trans"+"\t")
            delimFile.write("lem_trans"+"\t")

        else:
        # Write lemma's transcription in fourth column of _trans file 
            lemTrans = lemmas_trans[i-1]
            transFile.write(lemTrans+"\t") 
        # Delimit and write lemma's transcription in fourth column of _delim file 
            delimTrans = delimit(lemTrans, digraphs)
            delimFile.write(delimTrans+"\t")

        # Write rest of columns to _trans and _delim file 
        for j in range(2, len(tokens)):
            transFile.write(tokens[j])
            delimFile.write(tokens[j])
            if j != len(tokens)-1:
                transFile .write("\t")
                delimFile.write("\t")

def delimit(input, digraphs):
    # Add '.' between every character, unless it is part of a digraph
    delimTrans = ""
    # Iterate through input by pairs of characters 
    for c in range(len(input)-1):
        curr = input[c]
        next = input[c+1]
        if c < len(input)-1 and curr+next in digraphs:
            delimTrans += curr
        else:
            delimTrans += curr + '.'            
    return delimTrans[:-1] # Remove trailing dot

main()