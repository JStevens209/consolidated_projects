// Author: Joshua Stevens
// Professor: Dr. Perry
/* 
  Purpose: This program takes an input string, removes the repeated characters 
  using a function, and then outputs the string back to the command line
*/

#include <iostream>
#include <cstring>
#include <cctype>


using namespace std;

void delete_repeats(char array[], int size)
{
  char noRepeats[512]= {};
  char arrayTest = array[0];

  bool isRepeat = false;
  
  int numberRepeats = 0;

  for( int i = 0; i < size; i++ ) {
    // Set this variable to false for every new char that is tested
    isRepeat = false; 

    for( int j = 0; j < size; j++ ) {

      // Check if there is any character in noRepeats that is the same as the character at array[i]
      if( noRepeats[j] == array[i] ) {

        // Count how many null chars there would be in the array if this character wasnt printed
        isRepeat = true;
        numberRepeats ++; 
      }
    }

    if( isRepeat == false ) {

      // Set array[i] to noRepeats[i - the number of deleted/not printed characters].
      noRepeats[i - numberRepeats] = array[i];
    }
  }

  // Print out original without repeats.
  cout << "\"" << array << "\"" << " Without any repeats is: " << endl << noRepeats << endl; 
}
int main()
{
  char cstring[SIZE] ={};

  const int SIZE = 512;
  int length;
  
  string input;
  string cont = "yes";
  
  while(cont == "yes") {
    cout << "Please enter a new string: " << endl;

    // This is included so that the getline doesnt just read a /n 
    // from the buffer and skip getting an input.
    cin.ignore();
    getline(cin, input);

    // Check if Input fits within the max size of the cstring.
    if( input.length() < SIZE ) {

        strcpy( cstring, input.c_str() );
        length = input.length();

        delete_repeats( cstring, length );
    }
    else {
      cout << "ERROR: String length too long, please enter a shorter string." << endl;
      return 1;
    }
      cout << "Continue? yes/no" << endl;
      cin >> cont;

  }

  return 0;
}
