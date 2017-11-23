import sys
import xlrd
import csv
filePath = sys.argv[1] # user input file
csvPath = sys.argv[2]
workBook = xlrd.open_workbook(filePath)
nama_sheet = workBook.sheet_names()
list_sheet = []
length = len(nama_sheet)
for i in range(0,length):
	sheet =  workBook.sheet_by_name(nama_sheet[i])
	list_sheet.append(sheet)
outcsvFile = open(csvPath, 'wb')
wr = csv.writer(outcsvFile, quoting=csv.QUOTE_ALL)
total_row = list_sheet[0].ncols
for k in xrange(0,len(list_sheet)):
	for rownum in xrange(list_sheet[k].nrows):
		wr.writerow(list_sheet[k].row_values(rownum))
# if len(nama_sheet) > 1:
# 	for k in xrange(1,len(list_sheet)):
# 	  	if list_sheet[k].ncols != total_row:
# 			continue
# 	for rownum in xrange(1,list_sheet[k].nrows):
# 		wr.writerow(list_sheet[k].row_values(rownum))

outcsvFile.close()