import epitran
import sys

# Access command-line arguments
args = sys.argv
filename = args[1]

newFile = open("bangla_sample_epitran.txt", "w")

# Determine language
language = "ben-Beng"

epi = epitran.Epitran(language)

# Read first line
with open(filename, "r") as file:
    lines = file.readlines()
    line = lines[0]

# Transliterate words and write them to output file 
    words = line.split(" ")
    for word in words:
        trans = epi.transliterate(word)
        newFile.write(trans+"\t")
