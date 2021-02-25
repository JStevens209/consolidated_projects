import pandas as pd
import pprint as pp

problem = pd.read_csv( "/home/joshua/Documents/AOC_9_problem", delimiter='\n', names=[ "numbers" ] )
problem = problem[ "numbers" ]

working_numbers = {}
target_number = 400480901

for i in range( 25 ):
    working_numbers[ problem[i] ] = []

    for k in range( i + 1, 25 ):
        working_numbers[ problem[i] ].append( problem[i] + problem[k] )

for i in range( 25, len( problem ) ):
    working_numbers[ problem[i] ] = []
    found = False

    for k in range( i - 25, i ):
        working_numbers[ problem[k] ].append( problem[k] + problem[i] )

        if problem[i] in working_numbers[ problem[k] ]:
            found = True
    
    if not found:
        print( problem[i] )
        print( i )
        break

    working_numbers.pop( problem[ i - 25 ] )

