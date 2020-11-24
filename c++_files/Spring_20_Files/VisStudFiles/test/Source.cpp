/*#include <iostream>

using namespace std;

class Student {

public:

	string firstName;
	string lastName;
	string level;

};

int main(int argc, char** argv) {

	int* ip;
	Student* sp;
	Student s;

	s.firstName = "John";
	s.lastName = "Doe";
	sp = &s;

	int intArray[5] = { 2,5,7,9,12 };
	ip = intArray; //Arrays are ALWAYS passed by reference

	cout << ip << " " << *ip << " " << &intArray << endl;

	return 0;
}*/