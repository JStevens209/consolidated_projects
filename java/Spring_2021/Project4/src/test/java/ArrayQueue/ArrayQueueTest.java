package ArrayQueue;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import ArrayQueue.Exceptions.InvalidDataException;
import ArrayQueue.Exceptions.QueueEmptyException;
/**
 *
 * @author Joshua Stevens
 * @date 3/10/21
 */
public class ArrayQueueTest {
	
	public ArrayQueueTest() {
		
		
	}

	@Test
	public void testConstructor() throws Exception {
		
		assertThrows( InvalidDataException.class, () -> {
			ArrayQueue instance = new ArrayQueue(-1);
		});
	}
	/**
	 * Test of enqueue method, of class ArrayQueue.
	 */
	@Test
	public void testEnqueue() throws Exception {
		
		ArrayQueue<Integer> instance = new ArrayQueue(50);
		
		// Offset starting point by 23, a prime number, that is around half the size of the array.
		for( int i = 0; i < 23; i++ ) {
			instance.enqueue(i);
		}
		for( int i = 0; i < 23; i++ ) {
			instance.dequeue();
		}
		
		// Check enqueue, with some wraparound.
		// Array should be full, but not throw an error.
		for( int i = 0; i < 50; i++ ) {
			instance.enqueue(i);
		}
		for( int i = 0; i < 50; i++ ) {
			assertEquals( i, instance.dequeue() );
		}
		
		// Check growing of array, this should make it double twice.
		for( int i = 0; i < 200; i++ ) {
			instance.enqueue(i);
		}
		for( int i = 0; i < 200; i++ ) {
			assertEquals( i, instance.dequeue() );
		}
		
		// Checks for errors in size tracking with all these changes.
		assertEquals( 0, instance.size() );
		
		// Check for correct exceptions
		assertThrows( InvalidDataException.class, () -> {
			instance.enqueue( null );
		});
	}

	/**
	 * Test of dequeue method, of class ArrayQueue.
	 */
	@Test
	public void testDequeue() throws Exception {
		
		ArrayQueue<Integer> instance = new ArrayQueue(50);
		
		// Offset starting point by 23, a prime number, that is around half the size of the array.
		for( int i = 0; i < 23; i++ ) {
			instance.enqueue(i);
		}
		for( int i = 0; i < 23; i++ ) {
			instance.dequeue();
		}
		
		// Most of the testing is already accomplished in testEnqueue()
		
		// Testing exception cases
		
		assertThrows( QueueEmptyException.class, () -> {
			instance.dequeue();
		});
		
		instance.enqueue(1);
		instance.enqueue(2);
		
		instance.dequeue();
		instance.dequeue();
		assertThrows( QueueEmptyException.class, () -> {
			instance.dequeue();
		});
	}

	/**
	 * Test of front method, of class ArrayQueue.
	 * The code for front is almost exactly the same as dequeue(), except
	 * it does not get rid of the front object afterword.
	 */
	@Test
	public void testFront() throws Exception {
		
		ArrayQueue<Integer> instance = new ArrayQueue(50);
		
		assertThrows( QueueEmptyException.class, () -> {
			instance.dequeue();
		});
	}

	/**
	 * Test of size method, of class ArrayQueue.
	 * Test of isEmpty method, of class ArrayQueue.
	 */
	@Test
	public void testSize() throws Exception {
		
		ArrayQueue<Integer> instance = new ArrayQueue(10);
		
		// Offset starting point by 23, weird prime number.
		for( int i = 0; i < 23; i++ ) {
			instance.enqueue(i);
		}
		
		// isEmpty() check when array partially full.
		assertEquals( false, instance.isEmpty() );
		
		for( int i = 0; i < 23; i++ ) {
			instance.dequeue();
		}
		
		// Basic test cases of size() and isEmpty().
		assertEquals( 0, instance.size() );
		assertEquals( true, instance.isEmpty() );
		
		// Check size tracking through multiple growths of array.
		for( int i = 0; i < 200; i++ ) {
	
			assertEquals( i, instance.size() );
			instance.enqueue(i);
			assertEquals( false, instance.isEmpty() );
		}
		for( int i = 0; i < 200; i++ ) {
			
			assertEquals( 200 - i, instance.size() );
			instance.dequeue();
		}
		
	}

	
}
