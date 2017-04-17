# encoding:utf-8
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import time
import datetime
import requests
from datetime import date
from openpyxl import Workbook, load_workbook
from shutil import copyfile
from openpyxl import Workbook
from dateutil.relativedelta import relativedelta
import tweepy
import csv
import re

list_Entry = []
list_csv_key = []
reader = None
csvfile = None

def Main():
    root = tk.Tk()
    root.geometry('600x800')
    root.title("DBMS")

    nb = ttk.Notebook(root)

    page1 = ttk.Frame(nb)
    insert(page1)

    nb.add(page1, text='insert tool')

    nb.pack(fill=BOTH, expand=1)
    root.mainloop()
def insert(page):
    # path_filename = 'download_dir.txt'
    csv_label = Label(page, text = 'CSV_Path: ')
    csv_label.place(x=0,y=0)
    csv_path_var = StringVar()
    csv_path = Entry(page, textvariable = csv_path_var, bd=1, width = 35)
    csv_path.place(x=70,y=0)

    CSV_select = Button(page, text = '..', command = lambda: findFile(page, csv_path_var))
    CSV_select.place(x=440,y=0)

    table_label = Label(page, text = 'Table name: ')
    table_label.place(x=0,y=30)
    table = Entry(page, bd=1, width = 35)
    table.place(x=85,y=30)
    
    y_path = 550
    save_file_label = Label(page, text = 'Path: ')
    save_file_label.place(x=0,y=y_path)
    path_var = StringVar()
    path = Entry(page, textvariable = path_var, bd=1, width = 35)
    path.place(x=70,y=y_path)
    
    path_select = Button(page, text = '..', command = lambda: findDir(path_var))
    path_select.place(x=440,y=y_path)

    download_button = Button(page, text = 'create_insert_files', command = lambda: create_insert_file(path.get(), table.get())).pack(side=BOTTOM)
def create_insert_file(path, table_name):
    global list_Entry
    global reader
    global csvfile
    result = ""

    temp1 = "INSERT INTO "
    temp1 += table_name
    temp1 += " ("
    for attr in list_Entry:
        temp1 += attr.get()+", "
    temp1 = temp1[0:-2] + ")"
    temp1 += "VALUES ("

    next(reader)
    for row in reader:
        temp2 = temp1
        for j in range(len(row)):
            if re.match(r'[0-9]{4,5}-[0-9]{1,2}-[0-9]{1,2}', row[list_csv_key[j]]):
                temp2 += re.sub(r'([0-9]{4,5}-[0-9]{1,2}-[0-9]{1,2})',r"to_date('\1','YYYY-MM-DD')", row[list_csv_key[j]])+", "
            else:    
                temp2 += "\'"+row[list_csv_key[j]].replace("'","''")+"\'" + ", "
        temp2 = temp2[0:-2] + ");\n"
        result += temp2    
    result += "commit;"
    csvfile.seek(0)

    result_file = open(path.replace("/", "//")+"//insert_for_"+table_name+".txt", "w+")
    result_file.write(result)
    print("write successfully!")
        

def findDir(path_var): 
    directory = filedialog.askdirectory(initialdir='/',title=('Save Directory'))
    path_var.set(directory)
def findFile(page, path_var):
    current_y = 60
    add_per_y = 30
    current_x = 0
    add_per_x = 150
    global list_Entry 
    global list_csv_key
    list_Entry = []

    directory = filedialog.askopenfilename()
    path_var.set(directory)

    global csvfile
    csvfile = open(directory)
    global reader
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        for j, element in enumerate(row): 
            if j % 10 == 0 and j != 0:
                current_x += add_per_x
                current_y = 60
            current_y += add_per_y
            temp_Entry = Entry(page, bd=1, width=15)
            temp_Entry.insert(END, element)
            temp_Entry.place(x=current_x ,y=current_y)
            list_Entry.append(temp_Entry)
            list_csv_key.append(element)
        break
    csvfile.seek(0)

     

if __name__ == "__main__":
    Main()