package project6;

/**
 * The EulerTour class provides a base ADT for a variety of tree walks
 *
 * @author Dr. Gallagher
 * @version 1.0
 * Created: 16 Feb 01
 * Summary of Modifications:
 *
 * Description:  Provides a template pattern for traversing a binary tree.  An
 * Euler Tour performs pre-, post-, and in-order visits to a node.  Classes
 * derived from EulerTour can override specific methods to tailor these visits
 * to the particular needs of the traversal.
 */

public abstract class EulerTour {

    protected BinaryTree tree;

    public EulerTour (BinaryTree newTree) {
        tree = newTree;
    }

    /**
     * @return result computed from the walk of the subtree rooted at pos
     * @param pos is the node which acts as the root for this Euler Tour
     */
    public Object performTour (Position pos) {
        TraversalResult result = initResult();
        if (tree.isExternal (pos) ) {
            visitExternal (pos, result);
        }
        else {
            visitPreorder (pos, result);
			
			if (tree.leftChild(pos) != null) {
                result.leftResult = performTour (tree.leftChild(pos) );
			}
            visitInorder (pos, result);
			
			if (tree.rightChild(pos) != null) {
				result.rightResult = performTour (tree.rightChild(pos) );
			}
			
            visitPostorder (pos, result);
        }
        return computeResult( result);
    }

    /**
     * @param pos is the external node being visited
     * @param result is a storage mechanism for results computed as this node
     */
    protected void visitExternal (Position pos, TraversalResult result) { }

    /**
     * @param pos is the node being visited
     * @param result is a storage mechanism for results computed as this node
     */
    protected void visitPreorder (Position pos, TraversalResult result) { }
    /**
     * @param pos is the node being visited
     * @param result is a storage mechanism for results computed as this node
     */
    protected void visitInorder (Position pos, TraversalResult result) { }
    /**
     * @param pos is the node being visited
     * @param result is a storage mechanism for results computed as this node
     */
    protected void visitPostorder (Position pos, TraversalResult result) { }

    /**
     * Provides initialized result storage; this default version simply creates
     * an empty result object
     * @returns an initialized object for storing results of Euler Tour
     */
    protected TraversalResult initResult() {
        return new TraversalResult();
    }
    /**
     * Computes the overall result for the Euler Tour rooted at this node
     * @param result is the storage mechanism for results computed during the
     * tour
     */
    protected Object computeResult (TraversalResult result) {
        return result.nodeResult;
    }

}