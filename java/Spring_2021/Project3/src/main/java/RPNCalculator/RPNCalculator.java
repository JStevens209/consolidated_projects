/**
 * @Author: Joshua Stevens
 */

package RPNCalculator;

import java.util.Scanner;

public class RPNCalculator {

    public static void main(String[] args) {
    }

    public static double Compute ( String input ) {
        
        // Declares the list of possible operations the function can handle.
        final String OPERATIONS = "+-*/";

        Scanner scan = new Scanner( input );
        java.util.Stack stack = new java.util.Stack();

        double lhs;
        double rhs;
        String operation;

        while ( scan.hasNext() ) {
            
            if( scan.hasNextDouble() ) {
                stack.push( scan.nextDouble() );
            }
            else {
                operation = scan.next();
                
                // Error Checking for unexpected characters. IE "hi" of "+-"
                if( ( !OPERATIONS.contains( operation ) ) && ( operation.length() == 1 ) ) {
                    throw new InvalidRPNString( "ERROR: String Contains Unparsable Character: \"" + operation + "\"");
                } 
                // Error Checking for a string that does not give enough numbers to do an operation on.
                if( stack.size() < 2 ) {
                    throw new InvalidRPNString( "ERROR: String Is Unsolvable At Operation: \"" + operation + "\"" );  
                }
                
                // The Right Hand Side of the equation will always have been put in last
                // so must be pulled out first according to LIFO. Then the Left Hand Side can be pulled.
                rhs = (Double) stack.pop();
                lhs = (Double) stack.pop();
                
                double hold;
                
                // Perform Requested Operation
                if( "+".equals( operation ) ) {
                    stack.push( lhs + rhs );
                }

                else if( "-".equals( operation ) ) {
                    stack.push( lhs - rhs );                    
                }

                else if( "*".equals( operation ) ) {
                    stack.push( lhs * rhs );
                }

                else if( ( "/".equals( operation ) ) && ( rhs != 0 ) ) {
                    stack.push( lhs / rhs );                    
                }
                // Error Handling for division by zero.
                else {
                    throw new InvalidRPNString( "ERROR: Divide By Zero: \"" + lhs + " / " + rhs + "\"" );
                    
                }
            }
        }

        if( stack.size() > 1 ) {
            throw new InvalidRPNString( "ERROR: String Is Unsolvable, Ran Out Of Operations" );
        }

        return (Double) stack.pop();
    }

    public static class InvalidRPNString extends RuntimeException {
        public InvalidRPNString( String e ) {
            super(e);
        }
    }
}