// Author:  Keith A. Shomper
// Date:    2/11/14
// Purpose: To test a simple, sorted linked-list of positive
//          integers

#include <iostream>
#include <string>
#include <cstring>
#include <algorithm>
#include "LLSortedPosInt.h"



using namespace std;

#define NUM_LISTS 5

void showMenu();
int  rangeCorrect(int);

typedef LLSortedPosInt LL;

int main(int argc, char** argv) {
    if (argc > 2) {
        cout << "Usage:  testLL [NoMenu]\n";
        return 0;
    }

    bool noMenu = true;

    if (argc == 2 && strcmp(argv[1], "NoMenu") == 0) {
        noMenu = true;
    }

    // an array of six integers to test the array constructor
    int            a[] = { 3, 5, -6, 2, 8, 4, 6};
    int            b[] = { 3, 5, -6, 2, 7, 4, 7};
    // test default constructor by initializing NUMLIST default lists
    LLSortedPosInt l[NUM_LISTS] ;

    // test other constructors
    LL testOutput;
    LLSortedPosInt singletonList(2);
    LL otherList(3);
    LLSortedPosInt arrayBuiltList(a, 7);
    LL testArray(b, 7);

    //singletonList.isEmpty();
    //arrayBuiltList.containsElement(10);
    //LL copyArray(arrayBuiltList);
    //arrayBuiltList.~LLSortedPosInt();
    //copyArray == arrayBuiltList;
    //otherList = singletonList + otherList;
    //copyArray == testArray;
    //copyArray = testArray;
    //testArray = testArray - copyArray;
    //cout << testOutput << " " << otherList << " " << testArray << endl;
    //{
        // test copy constructors
        //LLSortedPosInt copiedList(arrayBuiltList);

        // test destructor when copiedList goes out of scope
    //}

    //  test assignment for various kinds of lists: i.e., empty, singleton, etc.
    l[1] = l[0];
    l[2] = singletonList;
    l[3] = arrayBuiltList;
    l[4] = l[3];

    // variables to test our implementation
    int              i, k, lnum;
    char             cmd;

    // try various linked-list functions, until q is typed
    do {
        if (!noMenu) showMenu();
        cin >> cmd;

        switch (cmd) {

            // print a list
        case 'p': cin >> lnum;
            cout << "List[" << lnum << "]:  ";
            lnum = rangeCorrect(lnum);
            cout << l[lnum] << endl;
            break;

            // print all lists
        case 'P': for (i = 0; i < NUM_LISTS; i++) {
            cout << "List[" << i << "]:  ";
            cout << l[i] << endl;
        }
                break;

                // insert an element into a list
        case 'i': cin >> i >> lnum;
            lnum = rangeCorrect(lnum);
            cout << "Inserting " << i << " into list[" << lnum << "]\n";
            l[lnum] = l[lnum] + i;
            break;

            // remove an element from a list
        case 'r': cin >> i >> lnum;
            lnum = rangeCorrect(lnum);
            cout << "Removing " << i << " from list[" << lnum << "]\n";
            l[lnum] = l[lnum] - i;
            break;

            // assign one list to another
        case 'a': cin >> i >> lnum;
            i = rangeCorrect(i);
            lnum = rangeCorrect(lnum);
            cout << "Assigning list[" << i << "] to list[" << lnum
                << "]\n";
            l[lnum] = l[i];
            break;

            // merge two lists together
        case 'm': cin >> i >> k >> lnum;
            i = rangeCorrect(i);
            k = rangeCorrect(k);
            lnum = rangeCorrect(lnum);
            cout << "Merging list[" << i << "] and list[" << k
                << "] as list[" << lnum << "]\n";
            l[lnum] = l[i] + l[k];
            break;

            // subtract one list from another
        case 's': cin >> i >> k >> lnum;
            i = rangeCorrect(i);
            k = rangeCorrect(k);
            lnum = rangeCorrect(lnum);
            cout << "Subtracting list[" << k << "] from list[" << i
                << "] as list[" << lnum << "]\n";
            l[lnum] = l[i] - l[k];
            break;

            // test if the list is empty
        case 'y': cin >> lnum;
            lnum = rangeCorrect(lnum);
            if (l[lnum].isEmpty()) {
                cout << "List[" << lnum << "] is empty\n";
            }
            else {
                cout << "List[" << lnum
                    << "] is not empty\n";
            }
            break;

            // test if the list as a certain element
        case 'c': cin >> i >> lnum;
            lnum = rangeCorrect(lnum);
            if (l[lnum].containsElement(i)) {
                cout << "List[" << lnum << "] contains "
                    << i << "\n";
            }
            else {
                cout << "List[" << lnum
                    << "] does not contain " << i << "\n";
            }
            break;

            // test two lists for equality
        case 'e': cin >> i >> lnum;
            i = rangeCorrect(i);
            lnum = rangeCorrect(lnum);
            if (l[i] == l[lnum]) {
                cout << "List[" << i
                    << "] is identical to list ["
                    << lnum << "]\n";
            }
            else {
                cout << "List[" << i
                    << "] is different from list ["
                    << lnum << "]\n";
            }
            break;

            // test two lists for inequality
        case 'n': cin >> i >> lnum;
            i = rangeCorrect(i);
            lnum = rangeCorrect(lnum);
            if (l[i] != l[lnum]) {
                cout << "List[" << i
                    << "] is different from list ["
                    << lnum << "]\n";
            }
            else {
                cout << "List[" << i
                    << "] is identical to list ["
                    << lnum << "]\n";
            }
            break;

            // quit the program
        case 'q': break;

            // any other leading letter is considered a comment
        default: {
            string dummy;
            getline(cin, dummy);
        }
               break;
        }
    } while (cmd != 'q');

    return 0;
}

// display the menu of choices
void showMenu() {
    cout << "This program tests the linked list implementation\n";
    cout << "Use the following single-letter commands to test:\n";
    cout << "  e # #      - compare two lists          ";
    cout << "n # #      - compare lists (not equal)\n";
    cout << "  p #        - print list #               ";
    cout << "P          - print all lists\n";
    cout << "  i #1 #2    - insert elem 1 into list 2  ";
    cout << "r #1 #2    - remove elem 1 from list 2\n";
    cout << "  s #1 #2 #3 - subtract list 2 frm 1 to 3 ";
    cout << "m #1 #2 #3 - merge list 1 & 2 into 3\n";
    cout << "  y #        - ask if list # is empty     ";
    cout << "c #1 #2    - ask is elem 1 in list 2\n";
    cout << "  a #1 #2    - assign list 1 to list 2    ";
    cout << "q          - quit the test program\n\n";
    cout << "Command:  ";
}

int  rangeCorrect(int n) {
    if (n < 0 || n > NUM_LISTS - 1) {
        cout << "rangeCorrect error:  list index " << n
            << " is outside range 0 to " << NUM_LISTS - 1 << endl;
    }

    return max(0, min(NUM_LISTS - 1, n));
}
