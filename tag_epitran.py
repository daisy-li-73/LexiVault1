import epitran
import sys

# Access command-line arguments
args = sys.argv
filename = args[1]

# Create output file with word transcriptions
parts = filename.split(".")
# Check there is at least one period in the filename
if len(parts) > 1:
# Add "_trans" before the last period
    # parts[-2] += "_red_trans"
    parts[-2] += "_trans"
# Join parts back together 
newFilename = ".".join(parts)
newFile = open(newFilename, "w")

# Determine language
language = "tgl-Latn"
# language = "tgl-Latn-red"

epi = epitran.Epitran(language)

# Read file line by line
with open(filename, "r") as file:
    lines = file.readlines()

# Transliterate words and write them to output file 
for line in lines:
    tokens = line.split(" ")
    newFile.write(tokens[0]+' ') # write original word to file 
    newFile.write(epi.transliterate(tokens[0]+'\n')) # write transliterated word to file 

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