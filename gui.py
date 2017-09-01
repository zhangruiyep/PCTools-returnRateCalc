import Tkinter as tk
import tkFileDialog
import tkMessageBox
import os
import csvop
import ttk
import record
import datetime

class datePicker(tk.Frame):
	def __init__(self, master=None, parentIdx="", date=""):
		tk.Frame.__init__(self, master)
		self.grid()
		if date != "":
		    splitDate = date.split("-")
		    self.y = splitDate[0]
		    self.m = splitDate[1]
		    self.d = splitDate[2]
		else:
		    self.y = 2017
		    self.m = 6
		    self.d = 1

		self.createWidgets()

	def createWidgets(self):
		yearOptionList = range(2000, 2030)
		self.yearVar = tk.StringVar()
		self.yearVar.set(self.y)
		self.yearOpt = tk.OptionMenu(self, self.yearVar, *yearOptionList)
		self.yearOpt.grid(row=0, column=0, sticky=tk.W)
		
		monthOptionList = range(1, 13)
		self.monthVar = tk.StringVar()
		self.monthVar.set(self.m)
		self.monthOpt = tk.OptionMenu(self, self.monthVar, *monthOptionList)
		self.monthOpt.grid(row=0, column=1, sticky=tk.W)

		dayOptionList = range(1, 32)
		self.dayVar = tk.StringVar()
		self.dayVar.set(self.d)
		self.dayOpt = tk.OptionMenu(self, self.dayVar, *dayOptionList)
		self.dayOpt.grid(row=0, column=2, sticky=tk.W)
		
		self.todayBtn = ttk.Button(self, text="Today", command=self.getToday)
		self.todayBtn.grid(row=0, column=3)
		
		
	def get(self):
		date = "{0}-{1}-{2}".format(self.yearVar.get(), self.monthVar.get(), self.dayVar.get())
		return date
		
	def getToday(self):
		today = datetime.date.today()
		self.yearVar.set(today.year)
		self.monthVar.set(today.month)
		self.dayVar.set(today.day)
		self.focus_force()
	
	
class AddFrame(tk.Frame):
	def __init__(self, master=None, parentIdx="", date=""):
		tk.Frame.__init__(self, master)
		self.grid()
		if parentIdx != "":
			self.accName = (master.item(parentIdx))['values'][0]
			self.mode = "record"
		else:
			self.accName = ""
			self.mode = "account"
		self.tradCount = ""
		self.tradDate = date
		self.tv = master
		self.parentIdx = parentIdx
		self.createWidgets()
		
	def createWidgets(self):
		curRow = 0
		label = ttk.Label(self, text="Account:", justify=tk.LEFT)
		label.grid(row = curRow)

		self.accEntry = ttk.Entry(self)
		self.accEntry.delete(0, tk.END)
		if self.mode == "record":
			self.accEntry.insert(0, self.accName)
			self.accEntry['state']=tk.DISABLED
		self.accEntry.grid(row=curRow, column=1)		

		curRow += 1
		label = ttk.Label(self, text="Count:", justify=tk.LEFT)
		label.grid(row=curRow)

		self.cntEntry = ttk.Entry(self)
		self.cntEntry.delete(0, tk.END)
		self.cntEntry.grid(row=curRow, column=1)		

		curRow += 1
		label = ttk.Label(self, text="Date:", justify=tk.LEFT)
		label.grid(row=curRow)
		'''
		self.dateEntry = ttk.Entry(self)
		self.dateEntry.delete(0, tk.END)
		'''

		#print self.tradDate
		self.dateEntry = datePicker(self, date=self.tradDate)
		self.dateEntry.grid(row=curRow, column=1)		
		
		if self.mode == "account":
			curRow += 1
			label = ttk.Label(self, text="Current Count:", justify=tk.LEFT)
			label.grid(row=curRow)

			self.curEntry = ttk.Entry(self)
			self.curEntry.delete(0, tk.END)
			self.curEntry.grid(row=curRow, column=1)		

			curRow += 1
			label = ttk.Label(self, text="Current Date:", justify=tk.LEFT)
			label.grid(row=curRow)
			'''
			self.curdateEntry = ttk.Entry(self)
			self.curdateEntry.delete(0, tk.END)
			'''
			self.curdateEntry = datePicker(self)
			self.curdateEntry.grid(row=curRow, column=1)		
		
		curRow += 1
		OKBtn = ttk.Button(self, text="OK", command=self.addTradRecord)
		OKBtn.grid(row=curRow)
		CancelBtn = ttk.Button(self, text="Cancel", command=self.cancelAdd)
		CancelBtn.grid(row=curRow, column=1)

	def addTradRecord(self):
		cnt = self.cntEntry.get()
		date = self.dateEntry.get()
		if self.mode == "record":
		#print cnt, date
			self.tv.insert(self.parentIdx, "end", values=("", cnt, date, "", "", ""))

		if self.mode == "account":
			self.accName = self.accEntry.get()
			curCnt = self.curEntry.get()
			curDate = self.curdateEntry.get()
			iid = self.tv.insert(self.parentIdx, "end", values=(self.accName, "", "", curCnt, curDate, ""))
			self.tv.insert(iid, "end", values=("", cnt, date, "", "", ""))
		
		self.tv.update_accs()
		self.tv.update_yrr()
		self.destroy()

	def cancelAdd(self):
		self.destroy()
		
