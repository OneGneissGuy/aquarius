# -*- coding: utf-8 -*-
"""
aquarius_example.py
:DESCRIPTION: Example script to read an aquarius csv file into python for 
analysis

:DEPENDENCIES: matplotlib, pandas, aquarius.py

:REQUIRES 
:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.1
"""
import os
from matplotlib import pyplot as plt

from aquarius import list_of_files, read_aq

if __name__ == "__main__":
    #Set the path to the csv data files
    #To start, use the example data files included with the pacakge
    path = os.path.join(os.getcwd(), 'data')
    # identify all of the csv filenames and combine into list 
    # that matches the criteria 
    files = list_of_files(path, '*.csv')

    #read all of the file into a list 
    list_of_dfs = []
    for n, fname in enumerate(files):
        list_of_dfs.append(read_aq(fname))
    #plot the data, one chart per time series
    for df in list_of_dfs:
        plt.figure()
        df.plot()