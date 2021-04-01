package Solver;

/**
 *
 * @author Joshua Stevens
 * @purpose to hold all the necessary data of a maze location.
 */
public class Location {
	
	// Need to be able to view and edit distance directly.
	public int distance;
	
	char type;
	int[] mazePos;
	
	public Location(char wall_type , int origin_distance, int[] position ) {
		
		type = wall_type;
		distance = origin_distance;
		mazePos = position;
	}
	
	public char getType() {
		return type;
	}
	
	public int[] getPos() {
		return mazePos;
	}
	
}
