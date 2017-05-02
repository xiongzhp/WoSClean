from bs4 import BeautifulSoup
import csv
import os


path=r'C:\Users\HENG GENG\WORK\InnovationGoogle\Python data\WOS_Data_20150810_Checked\2014'
with open(r'C:\Users\HENG GENG\WORK\InnovationGoogle\wosdata\2014_author.csv','wb') as f1:
   w= csv.writer(f1,dialect='excel')
   for root, dirs, filenames in os.walk(path):
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
                   if cells[0].get_text(strip=True)=='AU':
                       ABname=cells[1].findAll(text=True)
                       ABname=[each.replace('\n','') for each in ABname]
                       ABname=[WS,'AU']+ABname
                       w.writerow(ABname)
                   if cells[0].get_text(strip=True)=='AF':
                       AFname=cells[1].findAll(text=True)
                       AFname=[each.replace('\n','') for each in AFname]
                       AFname=[WS,'AF']+AFname
                       w.writerow(AFname)
f1.close()

