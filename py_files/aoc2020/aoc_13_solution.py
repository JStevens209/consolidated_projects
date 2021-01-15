earliest_time = 1000340
bus_ids = [ 13, 37, 401, 17, 19, 23, 29, 613, 41 ]

min_time = earliest_time * max( bus_ids )
early_id = 0

for i in range( len( bus_ids )):
    if ( ( int( earliest_time / bus_ids[i] ) * bus_ids[i] ) >= earliest_time ) and ( ( earliest_time % bus_ids[i] ) < min_time ):
        min_time = earliest_time + ( earliest_time % bus_ids[i] )
        early_id = bus_ids[i]

print( earliest_time )
print( early_id )
