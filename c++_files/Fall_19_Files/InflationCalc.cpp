#include <iostream>

using namespace std;

double calcInflationRate( double oldPrice, double newPrice );
double calcFutureCost( double oldPrice, double newPrice );

int main()
{
	char yes = 'y';
	
	while (yes == 'y')
	{
		int priceOld;
		int priceNew;
	
		cout << "Enter last year's price: ";
		cin >> priceOld;

		cout << "Enter today's price: ";
	 	cin >> priceNew;
	
		cout << "The current inflation rate is " << calcInflationRate( priceOld, priceNew ) << "%" << endl;
		cout << "The estimated price in one year is $";

		int nextPrice = calcFutureCost( priceOld, priceNew );
		cout << nextPrice << endl;
	
		cout << "The estimated price in two years is $" << calcFutureCost( priceNew, nextPrice ) << endl;
	
		cout << "Would you like to continue this program?";
		cin >> yes;
	}
	

	return 0;
}

double calcInflationRate( double oldPrice, double newPrice ) {

	double inflationRate = ((( newPrice - oldPrice ) / oldPrice ) * 100 );
	return inflationRate;
}

double calcFutureCost( double oldPrice, double newPrice ) {

	double futureCost = ( newPrice + ( newPrice * ( calcInflationRate( oldPrice, newPrice ) / 100 )));
	return futureCost;
}