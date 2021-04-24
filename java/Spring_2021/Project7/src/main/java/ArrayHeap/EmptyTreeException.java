package project7;

/**
 * The EmptyTreeException class provides an exception which a BinaryTree can
 * raise when a method is executed which doesn't make sense with an empty tree
 * @author Dr. Gallagher
 * @version 1.0
 * Created: 15 Feb 01
 * Summary of Modifications:
 *
 * Description:
 */

public class EmptyTreeException extends RuntimeException {

    public EmptyTreeException() {
        this ("Empty Tree");
    }
    public EmptyTreeException(String err) {
        super (err);
    }
}