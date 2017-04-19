"""
Simple script to convert HDF files to text output

Authors
-------
Bryan Webber, Nick Curtis

2017
"""

# coding: utf-8
from netCDF4 import Dataset
import os
import numpy as np

delt = 0.17
t0 = 2.4*60

# find directories to check starting from cwd
dirs = next(os.walk('.'))[1]
for d in dirs:
    files = os.listdir(d)
    for file in files:
        # find all CDF files in dir
        if file.endswith('.CDF'):
            # open datasets and find total intensity
            rootgrp = Dataset(file, 'r')
            print(os.path.join(d, file))
            total_intensity = rootgrp.variables['total_intensity']
            num_points = len(total_intensity)
            # load time for intensity values
            time = np.zeros(num_points)
            for j in range(num_points):
                time[j] = t0 + delt*j
            time = time/60  # Convert to minutes
            output = np.transpose(np.vstack((time, total_intensity)))
            # save to csv
            outfile = file.rstrip('.CDF') + '.csv'
            outloc = os.path.join(d, outfile)
            np.savetxt(fname=outloc, X=output, delimiter=',')
            rootgrp.close()
