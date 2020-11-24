//Joshua Stevens
//Homework 7
//C++ Parry


#include <iostream>



using namespace std;

int main() {

  //Declared Variables
  const int MAX = 5;
  int magicArr[MAX][MAX] = {};
  int answer = 0;
  int test = 0;
  int square;

  cout << "Enter the order of the square to be tested: ";
  cin >> square;       //gets the input for what power the square should be raised to

  cout << endl << "Enter the " << (square * square) << " values in row major order ";
  if (square <= MAX) {    //checks to see if input is small enough to fit in set array
    for (int i = 0; i < square; i++) {    //gets the input for the array
      for(int j = 0; j < square; j++) {
        cin >> magicArr[i][j];
      }
    }
  }
  else {
    cout << endl << "Error, order is too large" << endl;
    return 1;
  }

  cout << endl << "Adding Rows" << endl;    //adds all the rows together
  for (int i = 0; i < square; i++) {
    answer = 0;
    for (int j = 0; j < square; j++) {
      answer = magicArr[i][j] + answer;
    }
    cout << "Row:" << (i + 1) << " = " << answer << endl;

    if(i > 0 && test != answer) { //checks to see if the answer is valid

      cout << endl << "Your entry is not a magic square, because Row " << (i + 1) << " does not add up to " << test << " ."<< endl; //error message
      return 1;
    }
    else if(i == 0) //sets the first answer to a test variable to test everything else against
    {
      test = answer;
    }

  }

  cout << "Adding Columns" << endl;   //adds all the columns together
  for (int i = 0; i < square; i++) {
    answer = 0;
    for (int j = 0; j < square; j++) {
      answer = magicArr[j][i] + answer;

    }
    cout << "Column:" << (i + 1) << " = " << answer << endl;

    if(answer != test){     //tests each column
      cout << "Your entry is not a magic square, because Column " << (i + 1) << " does not add up to " << test << " ."<< endl;
      return 1;
    }
  }

  cout << "Adding Diagonals" << endl; //adds together the first major diagonal
  answer = 0;
  for (int j = 0; j < square; j++) {
    answer = magicArr[j][j] + answer;
  }
  cout << "Diagonal:1 = " << answer << endl;

  if(answer != test){     //tests the diagonal
    cout << "Your entry is not a magic square, because Diagonal 1 does not add up to " << test << " ."<< endl;
    return 1;
  }

  answer = 0;
  for (int j = 0; j < square; j++) {    //adds together the second major diagonal
    answer = magicArr[j][(square - 1) - j] + answer;
  }
  cout << "Diagonal:2 = " << answer << endl;

  if(answer != test){     //tests the diagonal
    cout << "Your entry is not a magic square, because Diagonal 2 does not add up to " << test << " ."<< endl;
    return 1;
  }

  return 0;
}
