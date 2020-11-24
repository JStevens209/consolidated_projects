#include <iostream>
#include <fstream>

using namespace std;

int main() {

    string inputFilepath = "./wordlists/unique_wordlist.txt";
    string outputFilepath = "./wordlists/output2.txt";

    ifstream fin( inputFilepath );
    ofstream fout( outputFilepath );

    bool append = false;

    for( int i = 0; i < 9999; i++ ) {
        string word;

        while( !fin.eof() && append ) {
            getline( fin, word );
            word = word + to_string( i );

            fout << word << endl;
        }

        while( !fin.eof() && !append ) {
            getline( fin, word );
            word = to_string( i ) + word;

            fout << word << endl;
        }

        fin.close();
        fin.open( inputFilepath );

        fout.close();
        fout.open( outputFilepath, ios::app );
    }

    fin.close();
    fout.close();
    
    return 0;
}