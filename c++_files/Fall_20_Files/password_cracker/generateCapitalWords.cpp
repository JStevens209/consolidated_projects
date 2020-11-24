// The idea of this code is that by counting to an abitrary number in binary,
// you go through every possible arrangement of 1s and 0s.
// Ex. when you count from 0 to 8 in binary you go 000 001 010 011 100 101 110 111
// that count goes through every possible arangement of 1s and 0s in a set of three
// without ever repeating a sequence.
// I used this idea to generate a list of words that have every possible combination
// of capital letters and lowercase letters by thinking of a capital as a 1 and a 
// lowercase letter as a 0. I avoided repeats by calculating how many bits was being used 
// by the the binaryCode, then only go over a word that has a length >= the number of bits.

#include <bitset>
#include <fstream>
#include <iostream>
#include <cmath>
#include <string>

using namespace std;


int main() {
    // longest word is 21 characters, so the bit limit must be 2^21
    // therefore the binary number needs to be 21 bits
    const int BIT_LIMIT = pow( 2, 21 );

    string filepath = "./wordlists/unique_wordlist.txt";
    string word;

    ifstream fin( filepath );
    fstream fout( "./wordlists/output.txt"  );

    int decimalCode = 1;

    // Holds the binary representation of the decimal number
    bitset<21> binaryCode = decimalCode;
    
    // Iterates through every binary number up to the bit limit
    while( decimalCode <= BIT_LIMIT ) {

        // Iterates through the file
        while( !fin.eof() ) {

            getline( fin, word );

            // Stores the length so it does not have to be calulated twice, saves time
            double wordLength = word.length();   

            // IF the minimum number of bits used to represent decimal Code
            // is LESS THAN OR EQUAL TO the wordLength
            if( ( int( log2( decimalCode )) + 1 ) <= wordLength ) {
                
                // For every 1 bit in binaryCode, capitalize the corresponding letter in the word
                for( int i = 0; i < wordLength ; i++ ) {
                    if( binaryCode[i] == 1 ) {
                        word[i] = toupper( word[i] );
                    }
                }
                fout << word << endl;
            }
        }

        decimalCode++;
        binaryCode = decimalCode;

        // closes the files to 
        // 1. Resets fin to beginning of file
        // 2. Saves fout to disk and stops it being stored in RAM, had a problem with running outta space
        // might save a small amount of time to remove fout.close(), but with larger lists the RAM usage WILL get large.
        fin.close();
        fout.close();
        
        fout.open( "./output.txt", ios::app );
        fin.open( filepath );
    }

    fin.close();
    fout.close();
}


