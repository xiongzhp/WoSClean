import csv
import os
import sys
import re
import pickle
import itertools

filelist=['2007','2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
# filelist=['2007']
j=0
k=0
for x in filelist:
    fnin = './'+x+'_author.csv'
    fnout = './'+x+'_mapped.csv'
    with open(fnout,'wb') as f1:
        w= csv.writer(f1, dialect='excel') 
        with open(fnin, 'r') as f:
            reader = csv.reader(f)
            for line1,line2 in itertools.izip_longest(*[reader]*2):
                # print(line1,line2)
                try:
                    for i, x in enumerate(line1[2:]):
                        x = re.sub(' +',' ', x.strip())
                        y = re.sub(' +',' ', line2[i+2].strip())
                        w.writerow([line1[0], x, y])
                except:
                    pass
        f.close()
    f1.close()

