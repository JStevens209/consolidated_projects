// Purpose:  Main program for testing Vehicle class hierarchy
// Author:   Dr Keith A. Shomper
// Date:     17 Mar 2006
// Modified:  1 Apr 2013
// Modified: 18 Mar 2015 - Added code to free objects allocated by the main 
//                         program, so Dr Memory would give a "clean" run
// Modified: 16 Mar 2020 - Edited header files for capitalization

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <typeinfo>
#include "MotorVehicle.h"

// Car.h and Truck.h included twice to test inclusion guards
#include "Car.h"
#include "Car.h"
#include "Truck.h"
#include "Truck.h"

typedef vector<MotorVehicle*> vectorOfMotorVehicle;

using namespace std;

// prompt the user for the Vehicle type to create, and get the reply
string prompt(void);

int main() {
    vectorOfMotorVehicle v;         // store dynamically created MotorVehicles
                                    // or objects derived from MotorVehicles
    int           numVehicles = 0;  // denotes how many MotorVehicles we have
    string        reply;            // indicates type of MotorVehicle to build
    bool          error = false;    // set when a user response is in error
    string        outputLocation;   // where the output of print() will go
    ofstream* out = NULL;
    MotorVehicle* m;

    // uncomment following line to test that Vehicle is an abstract base class
    // Vehicle theVehicle;

    // push a Vehicle into the vector so  first "real" Vehicle is at position 1
    m = new MotorVehicle("None");
    v.push_back(m);

    // chose where the output will go
    cout << "Where would you like the output?  ";
    cin >> outputLocation;

    if (outputLocation == "stdout") {
        ; // no action to take, because stdout (i.e., cout) is the default
    }
    else if (outputLocation == "stderr") {
        v[0]->setOut(cerr);
    }
    else {
        out = new ofstream;
        out->open(outputLocation.c_str());
        if (out->fail()) {
            cerr << "Error:  error writing to " << outputLocation << endl;
            return 1;
        }
        v[0]->setOut(*out);
    }

    // get the type of Vehicle to create
    reply = prompt();

    // loop, reading vehicle descriptions, until a "quit" command is received
    while (reply != "quit") {

        // create the new MotorVehicle object and push it into the vector
        switch (toupper(reply[0])) {
        case 'T': m = (MotorVehicle*)(new Truck);
            v.push_back(m);
            break;
        case 'C': m = (MotorVehicle*)(new Car);
            v.push_back(m);
            break;
        case 'Q': reply = "quit";
            continue;
        default: cerr << "Incorrect response\n\n";
            error = true;
        }

        // if no error, then we have a new Vehicle to initialize via read()
        if (!error) {
            numVehicles++;
            v[numVehicles]->read();
        }

        // reset error flag, and request a new Vehicle type
        error = false;
        reply = prompt();
    }

    // report on what Vehicles were created to test read() and print()
    for (int i = 0; i <= numVehicles; i++) {
        *out << "Vehicle " << i << endl;

        // print the Vehicle characteristics (attributes)
        v[i]->print();

        *out << endl;

        // free the storage for this Vehicle
        delete v[i];
    }

    // if we opened an output file, then close it
    if (out != NULL) {
        out->close();
        delete out;
    }

    return 0;
}

// prompt the user for the Vehicle type to create, and get the reply
string prompt() {
    string reply;    // the user reponse to the prompt

    // prompt for and get user response
    cout << "\nWhich type of vehicle would you like to initialize"
        << "\n--car or truck (or \"quit\" to exit):  ";
    cin >> reply;

    return reply;
}
