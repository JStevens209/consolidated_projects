// Author: Joshua Stevens
// Date Created: October 8, 2020

// This implementation of the LRU algorithm works in such a way that the most recently used pages are at the top
// as time goes on, if the page isnt used again, it moves towards the bottom of the list. When a new page is added
// the bottom-most page is destroyed, and the new page goes on top.
// It took me way to long to write these specific 14 lines of code, more than 6 hours I think, I am proud of this.
// I spent most of that time testing theories, and learning how specific parts of the code worked, especially iterators.
#include "LRU.h"

LRU::LRU( int numPageFrames ) : ReplacementAlgorithm( numPageFrames ) {
    pageFaultCount = 0;
    pageMemory.resize( numPageFrames, -1 );
}

void LRU::insert( int pageNumber ) {   
    
    // Finds the already existing page number in the list, if there is none, returns pageMemory.end()
    auto existingPage = std::find( pageMemory.begin(), pageMemory.end(), pageNumber );

    // If the pageNumber already exists in the list,
    // bump it back up to the beginning of the list.
    if( existingPage != pageMemory.end() ) {
        for( auto iter = (existingPage - 1); iter >= pageMemory.begin(); iter-- ) {
            std::iter_swap( existingPage, iter );
            existingPage--;
        }
    }
    // If pageNumber does not already exist
    // delete the item at the bottom of the list, and insert the new item at the top.
    else {
        pageMemory.pop_back();
        pageMemory.insert( pageMemory.begin(), pageNumber );
        
        pageFaultCount++;
    }
}
