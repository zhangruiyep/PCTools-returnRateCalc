import csv
import record
import datetime

def str2date(str):
	d = str.split("-")
	date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
	return date

def readDataFile(filename):
	accAll = []
	f = open(filename, "r")
	rdr = csv.reader(f)
	for row in rdr:
		#print row
		name = row[0]
		tradCount = row[1]
		tradDate = row[2]
		curCount = row[3]
		curDate = row[4]
		#print name, tradCount, tradDate, curCount, curDate
		a = record.findInList(name, accAll)
		if a == "":
			a = record.acc(name)
			accAll.append(a)

		if tradCount != "":
			#it is a trad record
			date = str2date(tradDate)
			r = record.tradRecord(float(tradCount), date)
			a.trad(r)
		if curCount != "":
			#set cur
			date = str2date(curDate)
			a.setCur(float(curCount), date)
	
	f.close()
	return accAll

def writeResultFile(acclist, filename):
	row = []
	f = open(filename, "w")
	wtr = csv.writer(f)
	for a in acclist:
		row.append(a.name)
		row.append(a.getYearRetRate())
		wtr.writerow(row)
		row = []
	
	f.close()
	
def writeDataFile(acclist, filename):
	row = []
	f = open(filename, "w")
	print( "saving %s" % filename)
	wtr = csv.writer(f)
	for a in acclist:
		for r in a.history:
			row.append(a.name)
			row.append(r.count)
			row.append(r.date)
			row.append("")
			row.append("")
			wtr.writerow(row)
			row = []
		
		row.append(a.name)
		row.append("")
		row.append("")
		row.append(a.cur)
		row.append(a.curDate)
		wtr.writerow(row)
		row = []
	
	f.close()
	
