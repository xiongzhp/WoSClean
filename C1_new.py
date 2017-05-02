__author__ = 'HENG GENG'
from bs4 import BeautifulSoup
import csv
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#filelist=["1956-1995", "1996-1999", "2000-2001", "2002-2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]
filelist=["2012", "2013", "2014", "2015"]
for name in filelist:
  RawPath=r'C:\Users\HENG GENG\WORK\InnovationGoogle\Python data\WOS_Data_20150810_Checked\\'+ name
  print(RawPath)
  SavePath=r'C:\Users\HENG GENG\WORK\InnovationGoogle\wosdata\C1_wos\\'+name+'_C1.csv'

  with open(SavePath,'wb') as f1:
     w= csv.writer(f1,dialect='excel')
     for root, dirs, filenames in os.walk(RawPath):
         for f in filenames:
             fullpath = os.path.join(root, f)
             page=open(fullpath)
             soup = BeautifulSoup(page, 'html.parser')
             allpapers=soup.find("table")
             for paper in allpapers.findAll("table",{'class': None}):
                 for item in paper.findAll("tr"):
                     lists=item.findAll("td")
                     if lists[0].get_text(strip=True)=='UT':
                         WS=lists[1].get_text(strip=True)
                 for row in paper.findAll("tr"):
                     cells = row.findAll("td")
                     if cells[0].get_text(strip=True)=='C1':
                         Au_add=cells[1].findAll(text=True)
                         Au_add=[each.replace('\n','') for each in Au_add]
                         Au_add=[each.encode('utf8') for each in Au_add]
                         Au_add=[WS]+Au_add
                         w.writerow(Au_add)
  f1.close()

