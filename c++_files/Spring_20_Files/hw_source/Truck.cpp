#include "Truck.h"

using namespace std;

//Default Constructor, Calls MotorVehicle default constructor
Truck::Truck(string truckName, string truckMake, string truckModel, double truckCapacity, double truckMPG)
	:MotorVehicle(truckName, truckMake, truckModel, truckMPG) {
	cargoCapacity = truckCapacity;
}

//Getter
double Truck::getCapacity() {
	return cargoCapacity;
}

//Setter
void Truck::setCapacity(double truckCapacity) {
	cargoCapacity = truckCapacity;
}

//Calls MotorVehicle::print then outputs its own variable to ostream
void Truck::print() const {
	MotorVehicle::print();
	*out << endl << cargoCapacity;
}

//Calls MotorVehicle::read then requests cargoCapacity from user
void Truck::read() {
	MotorVehicle::read();

	cout << endl << "Please enter your truck's cargo capacity: ";
	cin >> cargoCapacity;
}
