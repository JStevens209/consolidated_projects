#pragma once
#include <iostream>

using namespace std;

class Vehicle {
public:
	//Constructors
	Vehicle(string vehicleName = "");
	Vehicle(const Vehicle& l);

	//Destructor
	~Vehicle();

	//Operator =
	Vehicle& operator=(const Vehicle& l);

	//Output Operator
	friend ostream& operator<<(ostream& out, Vehicle &l);

	//Member Functions
	virtual void print() const = 0;
	virtual void read() = 0;

protected:
	char* name;
	static ostream* out;
}; 