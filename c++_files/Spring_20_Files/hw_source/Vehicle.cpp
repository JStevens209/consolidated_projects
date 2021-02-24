#include "Vehicle.h"
#include <cstring>

using namespace std;

//Initilization of static variable out
ostream* Vehicle::out = &cout;

//Constructor that takes a single String input
Vehicle::Vehicle(string vehicleName) {
	//If given an empty string, make name NULL;
	if (vehicleName == "") {
		name = NULL;
		return;
	}
	name = new char[vehicleName.length() + 1];
	strcpy(name, vehicleName.c_str());
}

//Deep copy constructor
Vehicle::Vehicle(const Vehicle& l) {
	//Assigns space of size l.name, then copys the data from one cstring to another
	name = new char[strlen(l.name)];
	strcpy(name, l.name);
}

//Destructor
Vehicle::~Vehicle() {
	//deletes the space assigned to name.
	delete[] name;
	name = NULL;
}

//Operator =
Vehicle& Vehicle::operator=(const Vehicle& l) {
	//Handles self assignment
	if (l.name == name) {
		return *this;
	}
	//destructs initialized name then performs deep copy
	delete[] name;
	name = new char[strlen(l.name)];
	strcpy(name, l.name);

	return *this;
}

//Output Operator <<
ostream& operator<<(ostream& out, Vehicle& l) {
	out << l.name;
	return out;
}
