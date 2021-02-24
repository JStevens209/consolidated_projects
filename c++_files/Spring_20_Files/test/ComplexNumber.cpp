// Purpose:  Demonstrate various ways to parse an input string.  This code is
//           for demonstration only.  While the techniques shown for parsing
//           a string can be applied in HW2, this example is NOT intended to
//           be a complete solution for that assignment.
// Date:     Feb 4th, 2016
// Author:   Dr Keith Shomper

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

// ordinarily this class would be defined in its own .h file and included here;
// however, it is pasted here for simplicity in this example
class ComplexNumber {
public:
    ComplexNumber(double real = 0.0, double imag = 0.0);

    friend ComplexNumber operator+ (const ComplexNumber&, const ComplexNumber&);
    friend ComplexNumber operator- (const ComplexNumber&, const ComplexNumber&);
    friend ComplexNumber operator* (const ComplexNumber&, const ComplexNumber&);
    friend ComplexNumber operator/ (const ComplexNumber&, const ComplexNumber&);

    friend ostream& operator<<(ostream& out, const ComplexNumber& c);

private:
    double r;
    double i;
};

void setRunMethods(vector<int>&, int, char**);

// The main test program: if only the program name is passed, then run all
// conversion methods; otherwise we expect a set of method numbers from 1-6
int main(int argc, char** argv) {
    string  s;
    double  x, y;
    int     i;
    vector<int> runMethods = { 1, 2, 3, 4, 5, 6 };

    setRunMethods(runMethods, argc, argv);

    // get a complex number to test, e.g., 3.2+4.5i
    cout << "Enter a point as x+yi:  ";
    cin >> s;

    // C++ Methods
    // 1. use custom code and stod() to parse the results
    if (!runMethods.empty() && runMethods.back() == 1) {
        i = 1;                                   // ignore any leading sign
        while (s[i] != '+' && s[i] != '-') i++;  // find the sign
        x = stod(s.substr(0, i));                // real part is before the sign
        y = stod(s.substr(i + 1));               // imag part is after the sign
        cout << "Using custom code:  you entered "
            << ComplexNumber(x, y) << endl;
        runMethods.pop_back();
    }

    // 2. use custom code with rfind() and substr()
    if (!runMethods.empty() && runMethods.back() == 2) {
        int signPos = max((int)s.rfind("+"), (int)s.rfind("-")); // find sign
        x = stod(s.substr(0, signPos));                       // get real part
        y = stod(s.substr(signPos + 1));                      // get imag part
        cout << "Using find(), etc:  you entered "
            << ComplexNumber(x, y) << endl;
        runMethods.pop_back();
    }

    // 3. use stringstream to parse the results
    //    stringstream works like cin, so just read the two parts of the string
    //    into x and y
    if (!runMethods.empty() && runMethods.back() == 3) {
        stringstream ss(s);
        ss >> x >> y;
        cout << "Using stringstream: you entered "
            << ComplexNumber(x, y) << endl;
        runMethods.pop_back();
    }

    // C Methods
    // 4. use scanf to parse the results
    if (!runMethods.empty() && runMethods.back() == 4) {
        int n = sscanf(s.c_str(), "%lf%lf", &x, &y);
        cout << "Using sscanf:       you entered "
            << ComplexNumber(x, y) << endl;
        runMethods.pop_back();
    }

    // 5. use strtof to parse the results
    if (!runMethods.empty() && runMethods.back() == 5) {
        x = 0; y = 0;
        char* endptr = nullptr;
        x = strtod(s.c_str(), &endptr);
        y = strtod(endptr, nullptr);
        cout << "Using strtod:       you entered "
            << ComplexNumber(x, y) << endl;
        runMethods.pop_back();
    }

    // 6. use strtok() to parse the results
    if (!runMethods.empty() && runMethods.back() == 6) {
        char* str = new char[s.length() + 1]; // allocate a char array to store s
        strcpy(str, s.c_str());               // copy s into the new char array

        // initial parsing
        char* p = strtok(str, "+-i");         // run the tokenizer to split str

        // examine the pieces of str (i.e., until p==NULL), the variable i let's
        // use know whether we're working on the real part (i==1) or imag part
        i = 1;
        while (p != NULL) {
            // convert each piece
            if (i == 1) x = atof(p);
            else        y = atof(p);
            p = strtok(NULL, "+-i");
            i++;
        }
        int signPos = max((int)s.rfind("+"), (int)s.rfind("-")); // find sign
        y = (s[signPos] == '+') ? y : -y;                        // correct on y

        cout << "Using strtok:       you entered "
            << ComplexNumber(x, y) << endl;
        runMethods.pop_back();
    }

    return 0;
}

void setRunMethods(vector<int>& rm, int cnt, char** args) {
    vector<int> v;
    for (int i = 1; i < cnt; i++) {
        int m = atoi(args[i]);
        if (m >= 1 && m <= 6) v.push_back(m);
    }
    if (v.size() > 0) rm = v;
    sort(rm.begin(), rm.end());
    reverse(rm.begin(), rm.end());
}

// below is the ComplexNumber class implementation, ordinarily it would appear
// in its own file, such as ComplexNumber.cpp and linked with the main()
// program; however, it is pasted here for simplicity in the example 
ComplexNumber::ComplexNumber(double rr, double ii) : r(rr), i(ii) {
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

ComplexNumber operator* (const ComplexNumber& a, const ComplexNumber& b) {
    ComplexNumber result;

    result.r = (a.r * b.r - a.i * b.i);
    result.i = (a.r * b.i + a.i * b.r);

    return result;
}

ComplexNumber operator/ (const ComplexNumber& a, const ComplexNumber& b) {
    ComplexNumber result;

    result.r = (a.r * b.r + a.i * b.i) / (b.r * b.r + b.i * b.i);
    result.i = (a.i * b.r - a.r * b.i) / (b.r * b.r + b.i * b.i);

    return result;
}

// This operator is a "pretty-print" replacement for the output operator
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
