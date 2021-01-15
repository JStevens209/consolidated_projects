
import pandas as pd
import numpy as np

problem = pd.read_csv( "/home/joshua/Documents/AOC_8_problem", sep=" ", names=[ "instruction", "integer" ] )

instructions = problem[ 'instruction' ]
integers = problem[ 'integer' ]


for j in range( len( instructions )):

    if instructions[j] == "jmp":
        instructions[j] = "nop"

    elif instructions[j] == "nop":
        instructions[j] = "jmp"

    elif instructions[j] == "acc":
        continue

    accumulator = 0
    i = 0
    indexes = []

    while i < len( instructions ):
        if instructions[i] == "acc":
            accumulator += int( integers[i] )

        if instructions[i] == "jmp":
            i += int( integers[i] )

        else:
            i += 1

        if i in indexes:
            break

        if instructions[i] == "end":
            print( accumulator )

        indexes.append( i )
     
    if instructions[j] == "jmp":
        instructions[j] = "nop"

    elif instructions[j] == "nop":
        instructions[j] = "jmp"

