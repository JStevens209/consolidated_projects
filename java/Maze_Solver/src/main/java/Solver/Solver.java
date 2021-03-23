/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


package Solver;

/**
 *
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
			System.out.println( e.getMessage() );
		}
	
		
	}
	
	public Solver() throws InvalidDataException {
		Scanner input = new Scanner( System.in );
	
		int columns = input.nextInt();
		int rows = input.nextInt();
		input.skip( "\n");
		
		maze = new Location[ columns ][ rows ];
		queue = new ArrayQueue<Location>( columns *  rows );

			
		for( int i = 0; i < rows; i++ ) {
			
			String nextLine = input.nextLine();
			
			for( int k = 0; k < columns; k++ ) {
				
				if( nextLine.substring(k, k+1).equals("S") ) {
					Location startingNode = new Location( "S", 0, new int[]{i,k} );
					
					queue.enqueue( startingNode );
					maze[i][k] = startingNode;
				}
				else {
					maze[i][k] = new Location( nextLine.substring(k,k+1), -1, new int[]{i,k} );
				}
				
			}
		}
	}
	
	public Location search() throws QueueEmptyException, InvalidDataException {
		
		Location activeLoc = (Location) queue.dequeue();
		
		int[] pos = activeLoc.getPos();
		int y = pos[0];
		int x = pos[1];
		
		if( activeLoc.getType().equals( "T" ) ) {
			return activeLoc;
		}
		
		if( ( y + 1 < maze.length ) && !( maze[y + 1][x].getType().equals("X") ) && ( maze[y + 1][x].distance == -1 ) ) {
			
			maze[y + 1][x].distance = activeLoc.distance + 1;
			queue.enqueue( maze[y + 1][x] );
		}
		if( ( y - 1 >= 0 ) && !( maze[y - 1][x].getType().equals("X") ) && ( maze[y - 1][x].distance == -1 ) ) {
			
			maze[y - 1][x].distance = activeLoc.distance + 1;
			queue.enqueue( maze[y - 1][x] );
		}
		if( ( x + 1 < maze[0].length ) && !( maze[y][x + 1].getType().equals("X") ) && ( maze[y][x + 1].distance == -1 ) ) {
			
			maze[y][x + 1].distance = activeLoc.distance + 1;
			queue.enqueue( maze[y][x + 1] );
		}
		if( ( x - 1 >= 0) && !( maze[y][x - 1].getType().equals("X") ) && ( maze[y][x - 1].distance == -1 ) ) {
			
			maze[y][x - 1].distance = activeLoc.distance + 1;
			queue.enqueue( maze[y][x - 1] );
		}
		
		return null;	
	}
	
	public void printPath( Location endLoc ) {
		
		int[] pos = endLoc.getPos();
		int y = pos[0];
		int x = pos[1];
		
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

		System.out.println( "<" + y + " " + x + ">" );
		if( endLoc.getType().equals("T") ) {
			System.out.println( "Total distance = " + endLoc.distance );
		}
		
		return;
	}
		
	
}
