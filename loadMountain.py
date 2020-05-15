import codecs
import numpy as np

"""
Convert asc file to a csv file
"""
def convert_tif_csv(filename):
    with codecs.open(filename, encoding='utf-8-sig') as f:
        for i in range(6):
            print(f.readline(), end='')
        X = [[float(x) for x in line.split()] for line in f]

        np.savetxt('Roger_Data', X, delimiter=',')

convert_tif_csv('Rogers_Data.asc')