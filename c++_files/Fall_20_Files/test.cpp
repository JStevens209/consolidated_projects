#include <iostream>
#include <string>
#include <sstream>
#include <bitset>
#include <string.h>

using namespace std;

int main()
{
    char input[100];
    string output;

    memset( input, '0', 100 );

    cin >> input;

    string newInput = input;

    for ( int i = 0; i < newInput.length(); i++ ) {

        output += bitset<8>( newInput[i] ).to_string();

    }

    cout << output << endl;

    return 0;
}