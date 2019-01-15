# Code for level translation of categorical variables in 2010 Census PUMS data.
#
# author: David Thaler
import pandas as pd

TEN =  ['Not in universe (vacant or GQ)',
        'Owned with a mortgage',
        'Owned free and clear',
        'Rented',
        'Occupied without payment of rent']

VACS = ['Not in universe (occupied or GQ)',
        'For rent',
        'Rented, not occupied',
        'For sale only',
        'Sold, not occupied',
        'For seasonal, recreational or occasional use',
        'For migrant workers',
        'Other vacant']

HHT = [ 'Not in universe (Vacant or GQ)',
        'Husband-wife family household',
        'Other family household: Male householder',
        'Other family household: Female householder',
        'Nonfamily household: Male householder, living alone',
        'Nonfamily household: Male householder, not living alone',
        'Nonfamily household: Female householder, living alone',
        'Nonfamily household: Female householder, not living alone']

PAOC = ['Not in universe (vacant or GQ)',
        'With own children under 6 years only',
        'With own children 6 to 17 years only',
        'With own children under 6 years and 6 to 17 years',
        'No own children under 18 years']

PARC = ['Not in universe (vacant or GQ)',
        'With related children under 6 years only',
        'With related children 6 to 17 years only',
        'With related children under 6 years and 6 to 17 years',
        'No related children under 18 years']

UPART = ['Not in universe (vacant or GQ)',
        'Male householder and male partner',
        'Male householder and female partner',
        'Female householder and female partner',
        'Female householder and male partner',
        'All other households']

MULTG = ['Not in universe (vacant or GQ)',
        'Not a multigenerational household',
        'Multigenerational household']

UNITTYPE = ['Housing unit', 'Group Quarters']

def add_key(d, key, values):
    d[key] = dict(zip(range(len(values)), values))


def housing_data_dict():
    out = {}
    add_key(out, 'TENURE', TEN)
    add_key(out, 'VACS', VACS)
    add_key(out, 'HHT', HHT)
    add_key(out, 'PAOC', PAOC)
    add_key(out, 'PARC', PARC)
    add_key(out, 'UPART', UPART)
    add_key(out, 'MULTG', MULTG)
    add_key(out, 'UNITTYPE', UNITTYPE)
    return out


def make_categorical(x, field, dd):
    if field in dd:
        return pd.Categorical(values=x[field].map(dd[field]), 
                categories=list(dd[field].values()))
    else:
        raise KeyError('Column name not in data dictionary.')
