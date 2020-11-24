#ifndef _REPLACEMENTALGORITHM_H
#define _REPLACEMENTALGORITHM_H

class ReplacementAlgorithm {
public:
    // numPageFrames - the number of physical page frames
    ReplacementAlgorithm( int numPageFrames ): pageFrameCount( numPageFrames ) {};

    // returns the number of page faults that occured
    int getPageFaultCount() { return pageFaultCount; }

    // pageNumber - the page number to be inserted
    virtual void insert( int pageNumber ) {};

protected:
    int pageFaultCount;
    int pageFrameCount;
};

#endif // !PPD_REPLACEMENTALGORITHM_H