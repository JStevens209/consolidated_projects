/*#include <iostream>
#include <vector>
#include "complex.h"

using namespace std;

// class implementation (or function bodies)

// this section typically appears in a ".cpp" file called after the class name

// and will include the corresponding .h file as shown below

//The purpose of a CONSTRUCTOR, is to INITIALIZE the DATA MEMBERS of the class

double ComplexNumber::getRealPart() const {

    return r;

}

void ComplexNumber::setImagPart(double value) {

    i = value;

}



// class usage (or client or test program)

// this section will typically appear in a ".cpp" file and often with a main()

// for CS1220 our test programs will be called after the class they test

// e.g., TestComplexNumber.cpp and will also include the class' .h file

using namespace std;

int main() {

    // object declaration

    ComplexNumber c;



    // set (or get) attributes of object

    c.setRealPart(1.2);

    c.setImagPart(c.getRealPart());



    // print c to see if it has the expected value (i.e., 1.2+1.2i)

    cout << c.r << "+" << c.i << "i" << endl;



    return 0;

}






//goes in .h files
/*class Cars { 
public: //users can access these
	
	void Print(); // prints...
	//function declarations go here(member functions, methods)
	//If a function is implemented here: called "inline", uncommon, except for "one liners".

private: //users cant access this data (encaspulation)
	
	int liscencePlate = 456;

	//data members (aka attributes)
	//helper functions
};


//------------------------------------------------------------------------------------------------------------------------
// ____.cpp file

//#include "_____.h"

//function implementation
void Cars::Print() { //:: == scope resolution operator
	
 }


//function bodies

//Implementation of class I.E. function body
int main(int argc, char* argv[]) {

	return 0;
}*/