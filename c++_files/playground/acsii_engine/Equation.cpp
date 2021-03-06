#include "Equation.h"
#include <sstream>
#include <regex>

Equation::Equation( std::string equation ) {
    
    try {
        parseEquation( equation );
    }
    catch InputException(e) {
        // TODO: Add error handling
    }
}   

void Equation::parseEquation( std::string equation ) {

    // Matches the characters +-*/^%()[]{}.
    if( regex_match( equation, std::regex( "[\\+\\-\\*\\/\\^\\%\\(\\)\\[\\]\\{\\}]" ))) {
        operations.push( character );
    }
    // Matches the characters xyz, then any number between 0 and 9.
    if( std::regex_match( equation, std::regex( "[x-z0-9]+" ))) {
        variables.push( character );
    }
    else {
        throw InputException( "Character: " + character + " not recognized." );
    }

}

double * Equation::walkEquation() {
   
}