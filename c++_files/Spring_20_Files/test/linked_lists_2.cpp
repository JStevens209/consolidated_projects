// Purpose:  To fix the former example's insertion problem into a linked list.
//           This code still contains errors
// Author:   Keith Shomper
// Date:     25 Jan 2006

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
    NodePtr newNode = NULL;
    int     val;

    // create and give an intial value to the first Node in the list
    head = new Node;
    p = head;
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
    newNode = new Node;   // formerly was:  p->next = new Node;
    newNode->key = val;
    newNode->next = p->next;
    p->next = newNode;

    return 0;
}