import matplotlib.pyplot as plt
import csv

x = [[]]
initialized = False
with open( 'log.csv', 'r' ) as csvfile:

    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if initialized == False:
            initialized = True
            x = [[] for j in range(len(row))]

        for i in range( len( row ) ):
            x[ i ].append( float( row[ i ] ) )

for j in range( len( x ) - 1 ):
    plt.figure( j )
    plt.plot( x[ j + 1 ] )

plt.show()
