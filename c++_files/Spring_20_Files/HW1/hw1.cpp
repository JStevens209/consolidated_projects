#include <iostream>
#include <vector>
#include <string>

using namespace std;

int zymain(int, char**);

void reverse(char* front, char* rear) {
	//Note to self: swap() is a thing.
	char memory;
	string string = front;
	int midpoint = 0;

	//Finds the midpoint of the distance
	midpoint = (string.length() / 2) + (string.length() % 2);

	//Reverses the section called
	for (int i = 0; i < midpoint; i++) {
		memory = *(rear - i);
		*(rear - i) = *(front + i);
		*(front + i) = memory;
	}
}

int main(int argc, char* argv[]){

	// Submitted via zybooks, this is necessary.
	return zymain(argc, argv);
	
}

int zymain(int argc, char* argv[]) {

	//Checks if there are the four expected command line arguments
	if (argc != 4) {
		cerr << "Expected 4 arguments" << endl;
		return 1;
	}

	string str = argv[1];
	char frontIndex = *argv[2];
	char rearIndex = *argv[3];

	//turns front/rearIndex into integers
	int frontInt = atoi(argv[2]);
	int rearInt = atoi(argv[3]);

	//Checks if frontIndex and rearIndex are integers
	if (((rearInt == 0) && (rearIndex != '0')) || ((frontInt == 0) && (frontIndex != '0'))) {
		cerr << "Invalid characters" << endl;
		return 2;
	}

	//Checks if rearIndex is after frontIndex
	if (frontInt > rearInt) {
		cerr << "Invalid integers" << endl;
		return 3;
	}

	//Checks if frontInt and rearInt are in the bounds of the given string
	if ((frontInt < 0) || (rearInt > str.size())) {
		cerr << "Arguments out of bounds" << endl;
		return 4;
	}

	//declares char pointers too the 1st command line argument at the argv[2/3] char.
	char* front = &argv[1][frontInt];
	char* rear = &argv[1][rearInt];

	//Calls reverse function
	reverse(front, rear);

	cout << "\"" << argv[1] << "\"" << endl;

	return 0;
}