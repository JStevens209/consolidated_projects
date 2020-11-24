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

  for(int i = 0; i < size; i ++)
  {
    isRepeat = false; //sets this variable to false for every new char that is tested
    for(int j = 0; j < size; j++)
    {
      if(noRepeats[j] == array[i]) //Checks if there is any character in noRepeats that is the same as the character at array[i]
      {
        isRepeat = true;
        numberRepeats ++; //Counts how many null chars there would be in the array if this character wasnt printed
      }
    }

    if(isRepeat == false)
    {
      noRepeats[i - numberRepeats] = array[i]; //Sets array[i] to noRepeats[i - the number of deleted/not printed characters]
    }

  }
  cout << "\"" << array << "\"" << " Without any repeats is: " << endl << noRepeats << endl; //prints out original without repeats


}
int main()
{
  //Variable Declarations:
  const int SIZE = 512;
  string input;
  int length;
  char cstring[SIZE] ={};
  string cont = "yes";

while(cont == "yes")
  {
      cout << "Please enter a new string: " << endl;

      cin.ignore(); //This is included so that the getline doesnt just read a /n from the buffer and skip getting an input.
      getline(cin, input);

    if(input.length() < SIZE) //Is the input an acceptable size?
    {
        strcpy(cstring, input.c_str());
        length = input.length();
        delete_repeats(cstring, length);
    }
    else
    {
      cout << "ERROR: String length too long, please enter a shorter string." << endl;
      return 1;
    }
      cout << "Continue? yes/no" << endl;
      cin >> cont;

  }

  return 0;
}
