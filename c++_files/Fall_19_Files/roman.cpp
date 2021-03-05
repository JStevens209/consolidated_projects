//Joshua Stevens
//To convert dates to Roman numerals
//Sept 14, 2019

#include <iostream>
#include <cctype>

using namespace std;

int main ()
{	char cont = 'y';
	while ( cont == 'y')
	{
		int intYear;
		cout << "Please enter a year between 1 and 3000:";
		cin >> intYear;
		cout << "The year " << intYear << "AD is the Roman numeral ";

		int thousands = intYear / 1000;
		for (int i = thousands; i >= 1; --i)	//thousands place
		{
			cout << "M";
		}

		intYear = intYear - (thousands * 1000);
		if (intYear >= 900)		//five hundreds
		{
			cout << "CM";
			intYear -= 900;
		}
		else if (intYear >=500)
		{
			cout << "D";
			intYear -= 500;
		}


		int hundreds = (intYear/100);
		for (int i = hundreds; i >= 1 && i != 4; --i)	//hundreds
		{
			cout << "C";
		}
		if (hundreds == 4)
		{
			cout << "CD";
		}
		intYear = (intYear - (hundreds * 100));


		if (intYear >= 90)	//fifties
		{
			cout << "XC";
			intYear -= 90;
		}
		else if (intYear >=50)
		{
			cout << "L";
			intYear -= 50;
		}


		int tens = (intYear/10);
		for (int i = tens; (i >= 1) && (i != 4); --i)	//tens
		{
			cout << "X";
		}
		if (tens == 4)
		{
			cout << "XL";
		}

		intYear -= (tens * 10);


		if (intYear >= 9)	//fives
		{
			cout << "IX";
			intYear -= 9;
		}
		else if (intYear >=5)
		{
			cout << "V";
			intYear -= 5;
		}


		for (int i = intYear; (i > 0) && (i < 4); --i)	//ones
		{
			cout << "I";
		}
		if (intYear == 4)
		{
			cout << "IV";
		}

		cout << endl << "Would you like to repeat this program? ";
		cin >> cont;


	}


}
