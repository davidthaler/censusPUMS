# Functions for computing statistics on Census PUMS data
#
# author: David Thaler
import pandas as pd
import census2010


def total(x):
    '''
    Computes a total of housing units or people from census data.
    Filter x to estimate size of a subset.

    Args:
        x: person or housing data frame

    Returns:
        estimated number of people or housing units represented by x
    '''
    if 'HWEIGHT' in x.columns:
        return x.HWEIGHT.sum()
    else:
        return 10 * len(x)


def total_cond(x, cond):
    '''
    Computes the population or housing unit count of a subset of x,
    based on a condition expressed as a lambda that is True for rows
    in x that are in the subset.

    Args:
        x: person or housing data frame
        cond: a lambda that is True for the numerator of the proportion

    Returns:
        estimate of population or housing unit count in a subset of x
    '''
    idx = x.apply(cond, axis=1)
    return total(x[idx])


def proportion_df(subset, universe):
    '''
    Computes the housing unit or population proportion of x in a subset.
    The subset is described by a lambda that is True for rows in x that
    are in the subset.

    Args:
        subset: a data frame containing a subset of the universe
        universe: a housing or population data frame

    Returns:
        proportion of the universe in the subset
    '''
    num = total(subset)
    den = total(universe)
    if den==0:
        raise ZeroDivisionError('Universe size is zero')
    return num / den


def proportion_cond(x, cond):
    '''
    Computes the housing unit or population proportion of x in a subset.
    The subset is described by a lambda that is True for rows in x that
    are in the subset.

    Args:
        x: person or housing data frame
        cond: a lambda that is True for the numerator of the proportion

    Returns:
        the population or housing unit proportion of x in a subset
    '''
    idx = x.apply(cond, axis=1)
    return proportion_df(x[idx], x)


def tabulate(x, field, dd=None):
    '''
    Groups x by field and tabulates totals.
    If the data dictionary, dd, is provided the levels are renamed using it.
    Do not use dd if the field was translated with census2010.make_categorical.

    Args:
        x: person or housing data frame
        field: string name of field to group by
        dd: optional data dictionary for renaming the tabulation labels

    Returns:
        totals tabulated within levels of field
    '''
    if dd is not None:
        cat_var = census2010.make_categorical(x, field, dd)
        gp = x.groupby(cat_var)
    else:
        gp = x.groupby(field)
    return gp.apply(total)


def tabulate_proportion(x, field, dd=None):
    '''
    Groups x by field and tabulates group proportions.
    If the data dictionary, dd, is provided the levels are renamed using it.
    Do not use dd if the field was translated with census2010.make_categorical.

    Args:
        x: person or housing data frame
        field: string name of field to group by
        dd: optional data dictionary for renaming the tabulation labels

    Returns:
        group size proportions tabulated within levels of field
    '''
    return tabulate(x, field, dd) / total(x)


def crosstab(x, row, col, dd, proportion=False):
    '''
    Groups x by fields row and col and cross-tabulates totals (default) or
    proportions by cell. If the data dictionary is provided, then row or col
    are replaced with categoricals named acccording to dd.

    Args:
        x: person or housing data frame
        row: string name of field for row-groups
        col: string name of field for column-groups
        dd: optional data dictionary for renaming the tabulation labels
        proportion: default False, if True, return proportions, else totals

    Returns:
        a pandas data frame containing the cross-tabulation
    '''
    if row not in x.columns:
        raise IndexError('Row name not in data dictionary.')
    if col not in x.columns:
        raise IndexError('Column name not in data dictionary.')
    fields = set(dd.field)
    if row in fields:
        rowvar = census2010.make_categorical(x, row, dd)
    else:
        rowvar = x[row]
    if col in fields:
        colvar = census2010.make_categorical(x, col, dd)
    else:
        colvar = x[col]
    if 'HWEIGHT' in x.columns:
        vals = x.HWEIGHT
    elif 'PWEIGHT' in x.columns:
        vals = x.PWEIGHT
    else:
        raise ValueError('No instance weight field present. Is this census data?')
    return pd.crosstab(index=rowvar, columns=colvar, values=vals,
                    aggfunc=sum, margins=True, normalize=proportion)
