import datetime
import csvop
import record

all = csvop.readFile("data.csv")
for a in all:
	#a.printHistory()
	print a.name, a.getYearRetRate()

csvop.writeFile(all, "result.csv")

