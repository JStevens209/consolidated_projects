// Have one of these files in almost every directory.
// Its a place where I throw snippets of code to quickly test logic/concepts.

#include <iostream>
#include <fstream>

using namespace std;

int main() { 

    string test;
    cin >> test;

    string input;

    ifstream fin;
    fin.open( "./Bible.txt" );

    while( !fin.eof() ) {
        getline( fin, input );

        if( input.substr( 0, test.size() ) == test ){
            cout << "Found" << endl;
        }
    }
    

    cout << input << endl;
    cout << test.length() << endl;
    cout << input.substr( 0, test.size() ) << endl;
}