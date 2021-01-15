#ifndef VECTOR_MATH_CPP
#define VECTOR_MATH_CPP

#include <vector>
#include <math.h>
#include <stdlib.h>

using namespace std;

// All equations with multiple inputs assume vectors are the same shape: (3,).
// I only needed it to handle vectors of shape (3,), so I didn't bother making general solutions.

// Calculates the dot product of 2 vectors
double dot_product( vector<double> left, vector<double> right ) {

    double answer;

    for( int i = 0; i < left.size(); i++ ) {

        answer += left.at(i) * right.at(i);
    }

    return answer;
}

// Calculates cross product of 2 vectors
vector<double> cross_product( const vector<double> left, const vector<double> right ) {
    
    vector<double> answer;

    // cx = ( ay * bz ) - ( az * by )
    answer.push_back( ( left.at(1) * right.at(2) ) - ( left.at(2) * right.at(1) ) );
    // cy = ( az * bx ) - ( ax * bz )
    answer.push_back( ( left.at(2) * right.at(0) ) - ( left.at(0) * right.at(2) ) );
    // cz = ( ax * by ) - ( ay * bx )
    answer.push_back( ( left.at(0) * right.at(1) ) - ( left.at(1) * right.at(0) ) ); 

    return answer;
} 

// Calculates the length of a vector squared
double vector_length( const vector<double> input ) {
    
    double answer = 0;

    for( int i = 0; i < input.size(); i++ ) {

        answer += input.at(i) * input.at(i);
    }

    return answer;
}

// Calculates the addition of 2 vectors
vector<double> vector_addition( const vector<double> left, const vector<double> right ) {
    
    vector<double> answer;

    for( int i = 0; i < left.size(); i++ ) {

        answer.push_back( left.at(i) + right.at(i) );
    }

    return answer;
}

vector<double> constant_multiplication( const double constant, const vector<double> right ) {
    
    vector<double> answer;

    for( int i = 0; i < right.size(); i++ ) {

        answer.push_back( right.at(i) * constant );
    }

    return answer;
}

#endif