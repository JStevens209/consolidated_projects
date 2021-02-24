#pragma once
#include "MotorVehicle.h"

using namespace std;

class Car : public MotorVehicle {
public:
	//Constructors
	Car(string carName = "", string carMake = "", string carModel = "", string carTrim = "", double carMPG = 0.0);

	//Accessor + Mutator
	string getTrim();
	void setTrim(string carTrim);

	//member functions
	void print() const override;
	void read()  override;

private:
	string trim;

};