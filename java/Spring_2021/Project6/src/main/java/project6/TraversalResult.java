package project6;

/**
 * The TraversalResult class provides result storage for use during tree
 *  traversals, particularly in support of Euler Tours
 *
 * @author Dr. Gallagher
 * @version 1.0
 * Created: 16 Feb 01
 * Summary of Modifications:
 *
 * Description:  Since an Euler Tour is a generic traversal which can be
 * tailored to meet many different requirements, it employs a generic results
 * storage mechanism which can store the results from the children nodes and
 * its own internal computations.
 */


public class TraversalResult {

    public Object nodeResult;
    public Object leftResult;
    public Object rightResult;

    public TraversalResult() {
    }
}