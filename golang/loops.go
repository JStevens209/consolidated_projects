package loops
import (
	"fmt"	
)

// Just testing out things Im learning.
func main() {

	var testArray = [10] int{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 }

	for i := 0; i < len( testArray ); i++ {
		if ( testArray[i] % 10 ) != 0 {
			fmt.Print( testArray[i], "\n" )
		}
		
	}
}