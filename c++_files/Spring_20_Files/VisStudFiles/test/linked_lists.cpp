//Shomper's notes on linked lists
// Purpose:  To demonstrate how *not* to insert into a linked list.  This code
//           contains errors
// Author:   Keith Shomper
// Date:     25 Jan 2006
/*
#include <iostream>

using namespace std;

class   Node;

typedef Node* NodePtr;

class   Node {
public:
    int     key;
    NodePtr next;
};

int main() {
    NodePtr head = NULL;
    NodePtr p = NULL;
    int     val;

    // create and give an intial value to the first Node in the list
    head = new Node;
    p = head; //Sets p to be THE EXACT SAME as head, NOT pointing to head.
    p->key = 2;
    p->next = NULL;

    // add another four Nodes to the list
    for (int i = 1; i < 5; i++) {
        p->next = new Node;
        p = p->next;
        p->key = (i + 1) * 2;
        p->next = NULL;
    }

    // insert a final Node in the list
    cout << "Please enter a value to insert into the list:  ";
    cin >> val;

    // find the insertion point
    p = head;
    while (p->next->key < val) {
        p = p->next;

    }

    // insert the Node
    p->next = new Node;
    p = p->next;
    p->key = val;

    return 0;
}*/
