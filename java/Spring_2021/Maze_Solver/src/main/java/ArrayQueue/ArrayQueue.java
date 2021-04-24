package ArrayQueue;

import ArrayQueue.Exceptions;
/**
 * @author Joshua Stevens
 * @date 3/10/21
 */
public class ArrayQueue<E> implements Queue<E> { 
	
	Object[] queue;
	int front;
	int back;
	
	// In defense of this variable, it simplifies the code, no unnecessary calculations
	// no extra cost. Why calculate it every time with some weird, hard to read equation
	// when you can store it in a variable that is obvious what it is.
	int size;
	
	
	/**
	 * 
	 * @param initialSize: The initial size of the queue.
	 */
	public ArrayQueue( int initialSize ) throws Exceptions.InvalidDataException {
		
		if( initialSize <= 0 ) {
			throw new Exceptions.InvalidDataException( "Queue size must be greater than 0" );
		}
			
		queue = new Object[ initialSize ];
	
		front = 0;
		back = 0;
		size = 0;
	}
	
	/**
	 * 
	 * @param element: Element to be inserted into ArrayQueue. Must be of the same type as declared at declaration.
	 * @throws InvalidDataException: Thrown when NULL data passed in as element.
	 */
	public <E> void enqueue( E element ) throws Exceptions.InvalidDataException {
		
		// If there is not enough space to hold the data, grow the queue so it can fit.
		if( size >= queue.length ) {
			growQueue();
		}
		
		if( element == null ) {
			throw new Exceptions.InvalidDataException( "ERROR: Entered NULL as data." );
		}
		
		queue[ back ] = element;
		
		back = ( back + 1 ) % queue.length;
		size++;
	}
	
	/**
	 * 
	 * @return Returns the next item in the queue, removes the item from the queue. Adheres to FIFO principle.
	 * @throws QueueEmptyException: Thrown when attempting to dequeue from an empty queue.
	 */
	public E dequeue() throws Exceptions.QueueEmptyException {
		
		if( size <= 0 ) {
			throw new Exceptions.QueueEmptyException( "ERROR: Attempt to remove non-existent elements." );
		}
		
		E element = (E)queue[ front ];
		
		queue[ front ] = null;
		front = ( front + 1 ) % queue.length;
		size--;
		
		return element;
	}
	
	/**
	 * 
	 * @return Returns the front-most element of the queue, without popping it.
	 * @throws QueueEmptyException: Thrown when trying to access an empty queue.
	 */
	public E front() throws Exceptions.QueueEmptyException {
		
		if( size <= 0 ) {
			throw new Exceptions.QueueEmptyException( "ERROR: Attempted to access non-existent element." );
		}
		
		return (E)queue[ front ];
	}
	
	/**
	 * 
	 * @return Returns the size of the queue.
	 */
	public int size() {
		return size;
	}
	
	/**
	 * 
	 * @return Returns true if queue is empty, and returns false if queue still has elements remaining. 
	 */
	public boolean isEmpty() {
		if( size <= 0 ) {
			return true;
		}
		
		return false;
	}
	
	/**
	 * Private function to double the size of the queue, used by enqueue().
	 */
	private void growQueue() {
		
		// Creates a temporary queue that is double the size of the old queue.
		Object[] tempQueue = new Object[ queue.length * 2 ];
		
		// The front pointer marches foreward, putting each element in the array
		// in the proper order. 
		for( int i = 0 ; i < size; i++ ) {
			
			tempQueue[i] = queue[ front ];
			front = ( front + 1 ) % queue.length;
		}
		
		back = size;
		front = 0;
		
		// Sets the temporary queue to queue, size has been successfully doubled.
		queue = tempQueue;
	}
	
};
