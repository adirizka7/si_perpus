import sys
import xlrd
import csv
filePath = sys.argv[1] # user input file
csvPath = sys.argv[2]
workBook = xlrd.open_workbook(filePath)
sheet_names = workBook.sheet_names()
list_sheet = []
lenth = len(sheet_names)
for i in range(0,lenth):
   sheet =  workBook.sheet_by_name(sheet_names[i])
   list_sheet.append(sheet)
yourcsvFile = open(csvPath, 'wb')
wr = csv.writer(yourcsvFile, quoting=csv.QUOTE_ALL)
total_row = list_sheet[0].ncols
for k in xrange(0,1):
    for rownum in xrange(list_sheet[k].nrows):
      wr.writerow(list_sheet[k].row_values(rownum))
if len(sheet_names) > 1:
   for k in xrange(1,len(list_sheet)):
      if list_sheet[k].ncols != total_row:
         continue
   for rownum in xrange(1,list_sheet[k].nrows):
       
      wr.writerow(list_sheet[k].row_values(rownum))

yourcsvFile.close()
