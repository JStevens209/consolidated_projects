#ifndef _FIFO_H
#define _FIFO_H

#include <iostream>
#include "ReplacementAlgorithm.h"
#include <list>
#include <algorithm>
#include <iterator>

class FIFO : public ReplacementAlgorithm {
public:
    FIFO( int numPageFrames );
    void insert( int pageNumber ) override;

private:
    // data structure to store the int page frame list
    std::list<int> pageMemory;
};

#endif