
#include "memory_functions_jsteven.h"

using namespace std;

void initMemory_jsteven(ComputerMemory &memory) {
   memory.mode        =  1;
   memory.hitRow      = -1;
   memory.hitCol      = -1;
   memory.hitShip     =  NONE;
   memory.fireDir     =  NONE;
   memory.fireDist    =  1;
   memory.lastResult  =  NONE;
   memory.depth = 0;

   for (int i = 0; i < BOARDSIZE; i++) {
      for (int j = 0; j < BOARDSIZE; j++) {
         memory.grid[i][j] = EMPTY_MARKER;
      }
   }
}

string smartMove_jsteven(const ComputerMemory &memory) {


    int  mode = memory.mode;
	string move;
	const string ROW[10] = {"A","B","C","D","E","F","G","H","I","J"};
  const string COL[10] = {"1","2","3","4","5","6","7","8","9","10"};
  int direction[4] = {1,-1,1,-1};

	if(memory.mode == 1){
		move = randomMove();
	}
	if(memory.mode == 2){

    for(int i = 0; i < 3; i++){
      if(memory.grid[memory.hitRows[memory.depth] + direction[memory.fireDirs[memory.depth]]][memory.hitCols[memory.depth]] == EMPTY_MARKER){

        move = ROW[((memory.hitRows[memory.depth] + direction[memory.fireDirs[memory.depth]])) ] + COL[(memory.hitCols[memory.depth]) ];

      }
      else if(memory.grid[memory.hitRows[memory.depth]][memory.hitCols[memory.depth] + direction[memory.fireDirs[memory.depth]]] == EMPTY_MARKER){

        move = ROW[(memory.hitRows[memory.depth]) ] + COL[((memory.hitCols[memory.depth]) + direction[memory.fireDirs[memory.depth]]) ];

      }
    }
	}
	if(memory.mode == 3){
	     move = randomMove();
     }
   return move;
}

void updateMemory_jsteven(int row, int col, int result, ComputerMemory &memory) {


  int j = 0;
  int ship[5] = {};
  static int staticMode;


	if(isAMiss(result)){
		   memory.lastResult = 0;
       memory.grid[row][col] = MISS_MARKER;
  }
	if(isAHit(result)){

    ship[j] = isShip(result);
    if((j != 0) && (ship[j] == ship[j-1])){
      staticMode = 3;
      memory.grid[row][col] = HIT_MARKER;
    }
    if(ship[j] != ship[j-1]){
      memory.depth = (memory.depth % 4) + 1;
      staticMode = 2;
	    memory.lastResult = 8;
	    memory.hitRows[memory.depth] = row;
      memory.hitCols[memory.depth] = col;
      memory.fireDirs[memory.depth] = (memory.fireDirs[memory.depth] % 3) + 1;
      j++;
      if(j == 5){
        j = 0;
      }
    }
	}
  if((isASunk(result)) &&( memory.depth == 1)){
    staticMode = 1;
    memory.depth--;
  }
  else if((isASunk(result)) && (j > 1)){
     memory.depth--;
     staticMode = 2;
    }

 if(staticMode != 0){
    memory.mode = staticMode;
  }
  else {
    memory.mode = 1;
  }
}
