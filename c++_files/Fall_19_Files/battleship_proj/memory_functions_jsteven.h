#include <string>
#include "memory.h"

using namespace std;

void   initMemory_jsteven(ComputerMemory &memory);
void   updateMemory_jsteven(int row, int col, int result, ComputerMemory &memory);
string smartMove_jsteven(const ComputerMemory &memory);
