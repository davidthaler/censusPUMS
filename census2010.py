# Load housing records for 2010 Census from the fixed-width file format provided.
# 
# author: David Thaler
import pandas as pd

# Housing record column names from PUMS documentation
HOUSE_COLNAMES = ['RECTYPE', 'SERIALNO', 'STATE', 'REGION', 'DIVISION', 
                  'PUMA', 'TOTAREA', 'LANDAREA', 'SUBSAMPL', 'HWEIGHT',
                  'PERSONS', 'UNITTYPE', 'HSUBFLG', 'VACS', 'VACSA', 
                  'TENURE', 'TENUREA', 'HHT', 'P60', 'P65', 'P18', 'NPF',
                  'NOCH', 'NRCH', 'PAOC', 'PARC', 'UPART', 'MULTG']

# 1-based column start index in housing record from PUMS documentation
HOUSE_COLSTART1 = [1, 2, 9, 11, 12, 13, 18, 32, 46, 48, 50, 52, 
                   53, 54, 55, 56, 57, 58, 59, 61, 63, 65, 67, 
                   69, 71, 72, 73, 74]

# Person record column names from PUMS documentation
PERSON_COLNAMES = ['RECTYPE', 'SERIALNO', 'PNUM', 'PSUB', 'RELATE', 
                   'RELATEA', 'OC', 'RC', 'SEX', 'SEXA', 'SSPA', 'AGE',
                   'AGEA', 'QTRBIR', 'HISPAN', 'HISPANA', 'NUMRACE',
                   'WHITE', 'BLACK', 'AIAN', 'ASIAN', 'NHAW', 'OPI', 
                   'OTHER', 'RACESHORT', 'RACEDET', 'RACECHKBX', 'RACEA',
                   'GQTYP', 'GQTYPA']

# 1-based column start index in person record from PUMS documentation
# NB: this includes the end index of the data (as the start of the padding)
PERSON_COLSTART1 = [1, 2, 9, 11, 14, 16, 17, 18, 19, 20, 21, 22, 24,
                    25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 
                    39, 41, 44, 45, 46, 47]

def load_person10(path, chunksize=None):
    person_colstart0 = [x-1 for x in PERSON_COLSTART1]
    person_colspec = list(zip(person_colstart0[:-1], person_colstart0[1:]))
    data = pd.read_fwf(path, colspecs=person_colspec, names=PERSON_COLNAMES, 
                       chunksize=chunksize)
    return data

def load_housing10(path, chunksize=None):
    '''
    Load housing data from 2010 Census fixed-width files and return.
    Returns either chunk iterator of size chunksize or a data frame with all
    data if chunksize is None

    Args:
        path: string path to the data
        chunksize: int or None. If None, return all data in a data frame.
            If int, return iterator over chunks with size of chunksize.

    Returns:
        either a Pandas data frame or a chunk iterator
    '''
    # 0 - based column start indices
    house_start = [x-1 for x in HOUSE_COLSTART1]
    house_end = house_start[1:] + [75]
    house_colspec = list(zip(house_start, house_end))
    data = pd.read_fwf(path, colspecs=house_colspec, names=HOUSE_COLNAMES,
                       chunksize=chunksize)
    return data
