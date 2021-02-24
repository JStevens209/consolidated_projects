

// Author:  Keith Shomper
// Date:    24 Oct 03
// Purpose: Header file for implementing a text-based battleship game
// Updated: 14 Nov 08 to align class types with Cedarville standard
// Updated:  3 Apr 14 to use struct rather than class for the defined types
// Updated:  5 Nov 15 to introduce new functions to replace the ISAxxx macros
//           and also the SHIPNUM and DEBUGOUT macros

// include files for implementing battleship
#include <iostream>
#include <cstdlib>
#include <time.h>
#include <curses.h>
#include "kasbs.h"
#include <stdlib.h>

using namespace std;

// use these constants to indicate if the player is a human or a computer
// battleship board size is 10x10 grid
const   int   BOARDSIZE = 10;

// data structure for position
struct  Position {
   int  startRow;          // ship's initial row
   int  startCol;          // ship's initial column
   int  orient;            // indicates whether the ship is running across
                           // or up and down
};

// data structure for ship
struct  Ship {
   Position pos;            // where the ship is on the board
   int  size;               // number of hits required to sink the ship
   int  hitsToSink;         // number of hits remaining before the ship is sunk
   char marker;             // the ASCII marker used to denote the ship on the
                            // board
};

// a game board is made up of a 10x10 playing grid and the ships
struct  Board {
   char grid[BOARDSIZE][BOARDSIZE];
   Ship s[6];               // NOTE:  the first (zeroth) position is left empty
};

// use these constants for designating to which player we are referring
const   int   HUMAN          = 0;
const   int   COMPUTER       = 1;

// use these constants for deciding whether or not the user gave a proper move
const   int   VALID_MOVE     = 0;
const   int   ILLEGAL_FORMAT = 1;
const   int   REUSED_MOVE    = 2;

// functions for screen control and I/O
void    welcome(bool debug = false, bool pf = false);
void    clearTheLine(int x);
void    clearTheScreen(void);
void    pauseForEnter(void);
string  getResponse(int x, int y, string prompt);
void    writeMessage(int x, int y, string message);
void    writeResult(int x, int y, int result, int playerType);
void    displayBoard(int x, int y, int playerType, const Board &gameBoard);

// functions to control the board situation
void    initializeBoard(Board &gameBoard, bool file = false);
int     playMove(int row, int col, Board &gameBoard);

// function to tell what happened in the last play_move() command
bool    isAMiss(int playMoveResult);
bool    isAHit (int playMoveResult);
bool    isASunk(int playMoveResult);  // formerly named isItSunk()
int     isShip (int playMoveResult);

// misc game functions
string  randomMove(void);
int     checkMove(string move, const Board &gameBoard, int &row, int &col);
void    debug(string s, int x = 22, int y = 1);
string  numToString(int x);


// former function signatures
void    debug(int x, int y, string s);
bool    isItSunk(int playMoveResult);
