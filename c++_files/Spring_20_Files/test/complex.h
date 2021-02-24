/*#pragma once
#include <iostream>

using namespace std;

class ComplexNumber {

    // this is the common use of "public", that is making members functions public

public:

    // accessor functions

    double getRealPart()  const;

    double getImagPart() const { return i; }

    ComplexNumber(const char i);



    // mutator functions

    void setRealPart(double value) { r = value; }

    void setImagPart(double value);

    // the data members are stll "public" -- is generally bad design

    double r;

    double i;

};*/