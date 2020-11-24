#include "Car.h"

using namespace std;

//Constructor, calls MotorVehicle's constructor
Car::Car(string carName, string carMake, string carModel, string carTrim, double carMPG)
	:MotorVehicle(carName, carMake, carModel, carMPG) {
	trim = carTrim;
}

//Getter
string Car::getTrim() {
	return trim;
}

//Setter
void Car::setTrim(string carTrim) {
	trim = carTrim;
}

//Calls MotorVehicle::print then prints own variable to ostream
void Car::print() const {
	MotorVehicle::print();
	*out << endl << trim;
}

//Calls MotorVehicle::read then requests trim from user
void Car::read() {
	MotorVehicle::read();

	cout << endl << "Please enter the car's trim: ";
	cin >> trim;
}
