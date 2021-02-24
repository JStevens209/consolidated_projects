package numeric;

public class GCD {

    public static void main( String[] args ) {

        if( args.length == 2 ) {

            var x = Integer.parseInt( args[0] );
            var y = Integer.parseInt( args[1] );

            System.out.println( Compute( x, y ) );

            return;
        }
    }

    // Uses recursion to calculate the GCD.
    // If y is 0, GCD is found, exit recursion with answer.
    public static int Compute( int x, int y ) {

        if( y != 0 ) {
            x = Compute( y, ( x % y ) );
        }

        if( x < 0 ) {
            x = -x;
        }
        return x;
    }
}