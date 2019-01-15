# Functions for computing statistics on Census PUMS data
import pandas as pd
import translate

def total(x):
    if 'HWEIGHT' in x.columns:
        return x.HWEIGHT.sum()
    else:
        return 10 * len(x)

def proportion_df(subset, universe):
    num = total(subset)
    den = total(universe)
    if den==0:
        raise ZeroDivisionError('Universe size is zero')
    return num / den

def proportion_cond(x, cond):
    idx = x.apply(cond, axis=1)
    return proportion_df(x[idx], x)

def tabulate(x, field, dd=None):
    if dd is not None:
        if field in dd:
            cat_var = translate.make_categorical(x, field, dd)
            gp = x.groupby(cat_var)
        else:
            raise KeyError('Column name not in data dictionary.')
    else:
        gp = x.groupby(field)
    return gp.apply(total)