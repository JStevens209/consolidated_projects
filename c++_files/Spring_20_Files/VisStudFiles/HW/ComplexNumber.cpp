// Author:  Keith A. Shomper
// Date:    Jan 7, 2020
// Purpose: Starter code for HW#2

#include <cstdio>
#include <cstring>
#include <string>
#include "ComplexNumber.h"
#include <cstring>
//STUB
ComplexNumber::ComplexNumber(const char* str) {
    //findImag(str);
}

ComplexNumber::ComplexNumber(float real, float imag) {
    r = real;
    i = imag;
}

ComplexNumber::ComplexNumber(const ComplexNumber& rhs) {
    r = rhs.r;
    i = rhs.i;
}

ComplexNumber& ComplexNumber::operator=(const ComplexNumber& rhs) {
    r = rhs.r;
    i = rhs.i;
    return *this;
}

bool ComplexNumber::operator==(const ComplexNumber& rhs) const {
    return (r == rhs.r && i == rhs.i);
}
//STUB
ComplexNumber operator* (const ComplexNumber& a, const ComplexNumber& b) {
    ComplexNumber result;
    result.r = (a.r * b.r) - (a.i * b.i);
    result.i = (a.r * b.i) + (b.r * a.i);
    return result;
}

ComplexNumber operator+ (const ComplexNumber& a, const ComplexNumber& b) {
    ComplexNumber result;

    result.r = a.r + b.r;
    result.i = a.i + b.i;

    return result;
}

ComplexNumber operator- (const ComplexNumber& a, const ComplexNumber& b) {
    ComplexNumber result;

    result.r = a.r - b.r;
    result.i = a.i - b.i;

    return result;
}

ostream& operator<< (ostream& out, const ComplexNumber& b) {
    bool rPrinted = false;

    if (b.r != 0 || (b.r == 0 && b.i == 0)) {
        out << b.r;
        rPrinted = true;
    }

    if (b.i > 0) {
        if (rPrinted) {
            out << "+";
        }
        if (b.i != 1) {
            out << b.i;
        }
        out << "i";
    }
    else if (b.i < 0) {
        if (b.i == -1) {
            out << "-";
        }
        else {
            out << b.i;
        }
        out << "i";
    }
    return out;
}

//STUB
istream& operator>>(istream& in, ComplexNumber& c) {
    
    return in;
}


