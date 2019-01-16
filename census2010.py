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
PERSON_COLNAMES = ['RECTYPE', 'SERIALNO', 'PNUM', 'PSUB', 'PWEIGHT', 'RELATE',
                   'RELATEA', 'OC', 'RC', 'SEX', 'SEXA', 'SSPA', 'AGE',
                   'AGEA', 'QTRBIR', 'HISPAN', 'HISPANA', 'NUMRACE',
                   'WHITE', 'BLACK', 'AIAN', 'ASIAN', 'NHAW', 'OPI', 
                   'OTHER', 'RACESHORT', 'RACEDET', 'RACECHKBX', 'RACEA',
                   'GQTYP', 'GQTYPA']

# 1-based column start index in person record from PUMS documentation
# NB: this includes the end index of the data (as the start of the padding)
PERSON_COLSTART1 = [1, 2, 9, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 24,
                    25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 
                    39, 41, 44, 45, 46, 47]


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


def load_person10(path, chunksize=None):
    '''
    Load population data from 2010 Census fixed-width files and return.
    Returns either chunk iterator of size chunksize or a data frame with all
    data if chunksize is None

    Args:
        path: string path to the data
        chunksize: int or None. If None, return all data in a data frame.
            If int, return iterator over chunks with size of chunksize.

    Returns:
        either a Pandas data frame or a chunk iterator
    '''
    person_colstart0 = [x-1 for x in PERSON_COLSTART1]
    person_colspec = list(zip(person_colstart0[:-1], person_colstart0[1:]))
    data = pd.read_fwf(path, colspecs=person_colspec, names=PERSON_COLNAMES,
                       chunksize=chunksize)
    return data


def person_subsample(housing_df, person_df):
    '''
    The Census housing record has a subsample field (SUBSAMPL) for computing
    group jackknife standard errors, but this field is not in the person data.
    The procedure is to exclude all persons in the excluded housing units.
    This function makes a column with the index of the person_df that maps on
    the housing unit SUBSAMPL by SERIALNO.

    To use this:
        person_df['SUBSAMPL'] = person_subsample(housing_df, person_df)

    Args:
        housing_df: pandas data frame of Census housing data, with SUBSAMPL
        person_df: data frame of Census person data, without SUBSAMPL

    Returns:
        pd.Series of subsample numbers that can be appended to person_df
    '''
    ss_dict = dict(zip(housing_df.SERIALNO, housing_df.SUBSAMPL))
    return person_df.SERIALNO.map(ss_dict)


def make_categorical(x, field, dd):
    '''
    Apply the data dictionary to an integer-coded categorical field,
    resulting in a string-labelled categorical variable. Result is returned
    as a new pandas Series. 

    Args:
        x: person or housing data frame
        field: name of a column in x
        dd: data-dictionary for x as a pandas Data Frame

    Returns:
        Pandas Series (pd.Categorical) with integer-coded levels in x[field]
        translated using values from dd.

    Raises:
        KeyError if field not in dd
    '''
    if field not in set(dd.field):
        raise KeyError('Column name not in data dictionary.')
    dd_field = dd[dd.field==field]
    dd_map = dict(zip(dd_field.level, dd_field.value))
    return pd.Categorical(values=x[field].map(dd_map), 
                        categories=dd_field.value)
