#To-Do:		   Add error-handling
#			   Add a selection to entire tree or only selected directory for scan
#			   Add a filter for file-name, file-size
#              Add an interface to view scanned file list
#-------------------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog
import os
import shutil
import random
from math import trunc
from time import sleep
from tkinter import ttk

frame_list = []
color = ["LIGHTCORAL", "LIGHTSALMON", "FIREBRICK", "PALEVIOLETRED", "TOMATO", "DARKKHAKI", "SLATEBLUE", "PALEGREEN", "FORESTGREEN", "PALETURQUOISE"]

def browse_folder(master):
	folder = filedialog.askdirectory()
	master.dest_label['text'] = ""
	if(folder != ""):
		master.dest_directory = folder
		i = 50
		while(i<len(folder)):
			master.dest_label['text'] += folder[i-50:i]+"\n"
			i += 50
		master.dest_label['text'] += folder[i-50:]
	if( len(master.dest_directory) == 0):
		master.dest_label['text'] = "No Folder Selected"
	
def browse_folders(master):
	master.source_directory = []
	master.source_label['text'] = ""
	while True:
		folder = filedialog.askdirectory()
		if(folder != ""):
			master.source_directory.append(folder)
			i = 50
			while(i<len(folder)):
				master.source_label['text'] += folder[i-50:i]+"\n"
				i += 50
			master.source_label['text'] += folder[i-50:]
		else:
			return
	if( len(master.source_directory) == 0):
		master.source_label['text'] = "No Folder Selected"
	
def delete_frame(_frame):
	frame_list.remove(_frame)
	_frame.destroy()

class Input_Row(Frame):
	source_directory = []
	dest_directory = ""
	
	def createWidgets(self):
		self.delete_frame=Button(self,text="X",bg="red",width=2,command=lambda m=self:delete_frame(m))
		self.get_entry=Entry(self)
		self.source_label = Label(self,text="No Folder Selected",width=45,fg="orange")
		self.dest_label = Label(self,text="No Folder Selected",width=45,fg="blue")
		self.add_source = Button(self,text="Browse",bg="orange",command=lambda m=self:browse_folders(self))
		self.add_dest = Button(self,text="Browse",bg="blue",command=lambda m=self:browse_folder(self))
		
		self.delete_frame.grid(row=0,column=0,sticky=W)
		self.get_entry.grid(row=0,column=1)
		self.source_label.grid(row=0,column=3)
		self.dest_label.grid(row=0,column=6)
		self.add_source.grid(row=0,column=5)
		self.add_dest.grid(row=0,column=7)
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self['bg']='silver'
		self['bd']=2
		self['bg']=random.choice(color)
		self.pack()
		self.createWidgets()
		frame_list.append(self)
		
def get_extension(filename):
	temp = filename.split('.')
	return "."+temp[-1]
		
#Since disk i/o is costly, disk is scanned only once and file is matched
def process_files(file_type, dest, folder,step,progress,progress_tk):
	for _folder in folder:
		_dir = os.listdir(_folder)
		_step = (step/(len(_dir)+1))
		print(_step,len(_dir))
		for _file in _dir:
			extension = get_extension(_file)
			if(extension in file_type[_folder]):
				#print('copying from {} to {}'.format(os.path.join(_folder,_file),dest[(_folder,extension)]))
				shutil.move(os.path.join(_folder,_file),dest[(_folder,extension)])
			progress.step(_step)
			progress.update()
		progress.step(_step)
		progress.update()
	progress_tk.destroy()
		
def start_process():
	file_type = {}
	dest = {}
	folder = set()
	SIZE = 0
	for _frame in frame_list:
		if(_frame.get_entry.get()!="" and _frame.dest_directory != "" and len(_frame.source_directory)!=0):
			for src_folder in _frame.source_directory:
				file_type[src_folder]=[]
				folder.add(src_folder)
				SIZE +=1
	for _frame in frame_list:
		if(_frame.get_entry.get()!="" and _frame.dest_directory != "" and len(_frame.source_directory)!=0):
			for src_folder in _frame.source_directory:
				file_type[src_folder].append(_frame.get_entry.get()) 
				dest[(src_folder,_frame.get_entry.get())]=_frame.dest_directory
	
	if(SIZE == 0):
		SIZE = 1
	step = (100/SIZE)
	print(step)	
	
	progress_tk = Tk()
	progress_tk.title('Progress')
	#progress_tk.geometry("50x550"+"400"+"300")
	progress = ttk.Progressbar(progress_tk, length=500)
	progress.pack()
	progress.after(1,process_files(file_type, dest, folder,step,progress,progress_tk))
	progress_tk.mainloop()	
	
def progress_bar():
	pass
			 
def app():
	###### Main Window ######
	root = Tk()
	root.title('{}'.format("File Organizer"))
	root.geometry('{}x{}+{}+{}'.format(900,400,200,200))
	root.resizable(width=FALSE, height=FALSE)

	#### Frames ####
	frame = Frame(root, relief=RAISED, borderwidth=4)


	#### Labels ####
	ext_label = Label(frame,text="File Type")
	src_folders = Label(frame,text="Source folders")
	dest_folder = Label(frame,text="Destination folder")


	#### Buttons ####
	add_ext_btn = Button(frame, text="Add More File Type", fg="white", bg="green", padx=25, pady=2, command=lambda m=root:Input_Row(m))
	add_ext_btn['width']=34

	start_btn = Button(frame, text="Start", fg="white", bg="green", padx=25, pady=2, command=start_process)
	start_btn['width']=34

	quit_btn = Button(frame, text="Quit", fg="white", bg="red", padx=25, pady=2, command=root.destroy)
	quit_btn['width']=34


	##### Layout ####
	add_ext_btn.grid(row=0,column=0)
	start_btn.grid(row=0,column=1)
	quit_btn.grid(row=0,column=2)

	ext_label.grid(row=1,column=0,padx=5,pady=2,sticky=N+W)
	src_folders.grid(row=1,column=1,columnspan=1,padx=5,pady=2,sticky=N+W)
	dest_folder.grid(row=1,column=2,columnspan=1,padx=5,pady=2,sticky=N+W)


	frame.pack()


	root.mainloop()
	
		
app()
