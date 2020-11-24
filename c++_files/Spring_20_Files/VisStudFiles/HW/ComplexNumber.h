// Author:  Keith A. Shomper
// Date:    Jan 7, 2020
// Purpose: Starter code for HW#2

#include <iostream>
#include <cstring>

using namespace std;

class ComplexNumber {
public:
    // constructors (copy constructor not necessary, included for illustration)
    ComplexNumber(float real = 0.0, float imag = 0.0);
    ComplexNumber(const ComplexNumber& rhs);

    //Constructor
    ComplexNumber(const char* str);

    // assignment operator (not necessary, included for illustration)
    ComplexNumber& operator=(const ComplexNumber& rhs);

    // the multiplication operation is a member function
    // * Operator
    friend ComplexNumber operator*(const ComplexNumber& a, const ComplexNumber& b);

    // equality operator needed for unit test in HW2
    bool operator==(const ComplexNumber& rhs) const;

    // +/- Operators
    friend ComplexNumber operator+(const ComplexNumber&, const ComplexNumber&);
    friend ComplexNumber operator-(const ComplexNumber&, const ComplexNumber&);
    // I/O Operators
    friend ostream& operator<<(ostream&, const ComplexNumber&);
    friend istream& operator>>(istream& in, ComplexNumber& c);

    // data members
private:
    float r;
    float i;

    const char* findReal(const char* str) {

    }
    const char* findImag(const char* str) {
        const char* pos1 = strchr(str, '+');
        const char* pos2 = strrchr(str, 'i');
       
        cout << pos1 << " " << pos2;
        return 0;
    }
};


