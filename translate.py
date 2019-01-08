# Code for level translation of categorical variables in 2010 Census PUMS data.
#
# author: David Thaler

TEN =  ['Not in universe (vacant or GQ)',
        'Owned by you or someone in this household with a mortgage or loan',
        'Owned by you or someone in this household free and clear (without a mortgage or loan)',
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

def get_data_dict():
    out = {}
    out['HHT'] = dict(zip(range(len(HHT)), HHT))
    return out