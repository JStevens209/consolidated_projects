#include <iostream>

using namespace std;

int main() {

	string getname = "";
	char name[6] = { 'h','e','l','l','o','\0' };

	getname = name;
	cout << getname << endl;

}