#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <cctype>

using namespace std;

int main(){
  //Variable Declarations
  srand(time(0));
  const int COLORS = 4;
  const int ROUNDS = 15;
  char colors[COLORS] = {'R', 'B', 'G', 'Y'}; //declares what chars will show up
  char memory[ROUNDS] = {};
  char nextColor;
  string answer;
  string enter;

  cout << "Welcome to Simon Says, press enter to continue..." << endl;
  getline(cin, enter, '\n');  //looks for a newline input.

  for(int i = 1; i <= ROUNDS; i++){ //This is the for loop that every other for loop runs off of, this one counts which round we are on.
    nextColor = colors[(rand() % 4)]; //chooses a random char in the array by choosing a random number between 0 and 4.
    memory[i-1] = nextColor;  //appends the next "color" to the end of memory
    cout << "Simon says... ";

    system("clear");  //clears the terminal screen

    for(int j = 0; j < i; j++){   //outputs memory one "color" at a time.

      cout << memory[j] << flush;
      sleep(1);
      cout << "\010." << flush;
      usleep(300000);
    }

    cout << endl << "Please enter the " << i << " characters that match: ";

    cin.clear();  //This is here to clear the buffer zone for the next cin, if this wasnt here, the program would skip over the cin.
    cin >> answer;

    for(int i = 0; i < answer.length(); i++) //Standardizes the format of the string
  		{
  			answer[i]=toupper(answer[i]);
  		}

    for(int i = 0; i < ROUNDS && i < answer.length(); i++){ //This is set in a for loop to be able to iterate through the answer

      if(answer[i] != memory[i]){                         //it needs to iterate because I wanted it to tell the player where they went wrong
        cout << endl << "Aww, you lost :(" << endl;
        cout << "The correct sequence was, " << memory << endl;   //gives the correct sequence
        cout << "You messed up on letter " << (i+1)  << "." << endl;  //tells the player where they went wrong
        return 1;
      }
    }
  }

  cout << "Congratulations! You win!" << endl;  //This will only ever output on a "win" because
                                                //getting to this point is only possible by
                                                //Iterating throughout the entire 15 rounds without error.
  return 0;
}
