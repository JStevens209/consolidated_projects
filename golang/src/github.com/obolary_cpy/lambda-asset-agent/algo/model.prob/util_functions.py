import pandas as pd
import numpy as np 

def zigzag( s, pct=0.04 ):
    
    ut = 1 + pct
    dt = 1 - pct

    ld = s.index[0]
    lp = s.C[ld]
    tr = None

    zzd, zzp, zzt = [ld], [lp], [0]

    for ix, ch, cl in zip(s.index, s.H, s.L):
        # No initial trend
        if tr is None:
            if ch / lp > ut:
                tr = 1
            elif cl / lp < dt:
                tr = -1
        # Trend is up
        elif tr == 1:
            # New H
            if ch > lp:
                ld, lp = ix, ch
            # Reversal
            elif cl / lp < dt:
                zzd.append(ld)
                zzp.append(lp)
                zzt.append(tr)

                tr, ld, lp = -1, ix, cl
        # Trend is down
        else:
            # New L
            if cl < lp:
                ld, lp = ix, cl
            # Reversal
            elif ch / lp > ut:
                zzd.append(ld)
                zzp.append(lp)
                zzt.append(tr)

                tr, ld, lp = 1, ix, ch

    # Extrapolate the current trend
    if zzd[-1] != s.index[-1]:
        zzd.append(s.index[-1])

        if tr is None:
            zzp.append(s.C[zzd[-1]])
            zzt.append(0)
        elif tr == 1:
            zzp.append(s.H[zzd[-1]])
            zzt.append(1)
        else:
            zzp.append(s.L[zzd[-1]])
            zzt.append(-1)
            
    df = pd.DataFrame( index=zzd, columns=['ZZ','ZT'] )
    df['ZZ'] = zzp
    df['ZT'] = zzt
    return df


def histzigzag(hist,edges):

    izigzag = [edges[0]]
    zigzag = [hist[0]]

    lastimax = edges[0]
    lastimin = edges[0]

    lastmax = zigzag[-1]
    lastmin = zigzag[-1]

    islastmax = False
    islastmin = False

    zigdir = 0
    zigscale = 0.01
    for j in range( len( hist ) ):

        if hist[j] > zigzag[-1] * (1 + zigscale):

            if islastmax:
                if hist[j] > lastmax:
                    print( '** max search', hist[j], '>', zigzag[-1] * (1 + zigscale) )
                    lastmax = hist[j]
                    lastimax = edges[j]
                    islastmax = True
            else:
                print( '** max search', hist[j], '>', zigzag[-1] * (1 + zigscale) )
                lastmax = hist[j]
                lastimax = edges[j]
                islastmax = True

            if zigdir <= 0 and islastmin:
                print('>> save min', lastmin, lastimin)
                zigzag.append(lastmin)
                izigzag.append(lastimin)
                zigdir = 1
                islastmin = False

        if islastmax and hist[j] < lastmax * (1 - zigscale) and zigdir >= 0:
            print('>> save max', lastmax, lastimax)
            zigzag.append(lastmax)
            izigzag.append(lastimax)
            zigdir = -1
            islastmax = False

        if hist[j] < zigzag[-1] * (1 - zigscale):

            if islastmin:
                if hist[j] < lastmin:
                    print( '** min search', hist[j], '<', zigzag[-1] * (1 - zigscale) )
                    lastmin = hist[j]
                    lastimin = edges[j]
                    islastmin = True
            else:
                print( '** min search', hist[j], '<', zigzag[-1] * (1 - zigscale) )
                lastmin = hist[j]
                lastimin = edges[j]
                islastmin = True

            if zigdir >= 0 and islastmax:
                print('>> save max', lastmax, lastimax)
                zigzag.append(lastmax)
                izigzag.append(lastimax)
                zigdir = -1
                islastmax = False

        if islastmin and hist[j] > lastmin * (1 + zigscale) and zigdir <= 0:
            print('>> save min', lastmin, lastimin)
            zigzag.append(lastmin)
            izigzag.append(lastimin)
            zigdir = 1
            islastmin = False 

    return zigzag, izigzag
    