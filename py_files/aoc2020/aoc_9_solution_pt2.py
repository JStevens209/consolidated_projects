import pandas as pd
import pprint as pp

problem = pd.read_csv( "/home/joshua/Documents/AOC_9_problem", delimiter='\n', names=[ "numbers" ] )
problem = problem[ "numbers" ]

target_number = 400480901

for i in range( len( problem )):

    accumulation = 0
    numbers = []

    while accumulation < target_number:
        accumulation += problem[i]
        numbers.append( problem[i] )
        i += 1
    

    if accumulation == target_number:
        print( min( numbers ) + max( numbers ) )