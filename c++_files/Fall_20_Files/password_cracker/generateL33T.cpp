#include <bitset>
#include <iostream>
#include <fstream>
#include <cmath>
#include <string>

using namespace std;

int main() {

    const int ARRAY_SIZE = 12;
    const int BIT_LIMIT = pow( 2, ARRAY_SIZE );

    char decimalReplacement[ ARRAY_SIZE ] = { '4','8','3','6','1','1','0','5','7','@','$','!' };
    char alphabetCore[ ARRAY_SIZE ] = { 'A','B','E','G','I','L','O','S','T','A','S','I' };

    //{ '@','$','!' };//
    //{ 'A','S','I' };//

    string inputFilePath = "./wordlists/unique_wordlist.txt";
    string outputFilePath = "./wordlists/output2.txt" ;

    ofstream fout( outputFilePath );
    ifstream fin( inputFilePath );

    int decimalCode = 1;
    bitset<ARRAY_SIZE> binaryCode = decimalCode;

    string word;

    // Iterates through every binary number up to the bit limit
    while( decimalCode <= BIT_LIMIT ) {

        // Iterates through the file
        while( !fin.eof() ) {

            getline( fin, word );

            // Stores the length so it does not have to be calulated twice, saves time
            double wordLength = word.length();   

            for( int i = 0; i < ARRAY_SIZE ; i++ ) {
                if( binaryCode.test(i) == 1 ) {

                    for( int j = 0; j < wordLength; j++ ) {
                        if( toupper( word[j] ) == alphabetCore[i] ) {
                            word[j] = decimalReplacement[i];
                        }
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
        
        fout.open( outputFilePath, ios::app );
        fin.open( inputFilePath );
    }

    fin.close();
    fout.close();

    return 0;
}