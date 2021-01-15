#include <iostream>
#include <fstream>
#include <cctype>
using namespace std;

//We were supposed to inlude a function and addend the verse to a file, so I did both in one
void StoreVerses(string verse);

int main ()
{
	// References the string.find function which returns -1 if substr not found
	const int DOES_NOT_EXIST = -1;

	ifstream in; 
	in.open("Bible.txt");

	string bookSearch;
	string bookPrintName;
	string chapterSearch;
	string verseSearch;
	string reference;

	// Gets search parameters
	cout << "Please enter a reference: " << endl << "Book: "; 
	cin >> bookSearch;
	bookPrintName = bookSearch;

	cout << endl << "Chapter: ";
	cin >> chapterSearch;

	cout << endl << "Verse: ";
	cin >> verseSearch;

	reference = bookSearch + " " + chapterSearch + ":" + verseSearch;

	// Standardizes the format of the origninal name
	for( int i = 0; i < bookSearch.length(); i++ ) {
		bookSearch[i] = toupper( bookSearch[i] );
	}

	bookSearch = "THE BOOK OF " + bookSearch;
	try {
		while(true) {

			bool bookFound = false;
			bool chapterFound = false;

			string verse;
			getline( in, verse );

			if( verse == bookSearch ) {
				bookFound = true;
			}

			else if( bookFound && (( verse.find( "CHAPTER" + chapterSearch ) != DOES_NOT_EXIST ) || (verse.find( "PSALM" + chapterSearch ) != DOES_NOT_EXIST ))) {
				chapterFound = true;
			}

			else if( bookFound && chapterFound && ( verse.find( verseSearch ) != DOES_NOT_EXIST )) {
				cout << reference << " " << verse << endl;
			}

			// If it gets to the next chapter, with out finding the verse number, verse doesn't exist.
			else if( bookFound && (( verse.find( "CHAPTER" + chapterSearch ) != DOES_NOT_EXIST ) || (verse.find( "PSALM" + chapterSearch ) != DOES_NOT_EXIST )) ) {
				throw verseNotFound( reference );
			}

			if( in.eof() ) {
				throw verseNotFound( reference );
			}

		}
	} catch ( verseNotFound& e ) {
		cout << "ERROR: " << e << " not found." << endl;
		return 1;
	}


}
/*

	string book;
	string chapter;
	string verse;
	
	// Searches for the book
	while( book != bookSearch ) {
		getline( in, book );

		if( in.eof() ) {
			cout << "Error, the book of " << bookPrintName << " does not exist" << endl;
			return 1;
		}
	}

	// Searches for the chapter
	while ( !in.eof() )	{

		const int NOT_EXIST = -1;
		getline( in, chapter )

		if((  chapter.find( "CHAPTER" + chapterSearch ) != NOT_EXIST ) || ( chapter.find( "PSALM" + chapterSearch ) != NOT_EXIST )) {
			break;
		}
		// Does it reach the next book?
		else if( chapter.find( "BOOK" ) != NOT_EXIST || in.eof() ) {
			cout << "Error, the chapter " << chapterSearch << " in " << bookPrintName << " does not exist" << endl;
			return 1;
		}
	}

	// Searches for the verse
	while( verse != verseSearch ) {
		in >> verse;

		//Does it reach the next chapter?
		if( verse == "CHAPTER" || in.eof() ) {
			cout << "Error, verse " << verseSearch << " in chapter " << chapterSearch << " of " << bookPrintName << " does not exist" << endl;
			return 1;
		}
	}

	// Since every other string has been removed before this, the next line it gets is the verse.
	getline( in, verse );
	cout << endl << bookPrintName << " " << chapterSearch << ":" << verseSearch << " " << verse << endl;

	//Stores the verse
	StoreVerses( verse ); 

	in.close();
	return 0;

}

void StoreVerses(string verse)
{
	ofstream out;
	out.open("Verses.txt");
	out << verse << endl;

	out.close();
}
*/