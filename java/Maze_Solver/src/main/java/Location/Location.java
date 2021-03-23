/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Location;

/**
 *
 * @author joshua
 */
public class Location {
	
	// Need to be able to view and edit distance directly.
	public int distance;
	
	String type;
	int[] mazePos;
	
	public Location(String wall_type , int origin_distance, int[] position ) {
		
		type = wall_type;
		distance = origin_distance;
		mazePos = position;
	}
	
	public String getType() {
		return type;
	}
	
	public int[] getPos() {
		return mazePos;
	}
	
}
