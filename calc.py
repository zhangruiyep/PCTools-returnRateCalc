import datetime
import csvop
import record

all = csvop.readDataFile("data.csv")
for a in all:
	#a.printHistory()
	print a.name, a.getYearRetRate()

csvop.writeResultFile(all, "result.csv")

