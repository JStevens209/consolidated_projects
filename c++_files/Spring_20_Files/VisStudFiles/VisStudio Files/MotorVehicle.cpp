#include <string>
#include <cstring>
#include "MotorVehicle.h"


//Constructor
MotorVehicle::MotorVehicle(string vehicleName, string vehicleMake, string vehicleModel, double vehicleMPG) : Vehicle(vehicleName) {
	make  = vehicleMake;
	model = vehicleModel;
	mpg   = vehicleMPG;
}

//Getters
string MotorVehicle::getName() const{
	//Assigns char* name to string getname, returns a string.
	string getName = name;
	return getName;
}

string MotorVehicle::getMake()  const {
	return make;
}

string MotorVehicle::getModel() const {
	return model;
}

double MotorVehicle::getMPG()   const {
	return mpg;
}

ostream* MotorVehicle::getOut() const {
	return out;
}

//Setters/Mutators
void MotorVehicle::setName(string vehicleName) {
	//Performs deep copy to name
	delete[] name;
	name = new char[vehicleName.length() + 1];
	strcpy(name, vehicleName.c_str());
}

void MotorVehicle::setMake(string vehicleMake) {
	make = vehicleMake;
}

void MotorVehicle::setModel(string vehicleModel) {
	model = vehicleModel;
}

void MotorVehicle::setMPG(double vehicleMPG) {
	mpg = vehicleMPG;
}

void MotorVehicle::setOut(ostream &os) {
	out = &os;
}

//outputs each variable to the ostream
void MotorVehicle::print() const {
	*out << endl << name << endl << endl << make << endl << model << endl << mpg;
}

//Takes input to initialize an an object
void MotorVehicle::read() {

	string vehicleName;
	string vehicleMPG;

	//Asks for data, then reads the data into "this"
	//Reads name as a string, then calls the setter
	cout << "Please enter the name of the vehicle: ";
	cin >> vehicleName;
	setName(vehicleName);

	cout << endl << "Please enter the vehicle's make: ";
	cin >> make;

	cout << endl << "Please enter the model of the vehicle: ";
	cin >> model;

	//Reads MPG as a string then converts to double
	cout << endl << "Please enter the miles per gallon of the vehicle: ";
	cin >> vehicleMPG;
	mpg = stod(vehicleMPG);
}
