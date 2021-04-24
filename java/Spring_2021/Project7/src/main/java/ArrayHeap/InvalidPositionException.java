package project7;

/**
 * The InvalidPositinException class provides an exception which any user of
 * the Position ADT can raise if it is passed a Position which does not make
 * sense it the present context

 * @author Dr. Gallagher
 * @version 1.0
 * Created: 15 Feb 01
 * Summary of Modifications:
 *
 * Description:
 */

public class InvalidPositionException extends RuntimeException {

    public InvalidPositionException() {
        this ("Invalid Position");
    }
    public InvalidPositionException(String err) {
        super (err);
    }
}