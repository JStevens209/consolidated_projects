#pragma once
#include "Vehicle.h"

using namespace std;

class MotorVehicle : public Vehicle {
public:
	//Constructors
	MotorVehicle(string vehicleName = "", string vehicleMake = "", string vehicleModel = "", double vehicleMPG = 0.0);

	//Getter
	string getName()  const;
	string getMake()  const;
	string getModel() const;
	double getMPG()   const;
	ostream* getOut()  const;

	//Mutators
	void setName(string vehicleName);
	void setMake(string vehicleMake);
	void setModel(string vehicleModel);
	void setMPG(double vehicleMPG);
	void setOut(ostream &os);

	//Other Functions
	virtual void print() const;
	virtual void read();

private:
	string make;
	string model;
	double mpg;

};
