package project7;

/**
 * Title:        Project #7
 * Description:
 * Copyright:    Copyright (c) 2001
 * Company:
 * @author
 * @version 1.0
 */

public class IntegerComparator implements Comparator {

    public IntegerComparator() {
    }

    public boolean isLessThan (Object obj1, Object obj2) 
				throws InvalidObjectException {
        if (! isComparable(obj1) || ! isComparable(obj2)) {
		    throw new InvalidObjectException ("Object not an integer");
		}
		
		Integer myInt1;
        Integer myInt2;
        myInt1 = (Integer) obj1;
        myInt2 = (Integer) obj2;

        return ( myInt1.intValue() < myInt2.intValue() );
    }

    public boolean isLessThanOrEqualTo (Object obj1, Object obj2) 
				throws InvalidObjectException{
        return ( ! isLessThan (obj2, obj1) );
    }

    public boolean isGreaterThan (Object obj1, Object obj2)
				throws InvalidObjectException {
        return ( isLessThan (obj2, obj1) );
    }

    public boolean isGreaterThanOrEqualTo (Object obj1, Object obj2) 
				throws InvalidObjectException {
        return ( ! isLessThan (obj1, obj2) );
    }

    public boolean isEqual (Object obj1, Object obj2) 
				throws InvalidObjectException {
        return ( (! isLessThan (obj1, obj2)) && (! isLessThan (obj2, obj1)) );
    }

    public boolean isComparable (Object obj) {
        return (obj instanceof Integer);
    }
}