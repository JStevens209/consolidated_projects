/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package RPNTests;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import RPNCalculator.RPNCalculator;
/**
 *
 * @author joshua
 */
public class RPNCalculatorTests {
    
    public RPNCalculatorTests() {
    }

    @Test
    public void expectedBasicInputTest() {
        assertEquals( RPNCalculator.Compute( "2 2 +" ), 4.0 );
        assertEquals( RPNCalculator.Compute( "3 2 -" ), 1.0 );
        assertEquals( RPNCalculator.Compute( "3 3 *" ), 9.0 );
        assertEquals( RPNCalculator.Compute( "9 3 /" ), 3.0 );  
    }
    
    @Test
    public void expectedAdvancedInputTest() {
        assertEquals( RPNCalculator.Compute( "2 2 3 + *" ), 10.0 );
        assertEquals( RPNCalculator.Compute( "2 2 + 3 *" ), 12.0 );
        assertEquals( RPNCalculator.Compute( "2 2 3 / -" ), 10.0 );
    }

    // TODO add test methods here.
    // The methods must be annotated with annotation @Test. For example:
    //
    // @Test
    // public void hello() {}
}
