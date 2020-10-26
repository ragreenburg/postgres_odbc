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


"""
I want to add the optiont to grab the headings
from the database and give the option to choose different 
databases so you can see them live.

select *
from inv_testing3
where false;

The above command will grab column names from the db.
"""


tb = "inv_testing3"

sql = f"SELECT * from {tb}"
cur.execute(sql)
rows = cur.fetchall()
total = cur.rowcount
#print(f"Total Data Entries: {total}")

#col_names = f"select * from {tb} where false;"
#cur.execute(col_names)
#row = cur.fetchall()
num_fields = len(cur.description)
field_names = [i[0] for i in cur.description]
#print(field_names)

win = Tk()
#frm = Frame(win)
#frm.pack(side=tk.LEFT, padx=20)
#frm.grid(row=5, column=0)

# ---------------------Trying to style the Treeview--------------------
style = ttk.Style()
style.configure(
    "mystyle.Treeview", highlightthickness=0.5, bd=0, font=("Calibri", 11)
)  # Modify the font of the body
style.configure(
    "mystyle.Treeview.Heading", font=("Calibri", 13, "bold")
)  # Modify the heading font
style.layout(
    "mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})]
)  # Remove borders
# ---------------------------------------------------------------------

tree = ttk.Treeview(
    win,
    columns=(
        1,2,3,4,5,6,7,8,9,10,11,
        12,13,14,15,16,17,18,19,20,21,22,
        23,24,25,26,27,28,29,30,31,32,33,
    ),
    displaycolumns="#all",
    show="headings",
    selectmode="extended",
    style="mystyle.Treeview",
)
tree.pack()
#tree.grid(row=4, column=1, padx=5)

# https://docs.python.org/3/library/tkinter.ttk.html#scrollable-widget-options
# https://docs.python.org/3/library/tkinter.ttk.html#column-identifiers
# https://docs.python.org/3/library/tkinter.ttk.html
# https://docs.python.org/3/library/tkinter.ttk.html#treeview
names = [
    'model', 'dimensions','frame','housing','tank size','tank material','compressor hp','condenser',
    'process pump hp','gpm @ 25 psi','weight','conn size','conn type','connection size','chiller pump hp',
    'heat exchanger','controls','electrical enclosure','shipping weight','decibals @ 10 feet','refrigerant',
    '230 1 FLA','230 1 MCA','230 1 MCO ','230 3 FLA','230 3 MCA','230 3 MCO','460 3 FLA','460 3 MCA','460 3 MCO',
    '20f','30f','40f']

"""
This might be the way to name the columns because they
are named differently in PostgreSQL because of how 
they need to be named for SQL. Either way though,
I am using a for loop towards the bottom to grab 
the info as of right now.
"""


for i in range(len(names)):
    tree.heading(i + 1, text=names[i])
    #tree.column(i + 1, minwidth=0, width=80, stretch=NO)
# Actually using my head for once and just making the for loop above and using that instead of defining each thing individually.

# tree.heading(1,text="Name")
# tree.heading(2,text="Age")
# tree.heading(3,text="Email")
# tree.heading(4,text="Naem")
# tree.heading(5,text="sfld")
# tree.heading(6,text="120")
# tree.heading(7,text="jh")
# tree.heading(8,text="aksdf")
# tree.heading(9,text="s;df")
# tree.heading(10,text="ljd")

scrlbr = ttk.Scrollbar(win, orient="horizontal", command=tree.xview)
#scrlbr.grid(row=10, column=3, columnspan=5)
# scrlbr.place(x=205, y=20, height=10)
scrlbr.pack(side='bottom', fill='x')
tree.configure(xscrollcommand=scrlbr.set)

for i in rows:
    tree.insert("", "end", values=i)

#for i in field_names:
#    print(field_names)
    #tree.heading(i, text=field_names[i])

"""
So the for loop below is used to grab the column 
names from the sql database and making it the header 
names for the Treeview
"""

    
#for i in range(len(field_names)):
#    tree.heading(i, text=field_names[i-1])
#    print(field_names[i])

    
win.title("Customer Data")
win.geometry("700x300")

# win.resizable(False, False)
win.mainloop()
