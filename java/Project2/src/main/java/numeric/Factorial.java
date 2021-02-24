package numeric;

public class Factorial {

    public static void main( String[] args ) {

        if( args.length == 1 ) {
            try {
                int x = Integer.parseInt( args[0] );
                double output = Compute( x );

                // If compute did not return the error code (-1.0), print output
                if( output > 0 ) {
                    System.out.println( output );
                }
            }
            catch( NegativeNumberException e ) {
                System.out.println( e );
                return;
            }
        }
    }
    
    public static double Compute( int x ) throws NegativeNumberException {

        double output = x;

        // If input > 0, calculate factorial iteratively
        if( x > 0 ) {

            for( int i = 1; i <= x; i++ ) {

                output = output * i;
            }
        }
        // If input < 0, throw error, program cannot handle negative numbers.
        else if( x < 0 ) {
            throw new NegativeNumberException( "ERROR: Input Cannot Be Negative" );
            
        }
        // If input is 0, 0! is defined to be 1
        else {
            output = 1;
        }

        return output;

    }
    
    // Adds a new exception to handle user input of negative numbers.
    public static class NegativeNumberException extends Exception {
        public NegativeNumberException( String errorMessage ) {
            super( errorMessage );
        }
    }
}
