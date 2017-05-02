import csv
import os
import sys
import re

# filelist=['2007']
filelist=['2007','2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
j=0
k=0
# l=0
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w))

for x in filelist:
    fnin = './'+x+'_C1.csv'
    fnout = './'+x+'_structurised.csv'
    with open(fnout,'wb') as f1:
        w= csv.writer(f1, dialect='excel') 
        w.writerow(['wos_id', 'author', 'univ', 'minist', 'hospital', 'division', 'acad', 'coll', 'school', 'inst', 'dept', 'faculty', 'center', 'lab', 'zipcode', 'city', 'country'])
        with open(fnin, 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                for x in line[1:]:
                    try:
                        univ = ''
                        minist = ''
                        hospital = ''
                        division = ''
                        acad = ''                       
                        coll = ''
                        school = ''
                        inst = ''                       
                        dept = ''
                        faculty = ''
                        center = ''
                        lab = ''
                        country = ''
                        city = ''
                        x = re.sub(' +',' ',x)
                        sx = x.split(']')
                        fa = sx[1].split(',')
                        for fa_info in fa:       
                            if (findWholeWord('Univ|univ').search(fa_info)):
                                if (univ == ''):
                                    univ = fa_info.strip().lower()
                                    # print univ
                            if ('Minist' in fa_info):
                                minist = fa_info.strip().lower()
                            if (findWholeWord('Hosp|hosp').search(fa_info)):
                                hospital = fa_info.strip().lower()
                            if (findWholeWord('Div').search(fa_info)):
                                division = fa_info.strip().lower()
                            if ('Acad' in fa_info):
                                acad = fa_info.strip().lower()
                            if ('Sch' in fa_info):
                                school = fa_info.strip().lower()
                            if ('Coll' in fa_info):
                                coll = fa_info.strip().lower()
                            if (findWholeWord('Inst|inst').search(fa_info)):
                                inst = fa_info.strip().lower()
                            if ('Dept' in fa_info):
                                dept = fa_info.strip().lower()
                            if ('Fac' in fa_info):
                                faculty = fa_info.strip().lower()
                            if ('Center'in fa_info or 'Ctr' in fa_info):
                                center = fa_info.strip().lower()
                            if ('Lab' in fa_info):
                                lab = fa_info.strip().lower()
                        country = fa[-1].strip()
                        # city = fa[-2].strip().lower()
                        city = ''.join([i for i in fa[-2] if not i.isdigit()]).strip().lower()
                        zipcode = ''.join([i for i in fa[-2] if not i.isalpha()]).strip().lower()
                        au = sx[0].replace('[', '')
                        au = au.split(';')
                        j+= 1
                        for author in au:
                            # print(line[0]+'\t'+author+'\t'+univ)
                            w.writerow([line[0], author.strip(), univ, minist, hospital, division, acad, coll, school, inst, dept, faculty, center, lab, zipcode, city, country])
                    except:
                        # print 'this line has no author name!'
                        pass
                        k+= 1
                        # print au
        f.close()
    f1.close()                      
print('%s items have been included, %s items have been omitted' % (j, k))
