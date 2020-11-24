
#include <string>
#include <vector>

std::vector<std::vector<std::string>> ciphertextFreq;
std::vector<std::vector<std::string>> plaintextFreq;


// string str is the cyphertext
void updateCiphertextFreq(const std::string str) {
	ciphertextFreq.clear();
	//create a character array as a copy of str
	char* cipherText = new char[str.length()+1];
	strcpy(cipherText, str.c_str());

	// for each letter of the alphabet
	for (int i = 0; i < 26; i++) {
		// counts number of a specific character 
		int charCount = 0;
		// letter is the letter that is associated to this loop cycle
		char letter = (int('A') + i);
		// for each char in the string passed to the function by parameter
		for (int j = 0; j < str.length(); j++) {
			// if a char in the string is the letter that is currently being counted,
			// increment the counter
			if (letter == cipherText[j]) {
				charCount++;
			}
		}

		// make a vector that holds the current loop cycles
		// letter and the number of times it appeared
		std::vector<std::string> letterSet;
		letterSet.push_back(std::string(1,letter));
		letterSet.push_back(std::to_string(charCount));
		// push this into the ciphertext frequency vector
		ciphertextFreq.push_back(letterSet);
	}

	delete[] cipherText;
}

// I created this because just look at the first if statement of
// updatePlaintextFreq()
// ... That would've been awful lol
void ptVectSet(std::string l, std::string n) {
	// make a vector that holds the current loop cycles
	// letter and the number of times it appeared
	std::vector<std::string> letterSet;
	letterSet.push_back(l);
	letterSet.push_back(n);
	// push this into the plaintext frequency vector
	plaintextFreq.push_back(letterSet);
}



// string str is the plaintext for comparing frequencies
// MAKE SURE YOU PASS A bool AS THE LAST PARAMETER!!!
// bool isDefault is whether or not default english is selected ==> if true, then default english
void updatePlaintextFreq(const std::string str, bool isDefault = true) {
	plaintextFreq.clear();

	if (isDefault) {
		// They are in order of the alphabet. I did this because every other time I
		// filled a vector, I also did it in alphabetical order. Maybe this will make the
		// graph/table a little easier
        ptVectSet("A","8.2");
        ptVectSet("B", "1.5");
        ptVectSet("C", "2.8");
        ptVectSet("D", "4.3");
        ptVectSet("E", "13.0");
        ptVectSet("F", "2.2");
        ptVectSet("G", "2.0");
        ptVectSet("H", "6.1");
        ptVectSet("I", "7.0");
        ptVectSet("J", ".15");
        ptVectSet("K", ".77");
        ptVectSet("L", "4.0");
        ptVectSet("M", "2.4");
        ptVectSet("N", "6.7");
        ptVectSet("O","7.5");
        ptVectSet("P", "1.9");
        ptVectSet("Q", "0.095");
        ptVectSet("R", "6.0");
        ptVectSet("S", "6.3");
        ptVectSet("T", "9.1");
        ptVectSet("U", "2.8");
        ptVectSet("V", "0.98");
        ptVectSet("W", "2.4");
        ptVectSet("X", "0.15");
        ptVectSet("Y", "2.0");
        ptVectSet("Z", "0.074");
	}
	else {
		//create a character array as a copy of str
		char* plainText = new char[str.length() + 1];
		strcpy(plainText, str.c_str());

		// for each letter of the alphabet
		for (int i = 0; i < 26; i++) {
			// counts number of a specific character 
			int charCount = 0;
			// letter is the letter that is associated to this loop cycle
			char letter = (int('a') + i);
			// for each char in the string passed to the function by parameter
			for (int j = 0; j < str.length(); j++) {
				// if a char in the string is the letter that is currently being counted,
				// increment the counter
				if (tolower(letter) == tolower(plainText[j])) {
					charCount++;
				}
			}

			// make a vector that holds the current loop cycles letter and the number of times it appeared
			ptVectSet(std::string(1, letter), std::to_string(charCount));
		}

		delete[] plainText;
	}
}


/*
// makes calling for default english easier, however this isn't necessary to have
// this can take zero parameters because it defaults to true
void updatePlaintextFreq(bool isDefault = true) {
	updatePlaintextFreq("", isDefault);
}
*/


/*
int main() {
	//TESTS, uncomment to use
    //updateCiphertextFreq("I JUST MADE A BIG OL PIZZA, AINT THAT GRAND!"); // This isn't cyphertext but it doesn't matter

	// I just continued these lines because this is a large paragraph
	//updatePlaintextFreq("Lorem ipsum dolor sit amet, consectetur adipiscing elit,\
 sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, \
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute \
irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit ani\
m id est laborum.", false);
	// MAKE SURE YOU PASS THIS FUNCTION A bool FOR THE LAST PARAMETER!!!!

	//default english
	//updatePlaintextFreq();

	return 0;

}
*/



