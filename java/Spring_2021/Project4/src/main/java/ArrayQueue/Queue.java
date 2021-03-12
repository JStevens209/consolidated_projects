package ArrayQueue;

import ArrayQueue.Exceptions;
/**
 * @author joshua
 */
public interface Queue<E> {     
	public <E> void enqueue (E element) throws Exceptions.InvalidDataException;    
	public E dequeue () throws Exceptions.QueueEmptyException;    
	public E front () throws Exceptions.QueueEmptyException;    
	public int size();    
	public boolean isEmpty(); 
} 