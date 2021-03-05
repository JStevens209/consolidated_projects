#include <iostream>
#include <unistd.h>
#include <stdlib.h>
#include <cctype>

using namespace std;

int main(){

  srand(time(0));

  const int COLORS = 4;
  const int ROUNDS = 15;

  char colors[COLORS] = {'R', 'B', 'G', 'Y'};
  char memory[ROUNDS] = {};
  char nextColor;

  string answer;
  string enter;

  cout << "Welcome to Simon Says, press enter to continue..." << endl;
  getline(cin, enter, '\n');

  for(int i = 1; i <= ROUNDS; i++){
    // Chooses a random char in the array by choosing a random number between 0 and 4,
    // then appends the "color" to the end of memory.
    nextColor = colors[(rand() % 4)]; 
    memory[i-1] = nextColor;  
    cout << "Simon says... ";

    system("clear");

    // Outputs memory one "color" at a time.
    for(int j = 0; j < i; j++){   

      cout << memory[j] << flush;
      sleep( 1 );
      cout << "\010." << flush;
      usleep( 300000 );
      
    }

    cout << endl << "Please enter the " << i << " characters that match: ";

    // This is here to clear the buffer zone for the next cin, 
    // if this wasnt here, the program would skip over the cin.
    cin.clear();
    cin >> answer;

    // Standardizes the format of the string
    for(int i = 0; i < answer.length(); i++) {
  			answer[i]=toupper(answer[i]);
  	}

    // Tells the player where they went wrong
    for(int i = 0; i < ROUNDS && i < answer.length(); i++){ 

      if( answer[i] != memory[i] ){
        cout << endl << "Aww, you lost :(" << endl;
        cout << "The correct sequence was, " << memory << endl; 
        
        cout << "You messed up on letter " << (i+1)  << "." << endl;  
        return 1;
      }
    }
  }

  // This will only ever output on a "win" because
  // getting to this point is only possible by
  // Iterating throughout the entire 15 rounds without error.
  cout << "Congratulations! You win!" << endl;  
  return 0;
}
