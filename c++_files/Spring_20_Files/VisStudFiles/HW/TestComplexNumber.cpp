// Author:  Keith A. Shomper
// Date:    Jan 07, 2020
// Purpose: A test program for HW#2.  
// NOTE:    To compile and link this program with the provided code, you must
//          FIRST provide specifications for the three new functions as
//          described in the ZyLab write up and provide at least a stub
//          implementation of each of these functions in ComplexNumber.cpp.

#include <iostream>
#include "ComplexNumber.h"

using namespace std;

void testMultiply(const ComplexNumber& result, const ComplexNumber& expected);

int main() {

    // test the multiplication operator
    ComplexNumber a(4, 2);
    testMultiply(a * 3, ComplexNumber(12, 6));
    testMultiply(a * ComplexNumber(1, -1.5), ComplexNumber(7, -4));

    // test string constructor (note, you may also want to test other values)
    cout << "Testing string constructor:\n";
    cout << " * real number only:   " << ComplexNumber("2.54") << endl;
    cout << " * imaginary only:     " << ComplexNumber("3.2i") << endl;
    cout << " * real and imaginary: " << ComplexNumber("2+4i") << endl;

    // test assignment of multiple objects via input operator
    ComplexNumber x, y;
    cout << "Enter two complex numbers:  ";
    //Note: Stops at space
    cin >> x >> y;
    cout << "\nYou entered:\n";
    cout << " * " << x << "\n * " << y << endl;

    // additonal user selected test cases - try several values to ensure the
    // correctness of your implementation
    ComplexNumber z;
    cout << "Please enter a list of complex numbers (type <CTRL-D> to exit): \n";
    cin >> z;

    if (!cin.eof()) cout << "You entered:\n";
   /* while (!cin.eof()) {
        cout << " * " << z << endl;
        cin >> z;
    }*/

    return 0;
}

void testMultiply(const ComplexNumber& result, const ComplexNumber& expected) {
    if (result == expected) {
        cout << "Multiply test passed\n";
    }
    else {
        cout << "Multiply test failed\n";
    }
}

