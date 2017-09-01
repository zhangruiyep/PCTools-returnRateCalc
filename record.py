import datetime

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
			#print delta
			total += r.count*delta
		
		yrr = ((self.cur - self.base)/total)*365
		return yrr

	
	def printHistory(self):
		for r in self.history:
			print( r.count, r.date)
			
	def getFirstTradDate(self):
		d = datetime.date.today()
		for r in self.history:
			if r.date < d:
				d = r.date
		return d
	
	def getTotalDays(self):
		return (self.curDate - self.getFirstTradDate()).days
		
	def isInList(self, acclist):
		for a in acclist:
			if a.name == self.name:
				return true
		return false

def findInList(name, acclist):
	for a in acclist:
		if a.name == name:
			return a
	return ""

