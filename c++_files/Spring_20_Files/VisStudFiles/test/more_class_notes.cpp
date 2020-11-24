/*#include <iostream>
#include "complex.h"
using namespace std;

//a = b + c where b is a real number and c is n*i, forming a complex number
//Function definition for an operator function that adds two ComplexNumbers
						//Always passes the operator "this", which is a pointer to the class definition
ComplexNumber operator(const ComplexNumber& c) const { //Makes the 
	ComplexNumber result;
	result.r = r + c.r; //r is b.r because this is lhs
	result.i = i + c.i; //i is b.i because this is lhs

	
	return result;
}

int main(int argc, char* argv[]) {
	/*
	Constructors:												}
	-Have name as Class.
	-Have NO return type.
	-Are only member function w/ init. list.					}
	-Are auto invoked at declaration.								  }
	-Default and Copy constructors given automatically.
	-Their purpose is to init.the data members of the class	.	}        } All member functions have implicit
																			first parameter: class_name *this
	Getters:														  }
	-Should be const											}

	Operators:
	-Defined with keyword "operator".							}

	Friends:
	-Have access to plass' data member,
	 BUT they are NOT member functions.
	*/


	/*
	
	. = selection operator
	-> - dereference and selection operator

	if you have a ComplexNumber*
	resultptr points to something

	then you go and say resultPtr.r = 0.0 you will get an error
	if you go and say (*resultPtr).r = 0.0 it will work

	-> does the same thing as (*resultPtr).r so resultPtr->r = 0.0
	
	*/
