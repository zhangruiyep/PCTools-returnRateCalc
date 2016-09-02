import Tkinter as tk
import tkFileDialog
import tkMessageBox
import os
import csvop
import ttk

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master) 
		self.grid() 
		self.createWidgets()
		self.accs = []

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
		
		self.mb = tk.Menubutton(menu_frame, text="Data")
		self.mb.grid(row=0, column=1)

		self.mb.menu = tk.Menu(self.mb, tearoff=0)
		self.mb["menu"] = self.mb.menu
		
		self.mb.menu.add_command(label="Total", command=self.calc_total)
		self.mb.menu.add_command(label="Average", command=self.calc_avr)
		
		self.tv = ttk.Treeview(self, columns=("name", "count", "date", "cur", "cur_date", "yrr"))
		self.tv.grid(row = 1)

		self.tv.column("#0", width=20)
		self.tv.column("name", width=100)
		self.tv.column("count", width=100)
		self.tv.column("date", width=100)
		self.tv.column("cur", width=100)
		self.tv.column("cur_date", width=100)
		self.tv.column("yrr", width=100)

		self.tv.heading('name', text='Name')
		self.tv.heading('count', text='Trad Count')
		self.tv.heading('date', text='Trad Date')
		self.tv.heading('cur', text='Cur Count')
		self.tv.heading('cur_date', text='Cur Date')
		self.tv.heading('yrr', text='Year Return Rate')
		
		self.sb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tv.yview)
		self.sb.grid(row = 1, column=1, sticky=tk.NS)
		
		self.tv.configure(yscrollcommand=self.sb.set)

		self.context_menu = tk.Menu(self.tv, tearoff=0)
		self.context_menu.add_command(label="Edit", command=self.edit_handler)
		self.tv.bind('<3>', self.show_context_menu)
		self.entryPopup = ""
 
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

		# place Entry popup properly         
		self.entryPopup = tk.Entry(self.tv)
		self.entryPopup.place( x=x, y=y, anchor=tk.NW, width=width)
		
		self.entryPopup.bind('<Return>', self.entryEnter)
		self.entryPopup.focus_force()

	def entryEnter(self, event):
		entry_text = self.entryPopup.get()
		#print entry_text
		self.tv.set(self.edit_row, column=self.edit_column, value=entry_text)
		self.entryPopup.destroy()
			
	def open_file(self):
		filename = os.path.realpath(tkFileDialog.askopenfilename())
		if os.path.isfile(filename):
			self.accs = csvop.readDataFile(filename)
			self.fill_treeview(self.tv, self.accs)
		
	def save_result(self):
		filename = os.path.realpath(tkFileDialog.asksaveasfilename())
		csvop.writeResultFile(self.accs, filename)

	def save_file(self):
		if self.accs == []:
			tkMessageBox.showwarning("Warning", "No Data to save!")
			return
			
		filename = os.path.realpath(tkFileDialog.asksaveasfilename())
		#print "get %s" % filename
		csvop.writeDataFile(self.accs, filename)

			
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
		
			
	
	def fill_treeview(self, tv, accs):
		for item in tv.get_children():
			tv.delete(item)
			
		for acc in accs:
			iid = tv.insert('',"end",values=(acc.name, "", "", acc.cur, acc.curDate, acc.getYearRetRate()))
			for r in acc.history:
				tv.insert(iid, "end", values=("", r.count, r.date, "", "", ""))
			

app = Application() 
app.master.title('Calc Real Return') 
app.mainloop() 