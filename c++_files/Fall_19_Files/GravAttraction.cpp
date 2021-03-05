#include <iostream>
#include <cmath>

using namespace std;

double CalcGravAttraction( double mass_1, double mass_2, double distance );

int main() {
	char notDone = 'y';

	while( notDone == 'y') {

		double mass_1; 
		double mass_2;
		double distance;

		cout << "Enter the mass (g) of the first object: ";
		cin >> mass_1;

		cout << "Enter the mass (g) of the second object: ";
		cin >> mass_2;

		cout << "Enter the distance (cm) between the two objects: ";
		cin >> distance;

		cout << "The gravitational force is " << CalcGravAttraction(mass_1, mass_2, distance) << "dynes." << endl; 
				
		cout << "Would you like to repeat this program?";
		cin >> notDone;
	}

	return 0;
}

double CalcGravAttraction( double mass_1, double mass_2, double distance ) {

	//gravitational constant
	const double G = 6.673e-8; 

	//Equation for gravitational force
	return ( G * mass_1 * mass_2 ) / ( pow( distance, 2.0 ));
}
