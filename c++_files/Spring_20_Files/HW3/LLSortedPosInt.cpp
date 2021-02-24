// Author:  Keith A. Shomper
// Additions: Joshua Stevens
// Date:    2/13/20
// Purpose: To implement a simple, sorted linked-list of positive integers

#include "LLSortedPosInt.h"

// The linked-list is constructed of Node elements
struct Node {
    int   key;
    Node* next;
};

// the following function is not a member function, it is a convenience
// function which exists to make the implementation of the LLSortedPosInt
// class more concise

// createNode() allocates a Node and initializes it with the
// given parameter values to simplify the initilization of a Node
static NodePtr createNode(int key, NodePtr p) {
    // allocate a new Node for storing the given key value
    NodePtr npp = new Node;

    // store the key value and the next pointer
    npp->key = key;
    npp->next = p;

    // return the new Node to the caller
    return npp;
}

// Student implementation of LLSortedPosInt begins here

// Constructors
LLSortedPosInt::LLSortedPosInt() {
    // creates the sentinal Node at the head of the list
    head = new Node;
    head = createNode(HEAD_OF_LIST, NULL);

    //head->key  = HEAD_OF_LIST;
    //head->next = NULL;
}

LLSortedPosInt::LLSortedPosInt(int key) {
    // create the sentinal Node at the head of the list
    head       = new Node;
    head = createNode(HEAD_OF_LIST, NULL);

    // add the single element key, as long as it is positive
    if (key > 0) {
        insert(key);
    }
}

LLSortedPosInt::LLSortedPosInt(int* keys, int n) {
    // create the sentinal node at the head of the list
    head = new Node;
    head = createNode(HEAD_OF_LIST, NULL);

    // add new Nodes for each positive value in keys
    for (int i = 0; i < n; i++) {
        if (keys[i] > 0) {
            insert(keys[i]);
        }
    }
}

LLSortedPosInt::LLSortedPosInt(const LLSortedPosInt& l) {
    // create a deep copy of the input list l
    NodePtr npp = l.head;
    head        = new Node;
    head        = createNode(HEAD_OF_LIST, NULL);

    while (npp->next != NULL) {
        npp = npp->next;
        insert(npp->key);
    }
}

// Destructor
LLSortedPosInt::~LLSortedPosInt() {
    // free the Nodes in *this, including the sentinal
    NodePtr npp;
    NodePtr npc = head;
    while (npc != NULL) {
        npp = npc;
        npc = npc->next;
        delete npp;
    }
    head = NULL;
}

// Assignment Operator
LLSortedPosInt& LLSortedPosInt::operator=
(const LLSortedPosInt& l) {
    // handle self assignment
    if (this == &l) {
        return *this;
    }

    // free old elements of the list before the new elements from l are assigned
    NodePtr npp = head;
    NodePtr npc = head->next; //Skips over sentinel node

    while (npc != NULL) {
        npp = npc;
        npc = npc->next;
        delete npp;
    }
    npp = head;
    head->next = NULL;

    // build the list as a deep copy of l
    NodePtr npl = l.head->next;

    while (npl != NULL) {
        insert(npl->key);
        npl = npl->next;
    }

    // return *this
    return *this;
}

// Print Operator (a non-member function)
ostream& operator<<  (ostream& out, const LLSortedPosInt& l) {
    NodePtr npp = l.head;
    // an empty list will be printed as <>
    if (npp->next == NULL) {
        out << "<>";
        return out;
    }
    // a singleton list (a list having one key value k) will be
    //     printed as <k>
    npp = npp->next;
    if (npp->next == NULL) {
        out << "<" << npp->key << ">";
    }
    // a list having multiple keys such as 2, 5, 7 will be printed
    //     as <2, 5, 7>
    else {
        //First bracket
        out << "<";
        //Prints each key
        while (npp != NULL) {
            if (npp->next != NULL) {
                out << npp->key << ", ";
            }
            else {
                out << npp->key;
            }
            npp = npp->next;
        }
        //Second bracket
        out << ">";
    }
    return out;
}

// Boolean Functions
bool LLSortedPosInt::isEmpty() const {
    // return true if only the sentinal is in the list; return false otherwise
    if (head->next == NULL) {
        return true;
    }
    return false;
}

