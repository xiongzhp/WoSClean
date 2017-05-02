import csv
import os
import sys
import re
import codecs,cStringIO
reload(sys)  
sys.setdefaultencoding('utf8')

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# filelist=['2007']
filelist=['2007','2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
omitted_num=0
included_num=0
univ_replaced_num=0
univ_annotated_num=0
univ_total_num=0
school_replaced_num=0
school_annotated_num=0
school_total_num=0
# m=0
# n=0
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w))

misspel_univ = dict()
misspel_school = dict()
with open('../university_standardization.txt', 'r') as name_map:
    for line in name_map:
        misspel_univ[line.split('\t')[0]] = line.split('\t')[1].strip()
name_map.close()
with open('../school_standardization.txt', 'r') as name_map:
    for line in name_map:
        misspel_school[line.split('\t')[0]+line.split('\t')[1]] = line.split('\t')[2].strip()
        misspel_school[line.split('\t')[0]+line.split('\t')[2]] = line.split('\t')[2].strip()
        # print line.split('\t')[0]+line.split('\t')[1],misspel_school[line.split('\t')[0]+line.split('\t')[1]]
name_map.close()

for x in filelist:
    fnin = './'+x+'_structurised.csv'
    fnout = './'+x+'_standardized_verbose.csv'
    with open(fnout,'wb') as f1:
        w= csv.writer(f1, dialect='excel') 
        # w = UnicodeWriter(f1,quoting=csv.QUOTE_ALL)
        w.writerow(['wos_id', 'AF', 'univ_original', 'univ_replaced', 'univ_chinese', 'univ', 'minist', 'hospital', 'division', 'acad', 'coll', 'school_original', 'school_replaced', 'school', 'inst', 'dept', 'faculty', 'center', 'lab', 'zipcode', 'city', 'country'])
        # w.writerow('\ufeff')        
        # w.writerow(['wos_id', 'author', 'univ', 'school', 'univ_chinese'])
        with open(fnin, 'r') as f:
            reader = csv.reader(f)
            # reader = UnicodeReader(f)
            next(reader, None)
            for i, line in enumerate(reader):
                univ = ''
                school = ''
                acad = ''
                coll = ''
                inst = ''
                univ_chinese = ''
                univ_original = ''
                univ_replaced = ''
                school_original = ''
                school_replaced = ''
                univ = line[2]
                school = line[8]
                acad = line[6]
                coll = line[7]
                inst = line[9]

                if (univ == '' and acad == ''):
                    univ = inst
                # print univ
                if (univ == '' and acad == '' and inst ==''):
                    univ = coll
                if (school == '' and univ != ''):
                    school = coll
                if (findWholeWord('vocat|broadcast|radio|police|polices').search(univ)):
                    omitted_num += 1
                    continue
                if (univ != ''):
                    univ_original = univ
                    univ = re.sub(r'teacher|teachers', r'normal', univ)
                    univ = re.sub(r'northeastern', r'northeast', univ)
                    univ = re.sub(r'southeastern', r'southeast', univ)
                    univ = re.sub(r'northwestern', r'northwest', univ)
                    univ = re.sub(r'southwestern', r'southwest', univ)
                    univ = re.sub(r'jiaotong', r'jiao tong', univ)
                    univ = re.sub(r'xi an', r'xian', univ)
                    univ = re.sub(r'tsing hua', r'tsinghua', univ)
                    if (univ in misspel_univ.keys()):
                        univ_annotated_num += 1
                        univ_chinese = misspel_univ[univ]
                    if (univ != univ_original):
                        univ_replaced_num += 1
                        univ_replaced = univ

                    if (school != ''):
                        school_original = school
                        school = re.sub(' & ', ' ', school)
                        school = re.sub('s&t', 'sci tech ', school)
                        school = re.sub('biolog', 'bio', school)
                        school = re.sub('biol', 'bio', school)
                        school = re.sub('bio sci', 'bio', school)
                        school = re.sub('biotechnol', 'bio', school)
                        school = re.sub('biotehnol', 'bio', school)
                        school = re.sub('biotech', 'bio', school)
                        school = re.sub('technology', 'tech', school)
                        school = re.sub('technol', 'tech', school)
                        school = re.sub('agriculture', 'agr', school)
                        school = re.sub('agri', 'agr', school)
                        school = re.sub('engineering', 'engn', school)
                        school = re.sub('engineer', 'engn', school)
                        school = re.sub('engn engn', 'engn', school)
                        school = re.sub('environment', 'environ', school)
                        school = re.sub('environm', 'environ', school)
                        school = re.sub('envioronm', 'environ', school)
                        school = re.sub('computat', 'comp', school)
                        school = re.sub('computing', 'comp', school)
                        school = re.sub('computer', 'comp', school)
                        school = re.sub('information', 'informat', school)
                        school = re.sub('mechan ', 'mech ', school)
                        school = re.sub('optelectron', 'opt elect', school)
                        school = re.sub('optoelectron', 'opt elect', school)
                        school = re.sub('optoelect', 'opt elect', school)
                        school = re.sub('optelect', 'opt elect', school)
                        school = re.sub('electron', 'elect', school)
                        school = re.sub('electro', 'elect', school)
                        school = re.sub('electr', 'elect', school)
                        school = re.sub('elecron', 'elect', school)
                        school = re.sub('pharmacyl', 'pharm', school)
                        school = re.sub('pharmacol', 'pharm', school)
                        school = re.sub('pharmaceut', 'pharm', school)
                        school = re.sub('pharmacy', 'pharm', school)
                        school = re.sub('resources', 'resource', school)
                        school = re.sub('sports', 'sport', school)
                        school = re.sub('telecommunicat', 'telecommun', school)
                        school = re.sub('poweer', 'power', school)
                        school = re.sub('sociol', 'social', school)
                        school = re.sub('agron', 'agr', school)
                        for x in ['environ', 'comp', 'informat', 'chem', 'mat', 'life']:
                            school = re.sub(x+' sci engn', x+' sci', school)
                            school = re.sub(x+' sci tech', x+' sci', school)
                            school = re.sub(x+' tech sci', x+' sci', school)
                            school = re.sub(x+' tech engn', x+' sci', school)
                            school = re.sub(x+' engn tech', x+' sci', school)
                            school = re.sub(x+' engn', x+' sci', school)
                            school = re.sub(x+' eng', x+' sci', school)
                            school = re.sub(x+' tech', x+' sci', school)
                        # print univ_chinese+school
                        school_misspel = univ_chinese+school
                        if (school_misspel in misspel_school.keys()):
                            school_annotated_num += 1
                            school = misspel_school[school_misspel]
                            # print school                    
                        if (school_original != school):
                            school_replaced_num += 1
                            school_replaced = school
                        school_total_num += 1
                    univ_total_num += 1
                included_num += 1
                row = [line[0], line[1], univ_original, univ_replaced, univ_chinese, univ] + line[3:8] + [school_original, school_replaced, school] + line[9:]
                # row = [s.encode('utf-8') for s in row]
                # print line[16]
                w.writerow(row)
        f.close()
    f1.close()                      
print('This chunk included %s items, omitted %s items.\r\n\
    Among total %s items with university names,\r\n\
    %s of them have been annotated with Chinese name\r\n and %s of them have been standardized. \r\n\
    Among total %s items with school name, \r\n\
    %s of them have been annotated\r\n and %s of them have been standardized' 
    % (included_num, omitted_num, univ_total_num, univ_annotated_num , univ_replaced_num, school_total_num, school_annotated_num, school_replaced_num))
