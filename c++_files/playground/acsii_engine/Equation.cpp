#include "Equation.h"
#include <sstream>

Equation::Equation( std::string equation ) {
    
    try {
        parseEquation( equation );
    }
    catch InputException(e) {
        // TODO: Add error handling
    }
}   

void Equation::parseEquation( std::string equation ) {

    const string VALID_OPERATIONS = "+ - * / ^ % ( ) [ ] { }";
    const string VALID_VARIABLES = "x y z";

    sstream ss( equation );

    while( !ss.eof() ) {
        char character = ss.get(1);

        if( VALID_OPERATIONS.find( character ) != string::npos ) {
            operations.push( character );
        }
        else if( VALID_VARIABLES.find( character ) != string::npos ) {
            variables.push( character );
        }
        else {
            throw InputException( "Character: " + character + " not recognized." );
        }
    }


}

double * Equation::walkEquation() {
   
}