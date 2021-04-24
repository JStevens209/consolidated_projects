package project7;

/**
 * Basic storage element for storing a key and data
 *
 * @author Dr. Gallagher
 * @version 1.0
 * Created 2 Mar 2001
 * Description: Stores 2 objects: a key and an element
 */

public class Item {

    private Object itemKey;
    private Object itemElement;

    public Item() {
        this (null, null);
    }

    public Item(Object key, Object element) {
        itemKey = key;
        itemElement = element;
    }

    public Object key() {
        return itemKey;
    }
    public void setKey(Object key) {
        itemKey = key;
    }
    public Object element() {
        return itemElement;
    }
    public void setElement (Object element) {
        itemElement = element;
    }
}