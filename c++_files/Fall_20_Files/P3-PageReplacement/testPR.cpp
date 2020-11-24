// testPR.cpp
// Patrick P. Dudenhofer
// CS3310 - Operating System
// Page Replacement
// 2015 October 12
//
// Testing program for the page replacement algorithms.
//

#include <cstdlib>
#include <time.h>
#include <vector>
#include <iostream>
#include <string>
#include <fstream>

#include "ReplacementAlgorithm.h"
#include "LRU.h"
#include "FIFO.h"
// #include "OPT.h"

std::vector<int> referenceString;

const int MAX_PAGE_NUMBER = 50;

// testPR <reference string size> <number of page frames> [fileName]
// The "reference string size" parameter is ignored if a filename is provided.
int main(  int argc, char **argv ) {
    int count;
    int numPageFrames;
    bool useRefFile = false;
    std::string fileName = "";
    std::ifstream in;

    srand( ( unsigned int )time( 0 ) );

    if ( argc < 3 || argc > 4 ){
        std::cerr << "Usage: " << argv[0]
                  << " <reference string size> <number of page frames> "
                  << "[reference string filename]"
                  << std::endl;
        exit(1);
    }

    count = atoi( argv[1] );
    numPageFrames = atoi( argv[2] );

    // input reference string from file or just randomly generate
    if ( argc == 4 ) {
        useRefFile = true;

        //open the input file
        in.open( argv[3] );
        if ( !in.is_open() ) {
            std::cerr << "Error opening file " << fileName
                      << ". Exiting..." << std::endl;
            exit(1);
        }

        int n;
        while ( !in.eof() ) {
            in >> n;
            if ( n >= 0 && n < MAX_PAGE_NUMBER ){
                referenceString.push_back( n );
            }
        }
        in.close();
    }

    else {
        for ( int i = 0; i < count; i++ ){
            referenceString.push_back( rand() % MAX_PAGE_NUMBER );
        }
    }
    
    ReplacementAlgorithm * lru = new LRU( numPageFrames );
    ReplacementAlgorithm * fifo = new FIFO( numPageFrames );

    for ( int i : referenceString ) {
        lru->insert( i );
        fifo->insert( i );
    }

    std::cout << "LRU faults  = " << lru->getPageFaultCount() << std::endl;
    std::cout << "FIFO faults = " << fifo->getPageFaultCount() << std::endl;
    return 0;
}