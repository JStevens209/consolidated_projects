{\rtf1\ansi\ansicpg1252\cocoartf1671\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #include <iostream>\
#include <cmath>\
\
using namespace std;\
\
	double CalcGravAttraction(double m1, double m2, double d);\
\
int main ()\
\{\
\
	char yes = 'y';\
	while( yes == 'y')\
	\{	double m1; //mass one\
		double m2; //mass two\
		double d;  //distance\
\
		cout << "Enter the mass (g) of the first object: ";\
		cin >> m1;\
\
		cout << "Enter the mass (g) of the second object: ";\
		cin >> m2;\
\
		cout << "Enter the distance (cm) between the two objects: ";\
		cin >> d;\
\
		cout << "The gravitational force is " << CalcGravAttraction(m1, m2, d) << "dynes." << endl; \
				\
		cout << "Would you like to repeat this program?";\
		cin >> yes;\
	\}\
\
\
	return 0;\
\}\
\
double CalcGravAttraction(double m1, double m2, double d)\
\{\
	const double G = 6.673e-8; //gravitational constant\
	\
	double gForce = (G * m1 * m2)/(pow(d,2.0)); //Equation for gravitational force\
\
	return gForce;\
\}\
\
}