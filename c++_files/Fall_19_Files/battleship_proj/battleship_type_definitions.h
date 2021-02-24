// Author:  Keith Shomper
// Date:    24 Oct 03
// Purpose: Type definitions for implementing a text-based battleship game
// Modified:15 Nov 2005 - Moved the class definitions into the file battleship.h
//                        to make the data structure more visible.
// Modified: 5 Nov 2013 - Moved the ISA macros higher in the file to make them
//                        more visible.  Added ISAMISS macro
// Modified: 5 Nov 2015 - Moved the ISA macros back to a lower section and made
//                        them conditionally compilable.  The purpose of this
//                        change was to promote their replacement by like-named
//                        functions, while maintaining backward compatibility.

// use these constants to indicate whether a ship goes across the grid or up
// and down

#ifndef BATTLESHIP_TYPE_DEFINITIONS_H
#define BATTLESHIP_TYPE_DEFINITIONS_H

const   int   HORZ           = 0;
const   int   VERT           = 1;

// these constants allow use to refer to the ships by numerical values
const   int   AC             = 1;
const   int   BS             = 2;
const   int   CR             = 3;
const   int   SB             = 4;
const   int   DS             = 5;

// constants for the ship size
const   int   AC_SIZE        = 5;
const   int   BS_SIZE        = 4;
const   int   CR_SIZE        = 3;
const   int   SB_SIZE        = 3;
const   int   DS_SIZE        = 2;
 
// markers for keeping track of game play
const   char  HIT_MARKER     = 'H';
const   char  MISS_MARKER    = '*';
const   char  SUNK_MARKER    = 'X';
const   char  EMPTY_MARKER   = ' ';
const   char  AC_MARKER      = 'A';
const   char  BS_MARKER      = 'B';
const   char  CR_MARKER      = 'C';
const   char  SB_MARKER      = 'S';
const   char  DS_MARKER      = 'D';
 
// TO STUDENTS:  It should not be necessary in your assignment for you to use 
// the information appearing below this comment

// color constants for diferent game situations
const   int   BATTLE_WHITE   = 1;
const   int   BATTLE_GREEN   = 2;
const   int   BATTLE_YELLOW  = 3;
const   int   BATTLE_RED     = 4;
 
// use these constants to set the return value in playMove(), they allow us
// to send back mutiple pieces of information about the result of the move in
// a single integer variable
const   int   MISS           = 0;
const   int   SHIP           = 7;
const   int   HIT            = 8;
const   int   SUNK           = 16;

#ifdef  BATTLESHIP_BACKWARD_COMPATIBILITY
// these macros use the MISS, HIT, etc. constants below to determine the 
// result of the move
#define ISAMISS(parm) (!((parm) & HIT))
#define ISAHIT(parm)  ((parm) & HIT)
#define ISASUNK(parm) ((parm) & SUNK)
#define SHIPNUM(parm) ((parm) & SHIP)
#endif // BATTLESHIP_BACKWARD_COMPATIBILITY

#endif // BATTLESHIP_TYPE_DEFINITIONS_H
