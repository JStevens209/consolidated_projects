package project7;

/**
 * Title:        Project #7
 * Description:
 * Copyright:    Copyright (c) 2001
 * Company:
 * @author
 * @version 1.0
 */

public interface Heap extends BinaryTree {
  // msy want to throw FullHeapException unless an extensible array used
  public void add(Object newKey, Object newElement) throws InvalidObjectException;

  public Object removeRoot() throws EmptyHeapException;
}
