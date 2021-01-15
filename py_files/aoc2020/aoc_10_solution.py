import pandas as pd

problem = pd.read_csv( "/home/joshua/Documents/AOC_10_problem", sep="\n", names=["numbers"] )
problem = problem["numbers"].copy()

problem.sort_values( inplace= True, ignore_index= True )

# PART 1

one_num_diff = 0
three_num_diff = 0

for i in range( len( problem )):
    if ( i != ( len( problem ) - 1 )) and ( problem[ i + 1 ] - problem[ i ] == 1 ):
        one_num_diff += 1
    
    if (i != ( len( problem ) - 1 )) and ( problem[ i + 1 ] - problem[ i ] == 3 ):
        three_num_diff += 1

#print( (one_num_diff + 1) * (three_num_diff + 1))

# PART 2

def is_valid_sequence( sequence ):

    for i in range( len( sequence )):
        if i == 0 and sequence[i] > 3:
            return False
        elif i == 0 and sequence[i] <= 3:
            continue

        if (i != ( len( sequence ) - 1 )) and ( sequence[ i + 1 ] - sequence[i] > 3 ):
            return False
        elif (i != ( len( sequence ) - 1 )) and ( sequence[ i + 1 ] - sequence[i]  <= 3 ):
            continue
    
    if max( sequence ) != sequence[ len( sequence ) - 1 ]:
        return False

    return True

