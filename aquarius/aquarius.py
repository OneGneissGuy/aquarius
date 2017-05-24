# -*- coding: utf-8 -*-
"""
Script to read in USGS Aquarius csv data files
Created on Tue May 23 21:15:59 2017

@author: saraceno
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 22:50:56 2017

@author: saraceno
"""
import glob
import os

import pandas as pd

def list_of_files(path, fmatch):
#    path = r'C:\Users\saraceno\Documents\Code\Python\WEBB\SS_PSDS'
#    fmatch = '*$ls.txt'
    files = []
    for name in glob.glob(os.path.join(path, fmatch)):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files

def read_aq_metadata(filename):
    out_dict = dict()
    for line in open(filename, 'r'):
        if line[0] == "#":
            line2 = line[1:].lstrip().rstrip()
            if line2.startswith('Time series identifier:'):
                ts_ID = line2.split(':')[1].lstrip().rstrip()
                site_ID = ts_ID.split('@')[-1].lstrip().rstrip()
                out_dict['time series id'] = ts_ID
                out_dict['site'] = site_ID
            if line2.startswith('Location:'):                
                out_dict['location'] = line2.split(' ')[-1].lstrip().rstrip()
            if line2.startswith('UTC offset:'):
                tz_off = line2.split(' ')[-1]
                if tz_off.startswith('(') and tz_off.endswith(')'):
                    out_dict['UTC offset'] = tz_off[1:-1]
            if line2.startswith('Value units:'):
                    out_dict['units'] = line2.split(':')[1].lstrip().rstrip()
            if line2.startswith('Value parameter:'):
                out_dict['parameter']= line2.split(':')[1].lstrip().rstrip()
            if line2.startswith("CSV"):
                out_dict['header_rows'] = int(line2.split(' ')[-1].lstrip().rstrip()[:-1])
        else:
            break #quit reading the file once we've read the header
    return out_dict


def read_aq(filename, UTC=False):
    """read in a corrected record that has been exported from Aquarius springboard"""
    #filename = r'NO3+NO2,water,insitu_as_N.mg_l.(purged,_ex_situ_SUNA2)@364200119420001.EntireRecord (1).csv'
    #skiprows=15
    #UTC=False    
    meta_data = read_aq_metadata(filename)
    skiprows = meta_data['header_rows']
    if UTC:
        ts_header = 'ISO 8601 UTC'
        ts_col = [0]
    else:
        ts_header = 'Timestamp' + meta_data['UTC offset']# (UTC-08:00)'
        ts_col = [1]
        ts_format = '%Y-%m-%d %H:%M:%S'
    headers = [ts_header, meta_data['parameter'], 'Approval Level', 'Grade', 'Qualifiers']
    df = pd.read_csv(filename, skiprows=skiprows,
                     header=None, index_col=ts_col, delimiter=',', na_values=0)
    df.columns = headers
    if UTC:
        df.index = pd.to_datetime(df.index, infer_datetime_format=True, utc=True)
    else:    
        df.index = pd.to_datetime(df.index, format=ts_format)
        #df.index.tz=timezone('US/Pacific')
    df2 = df[~df.index.duplicated(keep='first')]
    df_out = pd.DataFrame(df2[meta_data['parameter']])
    return df_out