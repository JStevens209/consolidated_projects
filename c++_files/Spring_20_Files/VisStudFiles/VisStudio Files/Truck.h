#pragma once
#include "MotorVehicle.h"

using namespace std;

class Truck : public MotorVehicle {
public:
	//Constructor
	Truck(string truckName = "", string truckMake = "", string truckModel = "", double truckCapacity = 0.0, double truckMPG = 0.0);

	//Accessor + Mutator
	double getCapacity();
	void   setCapacity(double truckCapacity);

	//Member functions
	void print() const override;
	void read() override;

private:
	double cargoCapacity;
}; 