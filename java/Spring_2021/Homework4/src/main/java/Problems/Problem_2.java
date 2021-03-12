/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Problems;

import static java.lang.Math.ceil;
import static java.lang.Math.pow;

/**
 *
 * @author joshua
 * @description This question is worded REALLY poorly. I mean like, there are half
 * million ways to interpret the wording. I am taking it to mean that it wants me to 
 * take a string full of integers, then parse each character recursively, which is really dumb.
 */
public class Problem_2 {
    public static void main(String[] args) {
        
		int answer = parseIntRecursively( "1234" );
		
		System.out.println( answer );
    }
    
    static int parseIntRecursively( String intString ) {
        
        int answer = 0;
        
        if( intString.length() > 1 ) {
			answer = parseIntRecursively( intString.substring( 1 ) );
        }
		
		if( answer > 0 ) {
			// The way this works is, there is a theorem that the number of digits in a number is equal to
			// the floor of log base 10 of n. Then I just raise 10 to the power of however many digits there are
			// to get a number that is a power of 10 above the previous number. The only case this does not work
			// is when the answer is 0, in which case, log base 10 is undefined.
			answer += Integer.parseInt( intString.substring( 0, 1 ) ) * pow( 10.0, Math.floor( Math.log10( answer ) + 1.0 ) );
		}
		else {
			answer = Integer.parseInt( intString.substring( 0, 1 ));
		}
        
		
        return answer; 
    }
}
