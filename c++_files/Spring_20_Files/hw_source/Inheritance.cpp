/*#include <iostream>

using namespace std;

//Declares class Blank with no parameters
class Blank {
public:

//Cannot be accessed by child functions
private:
	int numJohn;
	string foo;

//Protected members can be accessed by child functions
protected:
	int protectedThing;

};

//Declares a subclass of Blank that has all of Blanks parameters + its own parameters
class SubBlank : public Blank {
public:
	void setOtherThing(int thing) {
		protectedThing = thing;
	}
private:
	int numberOfPizzas;
protected:
	int otherThing;
};

//Is a child function of SubBlank, so it recieves all of SubBlank but NOT Blank;
class SubSubBlanks : public SubBlank{
public:
	void setThing(int thing) {
	    protectedThing = thing;
		otherThing = thing;
	}

private:

};

void test(string gest) {
	char test[4] = { 'c','o','d','\0' };
	cout << test;
}

int main() {
	test("test");

	return 0;
}*/

