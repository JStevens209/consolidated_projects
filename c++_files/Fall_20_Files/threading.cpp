//Author: Joshua Stevens
//Date: Sep 13, 2020
//Summary: A program used to simulate a possible solution to the producer/consumer problem


// condition_variable example
#include <iostream>           // std::cout
#include <thread>             // std::thread
#include <mutex>              // std::mutex, std::unique_lock
#include <condition_variable> // std::condition_variable
#include <vector>
#include <chrono>
#include <random>

using namespace std;

//I mean... I COULD pass them as args in both functions...
//Or I could just do this and make the code more readable.
mutex mtx;
condition_variable_any cv;

bool ready = true;
bool  done = false;

//OK, so I really wanted to use a user declared N.
//std::thread really does NOT want an array passed to it whose size was declared with a variable
// ex. 
// const int N = 10;
// char arr[N] = {};
//
// thread( producer, arr, N );
//
// will throw an error "a template argument may not reference a variable-length array type"
// so, to be able to use the array in a thread, it must be a global, which makes it impossible for the size to be variable.
// I commented the code that would use the array instead of the vector just in case you SPECIFICALLY wanted an array

//const int SIZE = 10;
//char arrayBuffer[ SIZE ] = { '0','0','0','0','0','0','0','0','0','0' }

/*
bool bufferHasItems(){
    for( int i = 0; i < SIZE; i++){
        if( arrayBuffer[i] != '0' ){
            return false;
        }
    }
    return true;
}
*/


//waits for buffer access, add item, release buffer, exit
void producer( vector<char> &buffer, int size ){

    // This is just my way of getting a random set of chars
    // Have a string of all the chars, randomly pick a number between 0-25 to access the string at
    const string charList = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    srand( time(0) );

    for( int i = 0; i < size; i++ ){
        while( !ready ){
            cv.wait( mtx );
        }

        ready = false;

        if( buffer.size() < size ){
            buffer.push_back( charList[ rand() % 26 ] );
            cout << char( tolower( buffer[ buffer.size() - 1 ])) << endl;
        }

        /*
        for( int i = 0; i < SIZE; i++){
            if( arrayBuffer[i] == '0' ){
                arrayBuffer[i] = charList[ rand() % 26 ];
                break;
            }
        }
        */

        ready = true;
        cv.notify_one();
    }

     done = true;
    return;
}

//waits for buffer access, take item, release buffer, exit
void consumer( vector<char> &buffer, int size ){

    //While the producer is still producing OR there are still items in the buffer...
    while( !done || buffer.size() > 0 ) {  // || bufferHasItems() ) {
        while( !ready){
            cv.wait(mtx);
        }

        ready = false;

        if( buffer.size() > 0 ){ 
            cout << buffer[0] << endl;
            buffer.erase( buffer.begin() );
        }
        
        /*
        for( int i = 0; i < SIZE; i++ ){
            if( arrayBuffer[i] != '0' ){
                cout << arrayBuffer[i] << endl;
                arrayBuffer[i] = '0';
                break;
            }
        }
        */

        ready = true;
        cv.notify_one(); 
    }

    return;
}

int main() {

    // I took "Use a char array of size N as the shared buffer."
    // to mean that it must handle a char array of size N
    int size;
    cout << "Enter number of items: ";
    cin >> size;
    cout << endl << "Producing and Consuming..." << endl;

    vector<thread> threads;
    vector<char> buffer;

    threads.push_back( thread( producer, ref(buffer), size ));
    this_thread::sleep_for( chrono::nanoseconds( 10 ) );

    threads.push_back( thread( consumer, ref(buffer), size ));

    threads[0].join();
    threads[1].join();

    return 0;
}

//the command I had to use to compile on MacOS 10.14
//clang++ -std=c++11 threading.cpp
