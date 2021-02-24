#include <iostream>
using namespace std;

class Stack {
public:
	Stack(int size = 1);              // make a new stack
	~Stack();                         // finalize the stack
	Stack& operator=(const Stack& s) {
		char charArray[s.size] = s.storage;
	}									// assign one stack to another
	void push(char c);                // push c onto the stack 
	char pop();                       // pop top char off the stack
	bool isEmpty() const;             // ask if the stack is empty
	bool isFull()  const;             // ask if the stack is full
	void resize(int size);            // resize the stack to size chars
	friend ostream& operator<<(
		ostream& out, const Stack& s);  // print the stack
private:
	char* storage;                    // place where chars are stored
	int  num;                         // number of chars stored in the stack
	int  size;                        // max num of chars that could be stored
};
