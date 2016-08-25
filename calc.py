import datetime

'''
d = datetime.date(2016, 8, 25)
print d

d2 = datetime.date(2016, 8, 30)
print (d2-d).days
'''
class tradRecord:
	def __init__(self, count, date=datetime.date.today()):
		self.count = count
		self.date = date


class acc:
	def __init__(self, name):
		self.name = name
		self.history = []
		self.base = 0
		self.cur = 0
		self.curDate = datetime.date.today()
	
	def trad(self, record):
		self.history.append(record)
		self.base += record.count
		
	def setCur(self, cur, date):
		self.cur = cur
		self.curDate = date
	
	def getRetRate(self):
		return (self.cur / self.base) - 1
		
	def getYearRetRate(self):
		total = 0.0
		for r in self.history:
			delta = (self.curDate - r.date).days
			print delta
			total += r.count*delta
		
		yrr = ((self.cur - self.base)/total)*365
		return yrr

	
	def printHistory(self):
		for r in self.history:
			print r.count, r.date
			
	def getFirstTradDate(self):
		d = datetime.date.today()
		for r in self.history:
			if r.date < d:
				d = r.date
		return d
	
	def getTotalDays(self):
		return (self.curDate - self.getFirstTradDate()).days
	
acc1 = acc("yuekaixin1")
t = tradRecord(1000.0, datetime.date(2016, 3, 15))
acc1.trad(t)
t2 = tradRecord(3000.0, datetime.date(2016, 8, 20))
acc1.trad(t2)
acc1.printHistory()
acc1.setCur(5000.0, datetime.date.today())
print acc1.getRetRate()
print acc1.getFirstTradDate()
print acc1.getYearRetRate()