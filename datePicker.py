import Tkinter as tk
import tkFileDialog
import tkMessageBox
import os
import ttk
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
