// This example demonstrates the STL list container using a integers which are 
// kept in the list.  The STL list operations demonstrated here are:
//     =, push_back(), push_front(), size(), erase(), and sort()
//
// Iterators are also demonstrated

/*#include <iostream>
#include <list>

using namespace std;

// use typedefs to make the type names for the template objects syntactically
// simpler
using MyList       = list<int>;
using ListIterator = list<int>::iterator;
//typedef list<int>           MyList;
//typedef list<int>::iterator ListIterator;

//typedef declaration alt name
//alias declaration:
// using alt-def = decl.

// test program
int main() {
    MyList       list1, list2;
    int          values[] = { 4, 2, 1, 3 };
    int          val, valFirst, valLast;
    int          i;
    ListIterator li1;

    // alternately insert integers on both the front an back of the list
    for (i = 0; i < 4; i++) {
        list1.push_back(values[i]);
    }

    cout << "There are " << list1.size() << " elements in list1:  " << endl;

    // use the iterator to "walk" the list and print the elements
    i = 1;
    for (li1 = list1.begin(); li1 != list1.end(); li1++) {
        cout << "\tElement " << i << ":  " << *li1 << endl;
        i++;
    }

    // make a copy of list1
    list2 = list1;

    cout << "\nThere are " << list2.size() << " elements in list2:  " << endl;

    // use the iterator to "walk" the list and print the elements
    i = 1;
    for (auto li2 = list2.begin(); li2 != list2.end(); li2++) {
        cout << "\tElement " << i << ":  " << *li2 << endl;
        i++;
    }

    cout << "\nBefore sort:  list1 is "
        << ((list1 == list2) ? "" : "not ") << "equal to list2\n";

    list2.sort();

    cout << "After sort: list1 is "
        << ((list1 != list2) ? "not " : "") << "equal to list2\n";

    cout << "\nThere are " << list2.size() << " elements in list2:  " << endl;

    // use an implicit iterator to "walk" the list and print the elements
    i = 1;
    for (auto li3 : list2) {
        cout << "\tElement " << i << ":  " << li3 << endl;
        i++;
    }

    // back up to the element that should be first, and get a copy, then erase it
    auto li4 = list1.end();
    li4--;
    li4--;
    valFirst = *li4;
    list1.erase(li4);

    // get a copy of the front element, erase it, and put it at the end where it
    // belongs.
    valLast = list1.front();
    list1.erase(list1.begin());
    list1.push_back(valLast);

    // now put the element the should be first on the list
    list1.push_front(valFirst);

    cout << "\nThere are " << list1.size() << " elements in list1:  " << endl;
    i = 1;
    for (auto li5 : list1) {
        cout << "\tElement " << i << ":  " << li5 << endl;
        i++;
    }

    return 0;
}*/