bool LLSortedPosInt::containsElement(int key) const {
    // return true if key is in the list; return false otherwise
    NodePtr npp = head;
    while (npp != NULL) {
        npp = npp->next;
        if (npp != NULL && npp->key == key) {
            return true;
        }
    }
    return false;
}

// Other Operator Member Functions
bool LLSortedPosInt::operator==(const LLSortedPosInt& l) const {
    // compare the Nodes in *this with the Nodes in l
    //Declared pointers to walk through both lists
    NodePtr npt = head->next;
    NodePtr npl = l.head->next;

    while ((npt != NULL) && (npl != NULL)) {
        //if the lists are ever not equal, code will exit with false
        if (npt->key != npl->key) {
            return false;
        }
        npt = npt->next;
        npl = npl->next;
    }
    // if all Node key values in *this match the cooresponding
    //  Node key values in l, then the lists are equivalent
    if ((npl == NULL) && (npt == NULL)) { //Only passes true if both pointers reached NULL pointers at the same time, meaning they are equal lengths
        return true;
    }
    else {
        return false;
    }
}

bool LLSortedPosInt::operator!=(const LLSortedPosInt& l) const {
    // do the opposite of operator==
    NodePtr nph = head->next;
    NodePtr npl = l.head->next;

    while ((nph && npl) != NULL) {
        //If they have any inequal keys, return true
        if (nph->key != npl->key) {
            return true;
        }
        nph = nph->next;
        npl = npl->next;
    }
    //Returns true if the lengths are not equal, if all cases fail, return false
    if (nph != npl) {
        return true;
    }
    else {
        return false;
    }
}

// Other Operator Functions (non-member functions)
LLSortedPosInt  operator+ (const LLSortedPosInt& l1,
    const LLSortedPosInt& l2) {
    // create a copy of l1 and add each element of l2 to it in
    // the correct (sorted ascending) order, allow duplicates
    LLSortedPosInt sum(l1);
    NodePtr np2 = l2.head->next;

    while (np2 != NULL) {
        sum.insert(np2->key);
        np2 = np2->next;
    }
    return sum;
}

LLSortedPosInt  operator- (const LLSortedPosInt& l1,
    const LLSortedPosInt& l2) {
    // copy l1 and remove all of l2 from l1, taking care to
    // reclaim any storage -- do not to remove the sentinal Node
    LLSortedPosInt diff(l1);

    NodePtr nph = diff.head->next;
    NodePtr npl = l2.head->next;

    while (npl != NULL) {
        nph = diff.head->next;
        //Nested while loops to account for the fact lists can have different sizes && numbers ex.
        // (1,1,1,1,1,1,2) -l2
        // (1,2,3,4,5,6)   -l1 without the while loop would return (2,3,4,5,6)
        while (nph != NULL) {
            if (nph->key == npl->key) {
                nph = nph->next;
                diff.remove(npl->key);
            }
            else {
                nph = nph->next;
            }
        }
        npl = npl->next;
    }
    return diff;
}

// The following helper functions are provide to assist you in
// building the class--these helper functions are useful in
// several places among the functions you will write--take time
// to learn what they do

// insert() inserts an element in the linked list in sorted order
void LLSortedPosInt::insert(int key) {

    // setup pointers to walk the list
    NodePtr npp = head;
    NodePtr npc = head->next;

    // walk the list, searching until the given key value is exceeded
    while (npc != NULL && npc->key <= key) {
        npp = npc;
        npc = npc->next;
    }

    // insert the new value into the list
    npp->next = createNode(key, npc);
}

// remove() removes an element from the list (if it is present)
void LLSortedPosInt::remove(int key) {

    // negative values should not be stored in the list
    if (key <= 0) {
        return;
    }

    // setup pointers to walk the list
    NodePtr npp = head;
    NodePtr npc = head->next;

    // search the list until the end (if necessary)
    while (npc != NULL) {

        // if the key value is found, then splice this Node from the list and
        // reclaim its storage
        if (npc->key == key) {
            npp->next = npc->next;
            delete npc;
            break;
        }

        // walk the pointers to the next Node
        npp = npc;
        npc = npc->next;
    }
}
