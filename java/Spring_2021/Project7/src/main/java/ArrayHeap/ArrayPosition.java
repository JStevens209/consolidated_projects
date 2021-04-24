package project7;

/**
 * Title:        Project #7
 * Description:
 * Copyright:    Copyright (c) 2001
 * Company:
 * @author
 * @version 1.0
 */

public class ArrayPosition implements Position {

    private int index;
    private Object element;

    public ArrayPosition() {
        this (-1, null);
    }

    public ArrayPosition(int newIndex, Object newElement) {
        index = newIndex;
        element = newElement;
    }

    public Object element () {
        return element;
    }

    public void setElement (Object newElement) {
        element = newElement;
    }

    public int getIndex () {
        return index;
    }

    public void setIndex (int newIndex) {
        index = newIndex;
    }
}