/**
 * @Author Joshua Stevens
 */
package RPNCalculator;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 *
 * @author joshua
 */
public class RPNCalculatorTest {
    
    public RPNCalculatorTest() {
    }

    /**
     * Test of Compute method, of class RPNCalculator.
     */
    @Test
    public void testExpectedBasicInput() {
        
        // Ensures each individual operation works.     
        assertEquals( RPNCalculator.Compute( "2 2 +" ), 4.0 );
        assertEquals( RPNCalculator.Compute( "3 2 -" ), 1.0 );
        assertEquals( RPNCalculator.Compute( "3 3 *" ), 9.0 );
        assertEquals( RPNCalculator.Compute( "9 3 /" ), 3.0 );
    }
    
    /**
     * Further Tests of the Compute method logic in class RPNCalculator.
     */
    @Test
    public void testExpectedAdvancedInput() {
        
        System.out.println( "Advanced Input" );
        
        // Misc tests for whether 0/2 also throws Divide By Zero, and if the program can handle negatives.
        assertEquals( RPNCalculator.Compute( "0 2 /" ), 0.0 );
        assertEquals( RPNCalculator.Compute( "-2 2 +" ), 0.0 );
        
        // Tests Multiplication and Addition together, specifically tests for if operations get done at the right times
        assertEquals( RPNCalculator.Compute( "2 2 3 + *" ), ( 2.0 + 3.0 ) * 2.0 );
        assertEquals( RPNCalculator.Compute( "2 2 + 3 *" ), ( 2.0 + 2.0 ) * 3.0 );
        
        // Tests Division and Subtraction together, specifically tests if numbers are used in the right order,
        // as division and subtraction are not the same backwards and forewards.
        assertEquals( RPNCalculator.Compute( "2 2 3 / -" ), 2.0 - ( 2.0 / 3.0 ) );
        assertEquals( RPNCalculator.Compute( "8 2 / 3 -" ), ( 8.0 / 2.0 ) - 3.0 );
    }

    /**
     * Tests Compute method in class RPNCalculator for expected errors.
     */
    @Test
    public void testExpectedErrors() {
        
        // Checks for Divide By Zero Exception
        assertThrows( RPNCalculator.InvalidRPNString.class,
                () -> RPNCalculator.Compute( "2 0 /" ), "ERROR: Divide by Zero: \"2 / 0\"" );
        
        // Checks for Unsolvable Equations Exception
        assertThrows( RPNCalculator.InvalidRPNString.class, 
                () -> RPNCalculator.Compute( "2 2 + *" ), "ERROR: String Is Unsolvable At Operation: \"+\"" );
        
        // Checks for Invalid Input Exception
        assertThrows( RPNCalculator.InvalidRPNString.class, 
                () -> RPNCalculator.Compute( "2 2 ^" ), "ERROR: String Contains Unparsable Character: \"^\"" );       
    }
    
}
