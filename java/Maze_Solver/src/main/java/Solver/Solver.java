package Solver;

/**
 * @author joshua
 */

import Location.Location;
import java.util.*;
import ArrayQueue.Exceptions.*;
import ArrayQueue.ArrayQueue;

public class Solver {
	
	ArrayQueue queue;
	Location[][] maze;
	
	public static void main(String[] args) {
		
		Location endLoc = null;
		
		try {
			Solver mazeSolver = new Solver();
			
			while( endLoc == null ) {
				endLoc = mazeSolver.search();
			}
			
			mazeSolver.printPath( endLoc );
			
		}
		catch( InvalidDataException e ) {
			System.out.println( e.getMessage() );
		}
		catch( QueueEmptyException e ) {
			System.out.println( "Maze not solvable." );
		}
	
		
	}
	
	/**
	 * @throws ArrayQueue.Exceptions.InvalidDataException 
	 * @description Initializes the maze and queue with data from STDIN. Assumes correct input.
	 */
	public Solver() throws InvalidDataException {
		
		Scanner input = new Scanner( System.in );
	
		int rows = input.nextInt();
		int columns = input.nextInt();
		input.skip( "\n");
		
		maze = new Location[ rows ][ columns ];
		queue = new ArrayQueue<Location>( columns *  rows );

			
		for( int i = 0; i < rows; i++ ) {
			
			String nextLine = input.nextLine();
			
			for( int k = 0; k < columns; k++ ) {
				
				if( nextLine.substring(k, k+1).equals("S") ) {
					Location startingNode = new Location( 'S', 0, new int[]{i,k} );
					
					queue.enqueue( startingNode );
					maze[i][k] = startingNode;
				}
				else {
					maze[i][k] = new Location( nextLine.charAt(k), -1, new int[]{i,k} );
				}
				
			}
		}
	}
	/**
	 * @return If the finish location has not been found, returns NULL, if it has, return the finish location.
	 * @throws ArrayQueue.Exceptions.QueueEmptyException
	 * @throws ArrayQueue.Exceptions.InvalidDataException 
	 * @description Searches the area around the next active location for unexplored locations.
	 */
	public Location search() throws QueueEmptyException, InvalidDataException {
		
		// Gets the next active loc, if this throws QueueEmptyException, this means
		// there are no more explorable locations, therefore the maze is not solvable.
		Location activeLoc = (Location) queue.dequeue();
		
		int[] pos = activeLoc.getPos();
		int y = pos[0];
		int x = pos[1];
		
		// If the active node is the finish node, the path has been found, return.
		if( activeLoc.getType() == 'T' ) {
			return activeLoc;
		}
		
		// Each of these if statements check in the 4 directions surrounding the active loc.
		// If a loc that has not been found before, is found, then change it's distance and add it to the queue.
		
		if( ( y + 1 < maze.length ) && !( maze[y + 1][x].getType() == 'X' ) && ( maze[y + 1][x].distance == -1 ) ) {
			
			maze[y + 1][x].distance = activeLoc.distance + 1;
			queue.enqueue( maze[y + 1][x] );
		}
		if( ( y - 1 >= 0 ) && !( maze[y - 1][x].getType() == 'X' ) && ( maze[y - 1][x].distance == -1 ) ) {
			
			maze[y - 1][x].distance = activeLoc.distance + 1;
			queue.enqueue( maze[y - 1][x] );
		}
		if( ( x + 1 < maze[0].length ) && !( maze[y][x + 1].getType() == 'X' ) && ( maze[y][x + 1].distance == -1 ) ) {
			
			maze[y][x + 1].distance = activeLoc.distance + 1;
			queue.enqueue( maze[y][x + 1] );
		}
		if( ( x - 1 >= 0) && !( maze[y][x - 1].getType() == 'X' ) && ( maze[y][x - 1].distance == -1 ) ) {
			
			maze[y][x - 1].distance = activeLoc.distance + 1;
			queue.enqueue( maze[y][x - 1] );
		}
		
		return null;	
	}
	
	/**
	 * @param endLoc The location object that the path prints up to.
	 * @description Recursively prints the path from the start location (declared in constructor) to endLoc.
	 */
	public void printPath( Location endLoc ) {
		
		int[] pos = endLoc.getPos();
		int y = pos[0];
		int x = pos[1];
		
		// Looks around the loc in 4 directions, if there is a loc with a lower distance, move to that one.
		if( ( y + 1 < maze.length ) && ( maze[y + 1][x].distance != -1 ) && ( maze[y + 1][x].distance < endLoc.distance )){
			this.printPath( maze[y + 1][x] );
		}
		else if( ( y - 1 >= 0) && ( maze[y - 1][x].distance != -1 ) && ( maze[y - 1][x].distance < endLoc.distance ) ) {
			this.printPath( maze[y - 1][x] );
		}
		else if( ( x + 1 < maze[0].length ) && ( maze[y][x + 1].distance != -1 ) && ( maze[y][x + 1].distance < endLoc.distance ) ) {
			this.printPath( maze[y][x + 1] );
		}
		else if( ( x - 1 >= 0 ) && ( maze[y][x - 1].distance != -1 ) && ( maze[y][x - 1].distance < endLoc.distance ) ) {
			this.printPath( maze[y][x - 1]);
		}

		// Prints the current position. Since this comes after recursive calls, it will print in reverse order.
		System.out.println( "<" + y + " " + x + ">" );
		if( endLoc.getType() == 'T' ) {
			System.out.println( "Total distance = " + endLoc.distance );
		}
		
		return;
	}
		
	
}
