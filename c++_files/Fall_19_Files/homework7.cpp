//Joshua Stevens
//Homework 7
//C++ Parry
/*
  This project is a very early work. The purpose of it is to take in a matrix
  and test if the matrix is a "magic square". I.E. do all the rows/diagonals/columns add up 
  to the same integer.
*/
#include <iostream>

// Bad practice in general, but removes unnecessary complications for this project.
using namespace std;

int main() {

  const int MAX = 5;
  int magicArr[MAX][MAX] = {};
  int answer = 0;
  int test = 0;
  int square;

  // Gets the input for what power the square should be raised to.
  cout << "Enter the order of the square to be tested: ";
  cin >> square;       

  cout << endl << "Enter the " << (square * square) << " values in row major order ";

  // Checks to see if input is small enough to fit in set array
  // then, gets the input for the array.
  if ( square <= MAX ) {
    for ( int i = 0; i < square; i++ ) {    
      for( int j = 0; j < square; j++ ) {
        cin >> magicArr[i][j];
      }
    }
  }
  else {
    cout << endl << "Error, order is too large" << endl;
    return 1;
  }

  // Adds all the rows together.
  cout << endl << "Adding Rows" << endl;    
  for (int i = 0; i < square; i++) {

    answer = 0;

    for (int j = 0; j < square; j++) {
      answer = magicArr[i][j] + answer;
    }

    cout << "Row:" << (i + 1) << " = " << answer << endl;

    // Check to see if the answer is valid.
    if(i > 0 && test != answer) { 

      cout << endl << "Your entry is not a magic square, because Row " << (i + 1) << " does not add up to " << test << " ."<< endl; //error message
      return 1;
    }

    // Set the first answer to a test variable to check everything else against.
    else if(i == 0) {
      test = answer;
    }

  }

  cout << "Adding Columns" << endl;

  // Add up all the columns.   
  for (int i = 0; i < square; i++) {

    answer = 0;

    for (int j = 0; j < square; j++) {
      answer = magicArr[j][i] + answer;

    }
    cout << "Column:" << (i + 1) << " = " << answer << endl;

    // Test each column.
    if(answer != test){     
      cout << "Your entry is not a magic square, because Column " << (i + 1) << " does not add up to " << test << " ."<< endl;
      return 1;
    }
  }

  cout << "Adding Diagonals" << endl; 

  // Add together the first major diagonal.
  answer = 0;
  for (int j = 0; j < square; j++) {
    answer = magicArr[j][j] + answer;
  }
  cout << "Diagonal 1 = " << answer << endl;

  // Test the diagonal.
  if(answer != test){     
    cout << "Your entry is not a magic square, because Diagonal 1 does not add up to " << test << " ."<< endl;
    return 1;
  }

  answer = 0;

  // Add together the second major diagonal.
  for (int j = 0; j < square; j++) {    
    answer = magicArr[j][(square - 1) - j] + answer;
  }

  cout << "Diagonal 2 = " << answer << endl;

  // Test the diagonal.
  if(answer != test){     
    cout << "Your entry is not a magic square, because Diagonal 2 does not add up to " << test << " ."<< endl;
    return 1;
  }

  return 0;
}
