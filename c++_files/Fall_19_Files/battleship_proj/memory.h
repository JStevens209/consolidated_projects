#ifndef MEMORY_H
#define MEMORY_H

#include "battleship.h"

using namespace std;

#define RANDOM  1
#define SEARCH  2
#define DESTROY 3

#define NONE    0
#define NORTH   1
#define SOUTH   2
#define EAST    3
#define WEST    4

struct ComputerMemory
{
	int  hitRow, hitCol;
	int  hitShip;
	int  fireDir;
	int  fireDist;
	int  lastResult;
	int  mode;
	char grid[BOARDSIZE][BOARDSIZE];

	// optional attributes for students wanting to keep track of hits on
	// multiple ships
	int  depth;
	int  hitRows[5], hitCols[5];
	int  hitShips[5];
	int  fireDirs[5];
	int  fireDists[5];
	int  lastResults[5];
	int  modes[5];
};

#endif // MEMORY_H
