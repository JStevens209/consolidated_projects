#ifndef _LRU_H
#define _LRU_H

#include <iostream>
#include <algorithm>
#include <iterator>
#include <chrono>
#include <vector>
#include <tuple>

#include "ReplacementAlgorithm.h"


class LRU : public ReplacementAlgorithm {
public:
    LRU( int numPageFrames );
    void insert( int pageNumber ) override;

private:
    // Used std::vector instead of std::list because std::list iterators are more annoying.
    std::vector<int> pageMemory;
};

#endif