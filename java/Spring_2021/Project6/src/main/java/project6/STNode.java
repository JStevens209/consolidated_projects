package project6;

/**
 * This class can be used as a node in a general tree.
 *
 * @author Dr. Gallagher
 * @version 1.0
 * Created: 15 Feb 01
 * Summary of Modifications:
 *
 * Description:  The STNode class provides a node which can be used in a
 * general tree.  It's sibling pointer can be used to form a list of children
 * of a particular node.  Thus, to find the children of a node, you follow the
 * leftChild pointer to find the first child, and then follow sibling pointers
 * to find the remaining children.
 */

public class STNode implements Position {

        // instance variables
    private Object element;
    private STNode leftChild, sibling, parent;

        // constructors
    public STNode() {
    }
    /**
     * @param elem is the object to be stored in the node
     * @param newParent is a reference to the parent node
     * @param newSibling is a reference to the sibling node
     * @param newLeftChild is a reference to the first child
     */
    public STNode (Object elem, STNode newParent, STNode newSibling,
                   STNode newLeftChild) {
        element = elem;
        parent = newParent;
        sibling = newSibling;
        leftChild = newLeftChild;
    }

            // public methods
    /**
     * @return reference to stored element
     */
    public Object element () {
        return element;
    }
    /**
     * @param newElement is the Object which is to be stored in the node
     */
    public void setElement (Object newElement) {
        element = newElement;
    }
    /**
     * @return reference to this node's parent
     */
    public STNode getParent () {
        return parent;
    }
    /**
     * @param newParent is an STNode reference which should be assigned to the
     * parent pointer
     */
    public void setParent (STNode newParent) {
        parent = newParent;
    }
    /**
     * @return reference to this node's first child
     */
    public STNode getLeftChild () {
        return leftChild;
    }
    /**
     * @param newLeftchild is an STNode reference which should be assigned
     * to the leftChild pointer
     */
    public void setLeftChild (STNode newLeftChild) {
        leftChild = newLeftChild;
    }
    /**
     * @return reference to this node's sibling
     */
    public STNode getSibling () {
        return sibling;
    }
    /**
     * @param newSibling is an STNode reference which should be assigned to the
     * sibling pointer
     */
    public void setSibling (STNode newSibling) {
        sibling = newSibling;
    }
}