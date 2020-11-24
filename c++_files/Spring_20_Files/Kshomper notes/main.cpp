#include <iostream>
#include "notes.h"

using namespace std;

int main() {
    try {
        //The thing that is thrown MUST have a type
        throw(2);
    }
    //The catch used is determined by the TYPE of throw
    catch(int) {
        cout << "speed" << endl;
    }
    TemplateClass<int> *foo;
    int c = 1;
    int d = 2;

    foo->swap(c, d);
    cout << c << " " << d << endl;

    foo->print();
    return 0;

}
