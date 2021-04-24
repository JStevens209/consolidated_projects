package project7;

/**
 * Title: Project #7
 * Description:
 * Copyright: Copyright (c) 2001
 * Company:
 * @author
 * @version 1.0
 */

public class ArrayHeap extends ArrayBinaryTree implements Heap {

    Comparator heapComp;

    public ArrayHeap(Comparator newComp) {
        this (newComp, DEFAULT_SIZE);
    }

    public ArrayHeap(Comparator newComp, int newSize) {
        super (newSize);
        heapComp = newComp;
    }


  public void add(Object newKey, Object newElement) throws InvalidObjectException {
      // TODO: add code here
  }

  public Object removeRoot() throws EmptyHeapException {
      // TODO: add code here
      return null;
  }

        // you may want to expand main; it is just provided as a sample
    public static void main (String[] args) {
	    Comparator myComp = new IntegerComparator();
        Heap myHeap = new ArrayHeap (myComp, 8);

        myHeap.add(14, 14);
        myHeap.add(17, 17);
        myHeap.add(3, 3);
        myHeap.add(2, 21);
        myHeap.add(8, 8);
        myHeap.add(7, 18);
        myHeap.add(1, 1);
        myHeap.add(19, 11);
        myHeap.add(17, 17);
        myHeap.add(25, 6);

        System.out.println(myHeap.size());
        while (!myHeap.isEmpty()) {

            Item removedItem = (Item) myHeap.removeRoot();
            System.out.print("Key:   " + removedItem.key() + "     ");
            System.out.println("Removed " + removedItem.element());
        }
        System.out.println("All nodes removed");
    }
}
