// Author:Joshua Stevens
// Date:
// Purpose:Battleship Game

#include "battleship.h"


int main() {

	// variable declarations (you'll need others, of course)

	bool done = false;
	const int NUMTOSINK = 5;	//declared as a const to help with testing purposes.

	Board humanBoard;
	Board compBoard;

	string move;
	string compMove;
	int testMove;


	int row;
	int col;
	int row2;
	int col2;

	bool humValid = false;
	bool compValid = false;

	int result;
	int compResult;
	int sunk = 0;
	int compSunk = 0;
	// Welcome the player to the game

	welcome();	//You're welcome

	// Initialize the game boards

	initializeBoard(humanBoard);
	initializeBoard(compBoard);

	// Play the game until one player has sunk the other's ships
	while(!done) {

		// Clear the screen to prepare show the game situation before the moves

		clearTheScreen();

		// Display the game board situation

		displayBoard(1,1, HUMAN, humanBoard);
		displayBoard(1,45, COMPUTER, compBoard);

		//Get and validate human move.
		humValid = false;

		while(!humValid) {
			move.clear();

			move = getResponse(20,1, "Please enter a move: ");

			for(int i = 0; i < move.length() && i < 10; i++) {	//Standardizes response

				move[i] = toupper(move[i]);
			}

			testMove = checkMove(move, compBoard, row, col);//tests for valid move
			if(testMove == 0)
			{
				humValid = true;
			}
			else{
				writeMessage(18,1,"Invalid move!");
			}
		}
		// Get and validate the computer's move
		compValid = false;

		while(!compValid) {
			compMove.clear();

			compMove = randomMove();
			testMove = checkMove(compMove, humanBoard, row2, col2);

			if(testMove == 0){
				compValid = true;
			}
		}

		// Execute both moves
		result = playMove(row,col, compBoard);
		compResult = playMove(row2,col2, humanBoard);

		// Clear the screen to show the new game situation after the moves
		clearTheScreen();
		displayBoard(1,1, HUMAN, humanBoard);
		displayBoard(1,45, COMPUTER, compBoard);

		writeResult(20,1, result, HUMAN);
		writeResult(21,1, compResult, COMPUTER);

		// Display the move choices each player made

		writeMessage(18,1, "The computer played: " + compMove);
		writeMessage(17,1, "You played: " + move);


		// Take note if there are any sunken ships
		if(isASunk(result)){
			sunk++;
		}
		if(isASunk(compResult)){
			compSunk++;
		}

		// determine if we have a winner
		if((compSunk >= NUMTOSINK) || (sunk >= NUMTOSINK)) {
			// if one of the player's has sunk five ships the game is over
			done = true;
		} else {
			// pause to let the user assess the situation
			pauseForEnter();
		}
	}

	// Announce the winner
	pauseForEnter();
	clearTheLine(17);
	clearTheLine(18);
	clearTheLine(20);

	if(sunk == NUMTOSINK) {

		writeMessage(21,1, "YOU WON!!!");

	} else if (compSunk == NUMTOSINK) {	//I was bored.
		writeMessage(21,1, "Wow, you actually lost that, I'm impressed.");

		pauseForEnter();
		writeMessage(21,1, "No, seriously, how did you lose?");

		pauseForEnter();
		writeMessage(21,1, "The computer plays totally randomly, how do you play worse than that.");

		pauseForEnter();
		writeMessage(21,1, "Well then.");

		pauseForEnter();
		clearTheScreen();
		return 0;

	} else {
      	writeMessage(21,1, "How did you get a tie??");
   	}

	pauseForEnter();



	return 0;
}// Author:Joshua Stevens
// Date:
// Purpose:Battleship Game

#include "battleship.h"


