from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext
import tkinter.messagebox
import psycopg2
import pandas as pd

con_path = r"C:\Users\Hank\Documents\Random Python Scripts\postgres-odbc\Archive"
sys.path.insert(1, con_path)

from postgres_db import connect_to_database

conn, cur = connect_to_database()

"""
This is in alpha mode right now because 
I still need to get the scrollbar to work.
Not sure exactly what is going on and why
it isn't working.
"""


tb = "inv_testing3"

sql = f"SELECT * from {tb}"
cur.execute(sql)
rows = cur.fetchall()
total = cur.rowcount
print(f"Total Data Entries: {total}")

win = Tk()
frm = Frame(win)
frm.pack(side=tk.LEFT, padx=20)

tv = ttk.Treeview(frm, columns=(1,2,3,4,5,6,7,8,9,10), show="headings", selectmode="browse")
tv.pack()

tv.heading(1,text="Name")
tv.heading(2,text="Age")
tv.heading(3,text="Email")
tv.heading(4,text="Naem")
tv.heading(5,text="sfld")
tv.heading(6,text="120")
tv.heading(7,text="jh")
tv.heading(8,text="aksdf")
tv.heading(9,text="s;df")
tv.heading(10,text="ljd")


"""
This place() needs to be worked on. As of right now it 
isn't ideal and kind of sucks big time.
Here is info on what to do:
https://stackoverflow.com/questions/41877848/python-treeview-scrollbar
"""

#scrlbr = ttk.Scrollbar(win, orient="horizontal", command=tv.xview)
#scrlbr.place(x=205, y=20, height=10)
#scrlbr.pack(side='bottom', fill='x')
#tv.configure(xscrollcommand=scrlbr.set)

for i in rows:
    tv.insert('','end', values=i)

win.title("Customer Data")
win.geometry("300x300")

#win.resizable(False, False)
win.mainloop()
