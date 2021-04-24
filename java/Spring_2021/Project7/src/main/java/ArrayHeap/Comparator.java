package project7;

/**
 * Title:        Project #7
 * Description:
 * Copyright:    Copyright (c) 2001
 * Company:
 * @author
 * @version 1.0
 */

public interface Comparator {

    public boolean isLessThan (Object obj1, Object obj2) 
			throws InvalidObjectException;

    public boolean isLessThanOrEqualTo (Object obj1, Object obj2) 
			throws InvalidObjectException;

    public boolean isGreaterThan (Object obj1, Object obj2) 
			throws InvalidObjectException;

    public boolean isGreaterThanOrEqualTo (Object obj1, Object obj2) 
			throws InvalidObjectException;

    public boolean isEqual (Object obj1, Object obj2) 
			throws InvalidObjectException;

    public boolean isComparable (Object obj);
}