class calcTreeview(ttk.Treeview):
	def __init__(self, master=None):
		ttk.Treeview.__init__(self, master)
		self['columns']=("name", "count", "date", "cur", "cur_date", "yrr")
		self.accs = []
		self.grid(sticky=tk.NSEW)
		self.createWidgets()
	
	def createWidgets(self):
		self.column("#0", width=20, stretch=0)
		self.column("name", width=100)
		self.column("count", width=100)
		self.column("date", width=100)
		self.column("cur", width=100)
		self.column("cur_date", width=100)
		self.column("yrr", width=100)

		self.heading('name', text='Name')
		self.heading('count', text='Trad Count')
		self.heading('date', text='Trad Date')
		self.heading('cur', text='Cur Count')
		self.heading('cur_date', text='Cur Date')
		self.heading('yrr', text='Year Return Rate')
		
	def fill_treeview(self, accs):
		self.accs = accs
		for item in self.get_children():
			self.delete(item)
			
		for acc in self.accs:
			iid = self.insert('',"end",values=(acc.name, "", "", acc.cur, acc.curDate, acc.getYearRetRate()))
			for r in acc.history:
				self.insert(iid, "end", values=("", r.count, r.date, "", "", ""))
				
	def update_accs(self):
		self.accs = []
		
		for i in self.get_children():
			item = self.item(i)
			name = item['values'][0]
			tradCount = item['values'][1]
			tradDate = item['values'][2]
			curCount = item['values'][3]
			curDate = item['values'][4]
			a = record.findInList(name, self.accs)
			if a == "":
				a = record.acc(name)
				self.accs.append(a)
			# Add history
			for trdIdx in self.get_children(i):
				trdItem = self.item(trdIdx)
				tradCount = trdItem['values'][1]
				tradDate = trdItem['values'][2]

				if tradCount != "":
					#it is a trad record
					date = csvop.str2date(tradDate)
					r = record.tradRecord(float(tradCount), date)
					a.trad(r)
			# Add Cur
			if curCount != "":
				#set cur
				date = csvop.str2date(curDate)
				a.setCur(float(curCount), date)

	def update_yrr(self):
		yrrcolumn = "yrr"
		for acc in self.accs:
			for accrow in self.get_children():
				if self.item(accrow)['values'][0] == acc.name:
					self.set(accrow, yrrcolumn, value=acc.getYearRetRate())

	def calc_total(self):
		total = 0.0
		for acc in self.accs:
			total += acc.cur
		tkMessageBox.showinfo("Total", "Your total count is %f" % total)
	
	def calc_avr(self):
		t = 0.0
		base = 0.0
		cur = 0.0
		
		for acc in self.accs:
			for r in acc.history:
				delta = (acc.curDate - r.date).days
				#print delta
				t += r.count*delta
			base += acc.base
			cur += acc.cur
			
		yrr = ((cur - base)/t)*365
		
		tkMessageBox.showinfo("Average YRR", "Your Average YRR is %f" % yrr)
	
	def history_merge(self):
		for acc in self.accs:
			for cur in acc.history:
				for comp in acc.history:
					if (comp != cur) and (comp.date == cur.date):
						#print acc.name, comp.count, cur.count, cur.date
						cur.count += comp.count
						acc.history.remove(comp)
						
		self.fill_treeview(self.accs)
						

					
