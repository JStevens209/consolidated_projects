// Author:  Keith A. Shomper
// Date:    2/13/20
// Purpose: To specify a simple, linked-list of sorted positive integers

// The following pattern prevents multiple inclusion of class definitions
#ifndef LLSPOSINT_H
#define LLSPOSINT_H

#include <iostream>
using namespace std;

struct  Node;
typedef Node* NodePtr;

// The key value HEAD_OF_LIST is used as a "sentinal" value
const int HEAD_OF_LIST = -1;

class LLSortedPosInt {
public:
    // constructors
    LLSortedPosInt();
    LLSortedPosInt(int  key);
    LLSortedPosInt(int* keys, int n);
    LLSortedPosInt(const LLSortedPosInt& l);

    // destructor
    ~LLSortedPosInt();

    // assignment operator
    LLSortedPosInt& operator= (const LLSortedPosInt& l);

    // print operator (non-member function)
    friend ostream& operator<<(ostream& out, const LLSortedPosInt& l);

    // other member functions
    bool                  isEmpty() const;
    bool                  containsElement(int key) const;

    // other operator member functions
    bool                  operator==(const LLSortedPosInt& l) const;
    bool                  operator!=(const LLSortedPosInt& l) const;

    // other operator functions (non-member functions)
    friend LLSortedPosInt operator+ (const LLSortedPosInt& l1,
        const LLSortedPosInt& l2);
    friend LLSortedPosInt operator- (const LLSortedPosInt& l1,
        const LLSortedPosInt& l2);
private:
    // helper functions
    void                  insert(int key);
    void                  remove(int key);
    // NOTE: see also the non-member function createNode() associated .cpp file

    // the data member for this class is a single item similar to the example
    // in ZyBook 12.21
    NodePtr head;
};

#endif //LLSPOSINT_H
