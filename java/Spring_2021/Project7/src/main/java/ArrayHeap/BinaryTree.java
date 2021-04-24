package project7;

/**
 * The BinaryTree interface defines an ADT for a binary tree.
 *
 * @author Dr. Gallagher
 * @version 1.0
 * Created: 15 Feb 01
 * Summary of Modifications:
 *
 * Description:  Provides a set of methods for employing a binary tree.
 * The ADT assumes the tree will be created externally, and provides no methods
 * for adding or deleting nodes from the tree.  Nodes within the tree are
 * abstracted as Positions using the Position interface.
 */

public interface BinaryTree {
    /**
     * @return a reference to the root node
     */
    public Position root() throws EmptyTreeException;
    /**
     * @param pos is the node whose left child will be returned
     * @return a reference to left child of pos
     */
    public Position leftChild (Position pos) throws InvalidPositionException;
    /**
     * @param pos is the node whose right child will be returned
     * @return a reference to right child of pos
     */
    public Position rightChild (Position pos) throws InvalidPositionException;
    /**
     * @param pos is the node whose sibling will be returned
     * @return a reference to the sibling of pos
     */
    public Position sibling (Position pos) throws InvalidPositionException;
    /**
     * @param pos is the node whose parent will be returned
     * @return a reference to the parent of pos
     */
    public Position parent(Position pos) throws InvalidPositionException;

    /**
     * @param pos is the node which will be examined
     * @return true if node has 1 or 2 childen
     */
    public boolean isInternal (Position pos) throws InvalidPositionException;
    /**
     * @param pos is the node which will be examined
     * @return true if node has no childen
     */
    public boolean isExternal (Position pos) throws InvalidPositionException;
    /**
     * @param pos is the node which will be examined
     * @return true if the node is the root node
     */
    public boolean isRoot (Position pos) throws InvalidPositionException;

    /**
     * @return the number of Positions (nodes) in the tree
     */
    public int size();
    /**
     * @return true if the tree currently contains no Positions
     */
    public boolean isEmpty();

}