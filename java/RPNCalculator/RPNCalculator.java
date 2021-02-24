package RPNCalculator;

import java.util.Scanner;

public class RPNCalculator {

    public static void main(String[] args) {
    }

    private static double Compute ( String input ) {
        
        // Declares the list of possible operations the function can handle.
        final String OPERATIONS = "+-*/";

        Scanner scan = new Scanner( input );
        Stack stack = new Stack();

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
                    throw InvalidRPNString( "ERROR: String Contains Unparsable Character: \"" + otherTemp + "\"");
                } 
                // Error Checking for a string that does not give enough numbers to do an operation on.
                if( stack.size() < 2 ) {
                    throw InvalidRPNString( "ERROR: String Is Unsolvable At Operation: \"" + operation + "\"" );  
                }
                
                // The Right Hand Side of the equation will always have been put in last
                // so must be pulled out first according to LIFO. Then the Left Hand Side can be pulled.
                rhs = stack.pop();
                lhs = stack.pop();
                
                // Perform Requested Operation
                if( operation == "+" ) {
                    stack.push( lhs + rhs );
                }

                if( operation == "-" ) {
                    stack.push( lhs - rhs );
                }

                if( operation == "*" ) {
                    stack.push( lhs * rhs );
                }

                if( ( operation == "/" ) && ( rhs != 0 ) ) {
                    stack.push( lhs / rhs );
                }
                // Error Handling for division by zero.
                else {
                    throw InvalidRPNString( "ERROR: Divide By Zero: \"" + lhs + " / 0\"" );
                }
            }
        }

        if( stack.size() > 1 ) {
            throw InvalidRPNString( "ERROR: String Is Unsolvable, Ran Out Of Operations" );
        }

        return stack.pop();
    }

    public static class InvalidRPNString extends RuntimeException {
        public InvalidRPNString( String e ) {
            super(e);
        }
    }
}