int main() {

	// variable declarations (you'll need others, of course)

	bool done = false;
	const int NUMTOSINK = 5;	//declared as a const to help with testing purposes.

	Board humanBoard;
	Board compBoard;

	string move;
	string compMove;
	int testMove;


	int row;
	int col;
	int row2;
	int col2;

	bool humValid = false;
	bool compValid = false;

	int result;
	int compResult;
	int sunk = 0;
	int compSunk = 0;
	// Welcome the player to the game

	welcome();	//You're welcome

	// Initialize the game boards

	initializeBoard(humanBoard);
	initializeBoard(compBoard);

	// Play the game until one player has sunk the other's ships
	while(!done) {

		// Clear the screen to prepare show the game situation before the moves

		clearTheScreen();

		// Display the game board situation

		displayBoard(1,1, HUMAN, humanBoard);
		displayBoard(1,45, COMPUTER, compBoard);

		//Get and validate human move.
		humValid = false;

		while(!humValid) {
			move.clear();

			move = getResponse(20,1, "Please enter a move: ");

			for(int i = 0; i < move.length() && i < 10; i++) {	//Standardizes response

				move[i] = toupper(move[i]);
			}

			testMove = checkMove(move, compBoard, row, col);//tests for valid move
			if(testMove == 0)
			{
				humValid = true;
			}
			else{
				writeMessage(18,1,"Invalid move!");
			}
		}
		// Get and validate the computer's move
		compValid = false;

		while(!compValid) {
			compMove.clear();

			compMove = randomMove();
			testMove = checkMove(compMove, humanBoard, row2, col2);

			if(testMove == 0){
				compValid = true;
			}
		}

		// Execute both moves
		result = playMove(row,col, compBoard);
		compResult = playMove(row2,col2, humanBoard);

		// Clear the screen to show the new game situation after the moves
		clearTheScreen();
		displayBoard(1,1, HUMAN, humanBoard);
		displayBoard(1,45, COMPUTER, compBoard);

		writeResult(20,1, result, HUMAN);
		writeResult(21,1, compResult, COMPUTER);

		// Display the move choices each player made

		writeMessage(18,1, "The computer played: " + compMove);
		writeMessage(17,1, "You played: " + move);


		// Take note if there are any sunken ships
		if(isASunk(result)){
			sunk++;
		}
		if(isASunk(compResult)){
			compSunk++;
		}

		// determine if we have a winner
		if((compSunk >= NUMTOSINK) || (sunk >= NUMTOSINK)) {
			// if one of the player's has sunk five ships the game is over
			done = true;
		} else {
			// pause to let the user assess the situation
			pauseForEnter();
		}
	}

	// Announce the winner
	pauseForEnter();
	clearTheLine(17);
	clearTheLine(18);
	clearTheLine(20);

	if(sunk == NUMTOSINK) {

		writeMessage(21,1, "YOU WON!!!");

	} else if (compSunk == NUMTOSINK) {	//I was bored.
		writeMessage(21,1, "Wow, you actually lost that, I'm impressed.");

		pauseForEnter();
		writeMessage(21,1, "No, seriously, how did you lose?");

		pauseForEnter();
		writeMessage(21,1, "The computer plays totally randomly, how do you play worse than that.");

		pauseForEnter();
		writeMessage(21,1, "Well then.");

		pauseForEnter();
		clearTheScreen();
		return 0;

	} else {
      	writeMessage(21,1, "How did you get a tie??");
   	}

	pauseForEnter();



	return 0;
}// Author:Joshua Stevens
// Date:
// Purpose:Battleship Game

#include "battleship.h"


int main() {

	// variable declarations (you'll need others, of course)

	bool done = false;
	const int NUMTOSINK = 5;	//declared as a const to help with testing purposes.

	Board humanBoard;
	Board compBoard;

	string move;
	string compMove;
	int testMove;


	int row;
	int col;
	int row2;
	int col2;

	bool humValid = false;
	bool compValid = false;

	int result;
	int compResult;
	int sunk = 0;
	int compSunk = 0;
	// Welcome the player to the game

	welcome();	//You're welcome

	// Initialize the game boards

	initializeBoard(humanBoard);
	initializeBoard(compBoard);

	// Play the game until one player has sunk the other's ships
	while(!done) {

		// Clear the screen to prepare show the game situation before the moves

		clearTheScreen();

		// Display the game board situation

		displayBoard(1,1, HUMAN, humanBoard);
		displayBoard(1,45, COMPUTER, compBoard);

		//Get and validate human move.
		humValid = false;

		while(!humValid) {
			move.clear();

			move = getResponse(20,1, "Please enter a move: ");

			for(int i = 0; i < move.length() && i < 10; i++) {	//Standardizes response

				move[i] = toupper(move[i]);
			}

			testMove = checkMove(move, compBoard, row, col);//tests for valid move
			if(testMove == 0)
			{
				humValid = true;
			}
			else{
				writeMessage(18,1,"Invalid move!");
			}
		}
		// Get and validate the computer's move
		compValid = false;

		while(!compValid) {
			compMove.clear();

			compMove = randomMove();
			testMove = checkMove(compMove, humanBoard, row2, col2);

			if(testMove == 0){
				compValid = true;
			}
		}

		// Execute both moves
		result = playMove(row,col, compBoard);
		compResult = playMove(row2,col2, humanBoard);

		// Clear the screen to show the new game situation after the moves
		clearTheScreen();
		displayBoard(1,1, HUMAN, humanBoard);
		displayBoard(1,45, COMPUTER, compBoard);

		writeResult(20,1, result, HUMAN);
		writeResult(21,1, compResult, COMPUTER);

		// Display the move choices each player made

		writeMessage(18,1, "The computer played: " + compMove);
		writeMessage(17,1, "You played: " + move);


		// Take note if there are any sunken ships
		if(isASunk(result)){
			sunk++;
		}
		if(isASunk(compResult)){
			compSunk++;
		}

		// determine if we have a winner
		if((compSunk >= NUMTOSINK) || (sunk >= NUMTOSINK)) {
			// if one of the player's has sunk five ships the game is over
			done = true;
		} else {
			// pause to let the user assess the situation
			pauseForEnter();
		}
	}

	// Announce the winner
	pauseForEnter();
	clearTheLine(17);
	clearTheLine(18);
	clearTheLine(20);

	if(sunk == NUMTOSINK) {

		writeMessage(21,1, "YOU WON!!!");

	} else if (compSunk == NUMTOSINK) {	//I was bored.
		writeMessage(21,1, "Wow, you actually lost that, I'm impressed.");

		pauseForEnter();
		writeMessage(21,1, "No, seriously, how did you lose?");

		pauseForEnter();
		writeMessage(21,1, "The computer plays totally randomly, how do you play worse than that.");

		pauseForEnter();
		writeMessage(21,1, "Well then.");

		pauseForEnter();
		clearTheScreen();
		return 0;

	} else {
      	writeMessage(21,1, "How did you get a tie??");
   	}

	pauseForEnter();



	return 0;
}
