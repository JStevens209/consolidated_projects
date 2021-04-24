package project7   ;

/**
 * The Position interface creates an ADT for use as nodes of linked lists
 * or trees
 * @author Dr. Gallagher
 * @version 1.0
 * Created: 15 Feb 01
 * Summary of Modifications:
 *
 *
 * Description:  Provides an abstraction of a Position, for use in various
 * data structures.  Provides only a single method, element(), which returns a
 * reference to the Object stored at this Position.
 */

public interface Position      {

    /**
     * This method returns a reference to the Object which is stored within
     * the Position
     * @return the Object stored within Position
     */
    public Object element();
}