// Author: Joshua Stevens
// Date Created: October 8, 2020

// This implementation of the FIFO algorithm relies on the basic structure of an array.
// It assumes that the data sent in will never be -1, and uses -1 to indicate an empty frame.
// If there is an empty frame, it fills it with the next available data, if not, it pops off 
// the front of the array ( which by design will always be the first one in ), and pushes the
// new data to the back of the array, IE First in, First out.

#include "FIFO.h"

FIFO::FIFO( int numPageFrames ) : ReplacementAlgorithm( numPageFrames ) {
    pageFaultCount = 0;
    pageMemory.resize( numPageFrames, -1 );
}

void FIFO::insert( int pageNumber ) {
    // Implement FIFO page replacement algorithm
    // Increment pageFaultCount if a page fault occurs
    auto emptyFrame = std::find( begin( pageMemory ), end( pageMemory ), -1 );
    auto pageNumberFrame = std::find( begin( pageMemory ), end( pageMemory ), pageNumber );

    // Checks if the pageNumber already exists in pageMemory
    // If the pageNumber already exists, dont do anything
    if( pageNumberFrame != pageMemory.end() ){
        return;
    }

    // If there is an empty page frame, and the number is not already in the list,
    // place the number in the first empty page frame.
    if( emptyFrame != pageMemory.end() ) {
        *emptyFrame = pageNumber;
        pageFaultCount++;
    }

    // If there are no empty frames, and the number is not already in the list,
    // remove the first element, place the new element in the back of the list
    else {
        pageMemory.pop_front();
        pageMemory.push_back( pageNumber );
        pageFaultCount++;
    }
}