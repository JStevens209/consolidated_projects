package Stack;

import PositionList;

public class Stack<E> {

    PositionList<Object> stack;

    private static void main() {
        PositionList<Object> stack = new PositionList<Object>();
    }

    public E pop() throws StackEmptyException {
        if( stack.isEmpty() ) {
            throw new StackEmptyException( "Cannot pop from empty stack." );
        }

        return (E) stack.remove( stack.first() );
        
    }

    public <E> void push( E element ) {

        try {
            stack.addBefore( stack.first(), element );
        }
        catch( IllegalArgumentException e ) {
            System.out.println( e );
        }
    }

    public E first() {
        if( stack.isEmpty() ) {
            throw new StackEmptyException( "There are no elements in stack" );
        }

        E temp = pop();
        push( temp );

        return temp;
    }

    public <E> bool isEmpty() {
        return stack.isEmpty();
    }

    public static class StackEmptyException extends Exception {
		public StackEmptyException( String e ) {
			super(e);
		}
	}
};