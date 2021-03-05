// Very beginning stages of an ambitious project I had when first starting out. 
// Abandoned.

#include <iostream>
#include <cstdlib>

using namespace std;

string Standardize(string input);
int EnemyOneFight(int health, int weaponDMG);


int main ()
{
	srand(time(0));

	string response;

	int health = 100;
	int weaponDMG = 20;


	cout << "What do you want to do? Fight/Run" << endl;
	cin >> response;
	response = Standardize(response);

	if(response == "FIGHT")
	{
		EnemyOneFight(health, weaponDMG);
	}

	cout << endl;
	return 0;


}

string Standardize(string input)
{
	for(int i = 0; i < input.length(); i++)
		{
			input[i]=toupper(input[i]);
		}
	return input;
}
//end int main()

int EnemyOneFight(int health, int weaponDMG)
{
	int enemyOneHP = 100;
	int enemyOneDMG = 10;

	string response;

	srand(time(0));

	while((enemyOneHP > 0) && (health > 0))
	{
		int chance = (rand() % 100);

		cout << "Strike or Run?" << endl;
		cin >> response;
		response = Standardize(response);

		if(response == "STRIKE")
		{
			if(chance < 75)
			{
				enemyOneHP -= weaponDMG;
			}
		}

		if(response == "RUN")
		{

			if(chance <= 10)
			{
				cout << "You trip, enemy gets a free hit." << endl;
				health -= enemyOneDMG;
			}
			if(chance > 10)
			{
				cout << "You successfully run away" << endl;
				return health;
			}
		}
		cout << "Enemy is at " << enemyOneHP << " hitpoints." << endl;
		if(chance < 50)
		{
			cout << "Enemy has successfully struck you!" << endl;
			health -= enemyOneDMG;
		}
	}


	if(enemyOneHP == 0)
	{
		cout << "You win! With " << health << " HP." << endl;
		return health;
	}
	if(health == 0)
	{
	 	cout << "You have died." << endl;
		return 0;
	}
	else
	{
		cout << "Error: Health underflow" << endl;
		return 1;
	}
}
