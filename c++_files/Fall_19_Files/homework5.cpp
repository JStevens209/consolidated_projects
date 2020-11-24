#include <iostream>
#include <fstream>
#include <cctype>
using namespace std;

void StoreVerses(string verse);//We were supposed to inlude a function and addend the verse to a file, so I did both in one

int main ()
{

	ifstream in; //Variables are grouped according to what they are used for
	ofstream out;

	string book;
	string chapter;
	string verse;

	string bookSearch;
	string currBook;
	string chapterSearch;
	string verseSearch;


	cout << "Please enter a reference: " << endl << "Book: "; //gets search parameters
	getline(cin, currBook); //It is a getline because books can be more than one word ex. Song of Solomon

	cout << endl << "Chapter: ";
	cin >> chapterSearch;

	cout << endl << "Verse: ";
	cin >> verseSearch;

	in.open("Bible.txt");

	bookSearch = currBook; //used to hold the original name of the book

	for(int i = 0; i < bookSearch.length(); i++) //Standardizes the format of the string
		{
			bookSearch[i] = toupper( bookSearch[i] );
		}
	for(int i = 0; i < currBook.length(); i++)//Standardizes the format of the origninal name, for ex. GENEsis becomes Genesis
		{
			currBook[i]=tolower( currBook[i] );
		}
	currBook[0] = toupper(currBook[0]);

	bookSearch = "THE BOOK OF " + bookSearch; //This is done because of the way the lines are formatted, and because I have to use getline for this

	while (book != bookSearch) //Searches for the book
	{
		getline(in, book);
		if(in.eof())
		{
			cout << "Error, the book of " << currBook << " does not exist" << endl;
			return 1;
		}
	}
	while (!in.eof())	//searches for the chapter
	{

		in >> chapter;

		if((chapter == "CHAPTER") || (chapter == "PSALM")) //Does it equal chapter?
		{
			in >> chapter; //If so then what is the next string?		//Sidenot: The imbedded if statement is so that I can run the input one more time to get the chapter's number, then check that.
			if(chapter == chapterSearch)	//is the next string the correct chapter number?
			{
				break;
			}
		}
		if(chapter == "BOOK" || in.eof()) //Does it reach the next book?
		{
			cout << "Error, the chapter " << chapterSearch << " in " << currBook << " does not exist" << endl;
			return 1;
		}
	}
	while(verse != verseSearch)
	{
		in >> verse;

		if(verse == "CHAPTER" || in.eof()) //Does it reach the next chapter?
		{
			cout << "Error, verse " << verseSearch << " in chapter " << chapterSearch << " of " << currBook << " does not exist" << endl;
			return 1;
		}
	}

	string finalVerse;
	getline(in, finalVerse);  //Since every other string has been removed before this, the next line it gets is the verse.
	cout << endl << currBook << " " << chapterSearch << ":" << verseSearch << " " <<finalVerse << endl;

	StoreVerses(finalVerse); //Stores the verse

	in.close();
	out.close();
	return 0;

}

void StoreVerses(string verse)
{
	ofstream out;
	out.open("Verses.txt");
	out << verse << endl;

	out.close();
}
