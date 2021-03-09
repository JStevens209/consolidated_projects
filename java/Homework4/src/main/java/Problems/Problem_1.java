package Problems;

import static java.lang.Integer.max;
import static java.util.Arrays.copyOfRange;

/**
 *
 * @author joshua
 * @description demonstration of a recursive function that returns the max of an array of size N.
 * 
 */
public class Problem_1 {
    public static void main(String[] args) {
        
        int[] array = { 1, 10, 3, 40, 5  };
        
        System.out.println( findMax( array ) );
    }
    
    static int findMax( int[] array ) {
        
        int max1 = 0;
        int max2 = 0;
        
        if( array.length > 2 ) {
            max1 = findMax( copyOfRange( array, 0, array.length/2 ) );
            max2 = findMax( copyOfRange( array, array.length/2, array.length ) );
        }
        else if( array.length > 1 ) {
             return max( array[0], array[1] );
        }
        else {
            return array[0];
        }
        
        
        return max( max1, max2 );
    }
}
