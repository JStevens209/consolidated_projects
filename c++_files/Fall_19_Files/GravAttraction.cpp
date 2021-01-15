#include <iostream>
#include <cmath>

using namespace std;

double CalcGravAttraction(double m1, double m2, double d);

int main ()
{
	char notDone = 'y';

	while( notDone == 'y')
	{	double m1; //mass one
		double m2; //mass two
		double d;  //distance

		cout << "Enter the mass (g) of the first object: ";
		cin >> m1;

		cout << "Enter the mass (g) of the second object: ";
		cin >> m2;

		cout << "Enter the distance (cm) between the two objects: ";
		cin >> d;

		cout << "The gravitational force is " << CalcGravAttraction(m1, m2, d) << "dynes." << endl; 
				
		cout << "Would you like to repeat this program?";
		cin >> notDone;
	}


	return 0;
}

double CalcGravAttraction(double m1, double m2, double d)
{
	//gravitational constant
	const double G = 6.673e-8; 

	//Equation for gravitational force
	double gForce = ( G * m1 * m2 ) / ( pow( d, 2.0 ) ); 

	return gForce;
}

}