class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master) 
		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.grid(sticky=tk.NSEW) 
		self.createWidgets()
		
	def createWidgets(self):

		#pass
		menu_frame = ttk.Frame(self)
		menu_frame.grid(sticky=tk.W)
		
		self.mb = tk.Menubutton(menu_frame, text="File")
		self.mb.grid()
		
		self.mb.menu = tk.Menu(self.mb, tearoff=0)
		self.mb["menu"] = self.mb.menu
		
		self.mb.menu.add_command(label="Open file...", command=self.open_file)
		self.mb.menu.add_command(label="Save file...", command=self.save_file)
		self.mb.menu.add_command(label="Save result...", command=self.save_result)
		

		self.tv = calcTreeview(self)
		self.tv.grid(row = 1, sticky=tk.NSEW)
				
		self.sb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tv.yview)
		self.sb.grid(row = 1, column=1, sticky=tk.NS)
		
		self.tv.configure(yscrollcommand=self.sb.set)

		self.context_menu = tk.Menu(self.tv, tearoff=0)
		self.context_menu.add_command(label="Edit", command=self.edit_handler)
		self.context_menu.add_command(label="Add", command=self.add_handler)
		self.tv.bind('<3>', self.show_context_menu)
		self.entryPopup = ""
		self.record_frame = ""

		self.mb = tk.Menubutton(menu_frame, text="Data")
		self.mb.grid(row=0, column=1)

		self.mb.menu = tk.Menu(self.mb, tearoff=0)
		self.mb["menu"] = self.mb.menu
		
		self.mb.menu.add_command(label="Total", command=self.tv.calc_total)
		self.mb.menu.add_command(label="Average", command=self.tv.calc_avr)
		self.mb.menu.add_command(label="History merge", command=self.tv.history_merge)

		
	def show_context_menu(self, event):
		self.context_menu.post(event.x_root,event.y_root)
		self.event = event		
 
	def edit_handler(self):
		#print "in copy_handler"
		#print self.event.x, self.event.y
		# close previous popups
		if self.entryPopup:
			self.entryPopup.destroy()

		self.edit_row = self.tv.identify_row(self.event.y)
		self.edit_column = self.tv.identify_column(self.event.x)
		#print self.tv.identify_element(self.event.x, self.event.y)
		x,y,width,height = self.tv.bbox(self.edit_row, self.edit_column)

		if self.edit_column == "#3" or self.edit_column == "#5":
			self.entryPopup = datePicker(self.tv)
			self.entryPopup.place( x=x, y=y, anchor=tk.NW)
		else:
			# place Entry popup properly         
			self.entryPopup = tk.Entry(self.tv)
			self.entryPopup.place( x=x, y=y, anchor=tk.NW, width=width)
			
		self.entryPopup.bind('<Return>', self.entryEnter)
		self.entryPopup.bind('<Escape>', self.entryEntryDestroy)
		self.entryPopup.focus_force()
		
	def add_handler(self):
		if self.entryPopup:
			self.entryPopup.destroy()

		self.edit_row = self.tv.identify_row(self.event.y)
		self.edit_column = self.tv.identify_column(self.event.x)
		#print self.tv.identify_region(self.event.x, self.event.y)
		#print self.edit_row
		#x,y,width,height = self.tv.bbox(self.edit_row)
		
		parent = self.tv.parent(self.edit_row)
		#print parent
		self.addDataFrame(parent)
			
			
	def addDataFrame(self, parentItem):
		#x,y,width,height = self.tv.bbox(parentItem)
		
		if self.record_frame:
			self.record_frame.destroy()

		#print self.tv.item(self.edit_row)['values']
		if (self.edit_row != "") and (self.edit_row != None):
		    date = self.tv.item(self.edit_row)['values'][2]
		else:
		    date = ""
		self.record_frame = AddFrame(self.tv, parentItem, date)
		self.record_frame.place(x=0, y=20, anchor=tk.NW)			
		

	def entryEnter(self, event):
		entry_text = self.entryPopup.get()
		#print entry_text
		self.tv.set(self.edit_row, column=self.edit_column, value=entry_text)
		self.tv.update_accs()
		self.tv.update_yrr()
		self.entryPopup.destroy()
	
	def entryEntryDestroy(self, event):
		self.entryPopup.destroy()
			
	def open_file(self):
		filename = os.path.realpath(tkFileDialog.askopenfilename())
		if os.path.isfile(filename):
			accs = csvop.readDataFile(filename)
			self.tv.fill_treeview(accs)
		
	def save_result(self):
		filename = os.path.realpath(tkFileDialog.asksaveasfilename())
		csvop.writeResultFile(self.tv.accs, filename)

	def save_file(self):
		
		if self.tv.accs == []:
			tkMessageBox.showwarning("Warning", "No Data to save!")
			return

		filename = tkFileDialog.asksaveasfilename()
		if (filename != None) and (filename != ""):
		    filename = os.path.realpath(filename)
		    #print "get %s" % filename
		    csvop.writeDataFile(self.tv.accs, filename)

			
		
			
	

app = Application() 
app.master.title('Calc Real Return') 
app.master.rowconfigure(0, weight=1)
app.master.columnconfigure(0, weight=1)
app.mainloop() 