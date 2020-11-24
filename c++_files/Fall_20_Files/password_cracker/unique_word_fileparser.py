import sys
import string

input_file = sys.argv[1]
output_file = "./wordlists/unique_wordlist.txt"

with open( input_file, 'r+' ) as fin, open( output_file, 'a' ) as fout:

    if fin.readable():
        # Get the input as a string
        input = fin.read()

        # Convert everything to lowercase
        input = input.lower()

        # Remove all punctuation from the string
        input = input.translate( str.maketrans( '', '', string.punctuation[:12] + string.punctuation[13:] ))

        # Cast string to a "set" which only holds unique members to get rid of copies of words
        # Then sort the set by length
        input = sorted( set( input.split() ), key= len )

        # Write the sorted set to the output file
        for word in input:
            if not word.isnumeric():
                fout.write( word + '\n' )

