package project7;

/**
 * This class implements the Binary Tree interface using an array as the
 * underlying structure
 *
 * @author Dr. Gallagher
 * @version 1.2
 * Created 23 Feb 2001
 * Summary of Modifications
 *      2 Mar 2001 - DMG - corrected bugs in rightChild(), leftChild(),
 *          sibling(), and parent() to prevent underrun/overrun of array
 *      5 Mar 2001 - DMG - corrected same bug from above in isExternal(); also
 *          added checkPosition to all functions which receive a Position as
 *          an argument
 *      28 Feb 2002 - DMG - adjusted array size to be 1 more than asked for,
 *          since element 0 not being used.  Required numerous checks for
 *          overrun to be adjusted in different routines.
 *      5 Mar 2002 - DMG changed design so that ROOT element stored in location
 *          0 in array - NOTE: most old change comments removed because of new
 *          paradigm
 *      8 Dec 2008 - DMG changed design of several methods to determine whether
 *          children are present based on size, not capacity. Improved checkPosition
 *          to test size and use instanceOf
 *
 * Description: This class provides an array implementation of the BinaryTree
 * ADT.  Because the underlying structure is an array, it will be most
 * effective in applications where the Binary Tree remains balanced.
 *
 */

public class ArrayBinaryTree implements BinaryTree {

        // static variables
    protected static final int DEFAULT_SIZE = 100;
    protected static final int ROOT = 0;

        // instance variables
    protected ArrayPosition[] btArray;
    protected int size=0;

        // constructors
    public ArrayBinaryTree() {
        this (DEFAULT_SIZE);
    }

    public ArrayBinaryTree( int initialSize) {
        btArray = new ArrayPosition[initialSize];
    }

        // instance methods
    public Position root() throws EmptyTreeException {
        if (size == 0) {
            throw new EmptyTreeException ("Tree was empty");
		}
        return (Position) btArray[ROOT];
    }

    public Position leftChild (Position pos) throws InvalidPositionException {
        checkPosition(pos);
            // DMG - 3/5/02  - added 1 to Index, since now ROOT=0
        int childIndex = (((ArrayPosition) pos).getIndex() << 1) + 1;
            // DMG - 3/5/02 - changed from > to >=
		// DMG - 12/8/08- changed capacity to size
        if (childIndex >= size ) {
            return null;
		}
        else {
            return (Position) btArray[childIndex];
		}
    }
	
    public Position rightChild (Position pos) throws InvalidPositionException {
        checkPosition(pos);
            // DMG - 3/5/02  - added 1 to Index, since now ROOT=0
        int childIndex = (((ArrayPosition) pos).getIndex() << 1) + 2;
            // DMG - 3/5/02 - changed from > to >=
		// DMG - 12/8/08- changed capacity to size
        if (childIndex >= size ) {
            return null;
		}
        else {
            return (Position) btArray[childIndex];
		}
    }
	
    public Position sibling (Position pos) throws InvalidPositionException {
        checkPosition(pos);
        int myIndex = ((ArrayPosition) pos).getIndex();
            // DMG - 3/5/02 - changed then-else blocks around
        if (myIndex % 2 == 0) {    // i.e., right child or root
                // it could also be root
            if (myIndex == ROOT) {
                return null;
			}
            else {
                return (Position) btArray[myIndex-1];
			}
        }
        else {      // left child
                // DMG 3/5/02 - added -1 because no longer declaring extra location
   		    // DMG - 12/8/08- changed capacity to size
            if (myIndex == size - 1) {
                return null;
			}
            else {
                return (Position) btArray[myIndex+1];
			}
        }
    }
	
    public Position parent(Position pos) throws InvalidPositionException {
        checkPosition(pos);
        int myIndex = ((ArrayPosition) pos).getIndex();
            // DMG   3/5/02  - Because root=0, parent= (index-1) / 2
        if (myIndex == ROOT) {
            return null;
		}
        else {
            return (Position) btArray[ (myIndex-1) >> 1];
		}

    }

    public boolean isInternal (Position pos) throws InvalidPositionException {
        checkPosition(pos);
        int myIndex = ((ArrayPosition) pos).getIndex();
            // DMG - 3/5/02 - next 2 lines changed because ROOT=0 and because no
            // capacity fudge required
        int lChildIndex = (myIndex << 1)  + 1;
            // DMG - 12/8/08- changed capacity to size
        if (lChildIndex >= size) {
            return false;
		}
            // case where left child is last element, and right child is past
            // only internal if leftchild is present
            // DMG - 3/5/02  - -1 added
        else if (lChildIndex == btArray.length - 1) {
            return (btArray[lChildIndex] != null);
		}
            // case where both inside array; internal if either child present
        else if ( (btArray[lChildIndex] != null) ||
                  (btArray[lChildIndex + 1] != null) ) {
            return true;
		}
        else {
            return false;
		}
    }
	
    public boolean isExternal (Position pos) throws InvalidPositionException {
        return (! isInternal (pos) );
    }
	
    public boolean isRoot (Position pos) throws InvalidPositionException {
        checkPosition(pos);
        int myIndex = ((ArrayPosition) pos).getIndex();
        return (myIndex == ROOT);
    }

    public int size() {
        return size;
    }
	
    public boolean isEmpty() {
        return (size == 0);
    }

    protected void checkPosition (Position pos) throws InvalidPositionException {
		// DMG - 12/8/08- changed to use instanceof
        if (!(pos instanceof ArrayPosition)) {
            throw new InvalidPositionException();
        }
		// DMG - 12/8/08- added check of size
        int index = ((ArrayPosition) pos).getIndex();
        if (index >= size) {
            throw new InvalidPositionException();
        }
    }

    public static void main (String[] args) {
        ArrayBinaryTree myTree = new ArrayBinaryTree();
    }
}