## NOTE: resulting transliteration not as good as phonemizer... contains some extraneous symbols; also doc mention Arabic should be approahced with caution
import epitran
import sys

# Access command-line arguments
args = sys.argv
filename = args[1]

# Create output file with word transcriptions
newFilename = filename+".epi"
newFile = open(newFilename, "w")

# Determine language
if "eng" in filename:
    language = "eng-Latn" 
elif "arabic" in filename:
    language = "ara-Arab"

epi = epitran.Epitran(language)

# Read file line by line
with open(filename, "r") as file:
    lines = file.readlines()

# Transliterate words and lemmas and write them to output file 
    for line in lines[1:]:
        tokens = line.split("\t")
        if language == "ara-Arab":
            newFile.write(epi.transliterate(tokens[1])+'\t') # write transliterated word
            newFile.write(epi.transliterate(tokens[3])+'\n') # write transliterated lemma
        elif language == "eng-Latn":
            newFile.write(epi.transliterate(tokens[0])+'\t') # write transliterated word
            newFile.write(epi.transliterate(tokens[1])+'\n') # write transliterated lemma


# # TODO: Add word transcriptions to input file
#     for i in range(len(lines)):
#         line = lines[i]
#         tokens = line.split("\t")
#         newFile.write(tokens[0]+"\t") # write word to new file
#         if (i == 0): # Write headers
#             newFile.write("transcription\t")
#         else:
#         # Write word's transcription in second column
#             newFile.write(words_trans[i-1]+"\t") 
#         # Write rest of columns to file 
#         for j in range(1, len(tokens)):
#             newFile.write(tokens[j])
#             if j != len(tokens)-1:
#                 newFile.write("\t")