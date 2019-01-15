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

CHLD = ['Not in universe (vacant or GQ)',
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

def housing_data_dict():
    out = {}
    out['TENURE']  = dict(zip(range(len(TEN)), TEN))
    out['VACS'] = dict(zip(range(len(VACS)), VACS))
    out['HHT']  = dict(zip(range(len(HHT)), HHT))
    out['PAOC'] = dict(zip(range(len(CHLD)), CHLD))
    out['PARC'] = dict(zip(range(len(CHLD)), CHLD))
    out['UPART'] = dict(zip(range(len(UPART)), UPART))
    out['MULTG'] = dict(zip(range(len(MULTG)), MULTG))
    out['UNITTYPE'] = dict(zip(range(len(UNITTYPE)), UNITTYPE))
    return out

def make_categorical(x, field, dd):
        if field in dd:
            return pd.Categorical(values=x[field].map(dd[field]), 
                                    categories=list(dd[field].values()))
        else:
            raise KeyError('Column name not in data dictionary.')
