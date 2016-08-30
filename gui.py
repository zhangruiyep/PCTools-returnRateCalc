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

	def createWidgets(self):
		#pass
		self.mb = tk.Menubutton(self, text="File")
		self.mb.grid()
		
		self.mb.menu = tk.Menu(self.mb, tearoff=0)
		self.mb["menu"] = self.mb.menu
		
		self.mb.menu.add_command(label="Open file...", command=self.open_file)
		self.mb.menu.add_command(label="Save result...", command=self.save_result)
		
		self.tv = ttk.Treeview(self, columns=("name", "count", "date", "cur", "cur_date"))
		self.tv.grid(row = 1)

		self.tv.column("name", width=100)
		self.tv.column("count", width=100)
		self.tv.column("date", width=100)
		self.tv.column("cur", width=100)
		self.tv.column("cur_date", width=100)

		self.tv.heading('name', text='Name')
		self.tv.heading('count', text='Trad Count')
		self.tv.heading('date', text='Trad Date')
		self.tv.heading('cur', text='Cur Count')
		self.tv.heading('cur_date', text='Cur Date')
		
	def open_file(self):
		filename = os.path.realpath(tkFileDialog.askopenfilename())
		#print filename
		self.accs = csvop.readFile(filename)
		self.fill_treeview(self.tv, self.accs)
		
	def save_result(self):
		filename = os.path.realpath(tkFileDialog.asksaveasfilename())
		csvop.writeFile(self.accs, filename)
	
	def fill_treeview(self, tv, accs):
		for acc in accs:
			iid = tv.insert('',"end",values=(acc.name, "", "", acc.cur, acc.curDate))
			for r in acc.history:
				tv.insert(iid, "end", values=("", r.count, r.date, "", ""))
		

app = Application() 
app.master.title('Calc Real Return') 
app.mainloop() 