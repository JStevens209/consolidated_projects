// An example to demonstrate
// 1. Big three functions: copy constructor, assignment operator and destructor
// 2. The aliasing which often occurs in default copy and assignment when 
//    pointers are present, causing memory errors: shallow copy, double free,
//    access after release, and memory leaks
// 3. Troubleshooting memory errors with the debugger
// 4. Making memory errors visible with Visual Leak Dectector

#include <iostream>
#include <cstring>
#include <cstdio>
//#include <vld.h>
using namespace std;

class BigThreeString {
public:
    BigThreeString(const char* str = "") {
        cerr << "BigThreeString default constructor called\n";

        // get the length of the input string to store in this class
        len = strlen(str);

        // allocate memory to store the string - add one for the NULL character
        s = new char[len + 1];

        // store the string in the class
        strcpy(s, str);

        // print the newly created BigThreeString
        Print("Finished default construction");
    }
    BigThreeString(const BigThreeString& rhs) {                     //Copy Constructor
        cerr << "BigThreeString copy constructor called\n";

        // the default copy constructor behavior
        /*/
        s = rhs.s;
        len = rhs.len;
        // print the newly assigned BigThreeString
        Print("Finished copy construction");
        return;
        /**/

        // the proper copy construction behavior when classes contain pointers
        // pointers often reference dynamically-allocated memory which needs
        // deep copied:
        //   2. allocate new memory, 
        //   3. deep copy the source (src) into the destination (dest)
        /* 1. delete [] s; */
        /* 2. */ s = new char[strlen(rhs.s) + 1]; 
        /* 3. */ SetData(rhs.s);
        // print the newly constructed BigThreeString
        Print("Finished copy construction");
    }
    BigThreeString& operator=(const BigThreeString& rhs) {
        cerr << "BigThreeString assignment operator called\n";

        // the default assignment behavior
        /*/
        s = rhs.s;
        len = rhs.len;
        // print the newly assigned BigThreeString
        Print("Finished assignment");
        return *this;
        /**/

        // the proper assignment behavior when classes contain pointers
        if (this != &rhs) {
            // pointers often reference dynamically-allocated memory which needs
            // to be reclaimed before reassignment -- the tasks are:
            //   1. release old memory, 
            //   2. allocate new memory, 
            //   3. deep copy the source (src) into the destination (dest)
            /* 1. */ delete[] s;
            /* 2. */ s = new char[strlen(rhs.s) + 1];
            /* 3. */ SetData(rhs.s);
        }
        // print the newly assigned BigThreeString
        Print("Finished assignment");
        return *this;
    }
    ~BigThreeString() {
        // the default destructor is a stub
        /**/
        cerr << "BigThreeString destructor called\n";
       // return;
        /**/

        // a proper destructor ensures any allocated memory/objects are released
        delete[] s; //Causes heap corruption, beacause when two pointers are aliases, and one the space one is pointing to gets deleted
                    //Then when the OS tries to delete the space the other is pointing to, it has already been deleted.
    }
    void SetData(const char* str) {
        //Checks if we need to reallocate
        if (strlen(str) > strlen(s)) {
            delete[] s;
            s = new char[strlen(str) + 1];
        }
        strcpy(s, str);
        len = strlen(s);
    }
    void Print(const char* msg) {
        printf("%s: s = \"%s\", len = %d\n", msg, s, len);
    }
private:
    char* s;
    int   len;
};

int main(int argc, char** argv) {

    BigThreeString s1("Apple");
    BigThreeString s2("Banana");
    BigThreeString s3(s1);
    BigThreeString s4;
    s4 = s2;

    //Pointer Aliasing, when you set the pointers, it still points to the same location im memory
    s3.SetData("Cherry");
    s4.SetData("Date");

    s1.Print("s1:");
    s2.Print("s2:");
    s3.Print("s3:");
    s4.Print("s4:");

    //deallocation
    //delete [] s; //did you allocate with [] or without?
    //delete s;

    return 0;
}
