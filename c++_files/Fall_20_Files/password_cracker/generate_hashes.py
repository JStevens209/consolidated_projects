import hashlib as hsh
import pandas as pd
import numpy as np


wordlist = pd.read_csv( "./wordlists/l33t_wordlist.txt", sep= '\n' )
hashlist = pd.read_csv( "./PA4-Hashes.txt", sep= ':', names= [ 'name', 'salt', 'hash' ] )

col = wordlist.loc(0)
salts = hashlist[ 'salt' ]

for i in range( len( wordlist )):
    #for j in range( len( salts[ 9: ])):
    col[i] = hsh.md5( ( col[i][0] ).encode( 'utf-8' )).hexdigest()

#wordlist = wordlist.drop_duplicates()
wordlist.to_csv( "./wordlists/output.txt", index= False, sep= '\n' )

