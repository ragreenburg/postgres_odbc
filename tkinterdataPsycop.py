import os
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog, scrolledtext

import pandas as pd
import psycopg2

from Parts import comp_db, cond_db, edit_autofill, editdb, editing, parts_db

"""
dyanically changing oid:
This won't work as an oid is a primary key so it can not be changed.
Though there can be up to 2^32 -1 oid's so there is plenty of room
to space them out to make room for them to be inserted at a later time.
Though I do need to look into having the database ordered alphabetically.
Or rather look into organizing them before storing into the database.
"""

"""
8/7/2020
This is currently set up to connect to the same database but is using
psycopg2 instead of pyodbc because the syntax is easier to work with in psycopg2
and tkinter as apposed to pyodbc. If needed I can convert it to pyodbc without
a ton of challenges but I honesly don't want to. I have a similar script running
on pyodbc but the functionality isn't as good because it is more annoying to work with.
"""

"""
Some of these functions have (event=None) inside and that is because they 
are bound to a key input and need that so that the function will run on the key input
"""


# Connection modules
root = Tk()
root.title("G&D Chillers")
root.iconbitmap(
    r"C:\Users\Hank\Documents\Random Python Scripts\postgres-odbc\Icons\IconForTkinter.ico"
)
root.geometry("1000x400")
tb = "inv_testing3"

con_path = r"C:\Users\Hank\Documents\Random Python Scripts\postgres-odbc\Archive"
sys.path.insert(1, con_path)

from postgres_db import connect_to_database

conn, cur = connect_to_database()


def disconnect_from_db(dbconnection, cursor):
    # closes connecttion to database, I am almost certain this is useless
    cursor.close()
    dbconnection.close()


def add_to_row():
    answer = tkinter.messagebox.askquestion(
        "G & D Chillers", "Are you sure you want to commit data to database?"
    )
    if answer == "yes":
        try:
            sql = f"""INSERT INTO {tb} (model, dimensions, frame, housing, tank_size,
                    tank_mat, compressor_hp, condenser, process_pump_hp, gpm_at_25psi,
                    weight, conn_size, conn_type, chiller_pump_hp,
                    heat_exchanger, controls, electrical_enclosure, shipping_weight,
                    decibals_at_10_feet, refrigerant, _230_1_FLA, _230_1_MCA, _230_1_MCO,
                    _230_3_FLA, _230_3_MCA, _230_3_MCO, _460_3_FLA, _460_3_MCA, _460_3_MCO,
                    _20F, _30F, _40F) VALUES ('{model.get()}', '{dimensions.get()}', '{frame.get()}', 
                    '{housing.get()}', {tank_size.get()}, '{tank_mat.get()}', '{compressor_hp.get()}', 
                    '{condenser.get()}', {process_pump_hp.get()}, {gpm_at_25psi.get()},{weight.get()}, 
                    '{conn_size.get()}', '{conn_type.get()}', '{chiller_pump_hp.get()}','{heat_exchanger.get()}', 
                    '{controls.get()}', '{electrical_enclosure.get()}', '{shipping_weight.get()}',
                    {decibals_at_10_feet.get()}, '{refrigerant.get()}', '{_230_1_FLA.get()}', 
                    '{_230_1_MCA.get()}', '{_230_1_MCO.get()}','{_230_3_FLA.get()}', '{_230_3_MCA.get()}', 
                    '{_230_3_MCO.get()}', '{_460_3_FLA.get()}', '{_460_3_MCA.get()}', 
                    '{_460_3_MCO.get()}', '{_20F.get()}', '{_30F.get()}', '{_40F.get()}')
                    """
            print(sql)
            cur.execute(sql)
            tkinter.messagebox.showinfo(
                "G&D Chilllers", f"You have added {model.get()} to your database."
            )
            # This deletes the entries of the box after submitting the data.
            model.delete(0, END)
            dimensions.delete(0, END)
            frame.delete(0, END)
            housing.delete(0, END)
            tank_size.delete(0, END)
            tank_mat.delete(0, END)
            compressor_hp.delete(0, END)
            condenser.delete(0, END)
            process_pump_hp.delete(0, END)
            gpm_at_25psi.delete(0, END)
            weight.delete(0, END)
            conn_size.delete(0, END)
            conn_type.delete(0, END)
            connection_size.delete(0, END)
            chiller_pump_hp.delete(0, END)
            heat_exchanger.delete(0, END)
            controls.delete(0, END)
            electrical_enclosure.delete(0, END)
            shipping_weight.delete(0, END)
            decibals_at_10_feet.delete(0, END)
            refrigerant.delete(0, END)
            _230_1_FLA.delete(0, END)
            _230_1_MCA.delete(0, END)
            _230_1_MCO.delete(0, END)
            _230_3_FLA.delete(0, END)
            _230_3_MCA.delete(0, END)
            _230_3_MCO.delete(0, END)
            _460_3_FLA.delete(0, END)
            _460_3_MCA.delete(0, END)
            _460_3_MCO.delete(0, END)
            _20F.delete(0, END)
            _30F.delete(0, END)
            _40F.delete(0, END)
            conn.commit()
        except Exception as e:
            print(f"this is your error for add_to_row: \n {e}")
            warning = "Make sure that the entries are the proper data type ie numbers or words."
            tkinter.messagebox.showinfo(
                "G&D Chillers", f"Unable to add the data to the database. {warning}"
            )


"""
The query function button is commented out below becuase it basically
serves no real purpose when you have more than a handful of entries in
the database because it will take over the entire screen.
"""


def query():
    sql = f"SELECT * FROM {tb}"
    cur.execute(sql)
    records = cur.fetchall()
    # Loop through results and print them out.
    print_records = ""
    for record in records:
        # can change str(record) to str(record[0]) to get the first item and so on
        # Or so str(record[0]) + str(record[1]) to get the first two columns
        # \t puts a tab in, could be useful.
        print_records += str(record) + "\n"
    query_label = Label(root, text=print_records)
    query_label.grid(row=9, column=0, columnspan=2)
    conn.commit()


# This deletes the database entry by the model name. Not sure how to deal with it.
def delete():
    answer = tkinter.messagebox.askquestion(
        "G & D Chillers", "Are you sure you want to delete data to database?"
    )
    if answer == "yes":
        try:
            sql = f"DELETE from {tb} WHERE model = '{model.get()}'"
            cur.execute(sql)
            print(f"Model {model.get()} was deleted from {tb}")
            tkinter.messagebox.showinfo(
                "G&D Chillers", f"{model.get()} has been deleted from the database"
            )
            model.delete(0, END)
            dimensions.delete(0, END)
            frame.delete(0, END)
            housing.delete(0, END)
            tank_size.delete(0, END)
            tank_mat.delete(0, END)
            compressor_hp.delete(0, END)
            condenser.delete(0, END)
            process_pump_hp.delete(0, END)
            gpm_at_25psi.delete(0, END)
            weight.delete(0, END)
            conn_size.delete(0, END)
            conn_type.delete(0, END)
            connection_size.delete(0, END)
            chiller_pump_hp.delete(0, END)
            heat_exchanger.delete(0, END)
            controls.delete(0, END)
            electrical_enclosure.delete(0, END)
            shipping_weight.delete(0, END)
            decibals_at_10_feet.delete(0, END)
            refrigerant.delete(0, END)
            _230_1_FLA.delete(0, END)
            _230_1_MCA.delete(0, END)
            _230_1_MCO.delete(0, END)
            _230_3_FLA.delete(0, END)
            _230_3_MCA.delete(0, END)
            _230_3_MCO.delete(0, END)
            _460_3_FLA.delete(0, END)
            _460_3_MCA.delete(0, END)
            _460_3_MCO.delete(0, END)
            _20F.delete(0, END)
            _30F.delete(0, END)
            _40F.delete(0, END)
            conn.commit()
        except Exception as e:
            print(f"this is your error for delete: \n {e}")
            d_text = (
                "Unable to delete entry from database. Make sure that the model name"
            )
            tkinter.messagebox.showinfo(
                "G&D Chillers",
                f"{d_text} matches a model name from the database. Email hank@gdchillers.com if you have issues.",
            )


def add_to_csv():
    """
    This function will take the contents of the table in PostgreSQL
    and put them to a csv. May be needed if peole want to externally save the
    contents of the database in a public place that people can easily access
    i.e. pushing the csv to a public folder for the company to look at.
    """
    csv_exp = Tk()
    csv_exp.title("Update a record")
    csv_exp.geometry("300x300")
    csv_exp.iconbitmap(
        r"C:\Users\Hank\Documents\Random Python Scripts\postgres-odbc\Icons\IconForTkinter.ico"
    )
    csv_lab = "Click here to export CSV file"
    csv_button = Button(csv_exp, text=csv_lab, command=csv_2_xlsx)
    csv_button.grid(row=3, column=3, columnspan=2, pady=5, padx=5, ipadx=66)


# Adds the option to push a csv into the database.
def csv_to_postgres():
    answer = tkinter.messagebox.askquestion(
        "G & D Chillers", "Are you sure you want to import data from a CSV?"
    )
    if answer == "yes":

        csv_imp = Tk()
        csv_imp.title("Update a record")
        csv_imp.geometry("300x300")
        csv_imp.iconbitmap(
            r"C:\Users\Hank\Documents\Random Python Scripts\postgres-odbc\Icons\IconForTkinter.ico"
        )
        csv_lab = "Click here to impport a CSV file"
        csv_button = Button(csv_imp, text=csv_lab, command=file_opener)
        csv_button.grid(row=3, column=3, columnspan=2, pady=5, padx=5, ipadx=66)


def file_opener(event=None):
    # This is connected to csv_to_postgres
    # https://www.tutorialspoint.com/askopenfile-function-in-python-tkinter
    input = filedialog.askopenfile(
        initialdir="/", filetypes=[("CSV", "*.csv"), ("XLSX", "*.xlsx")]
    )
    # tb = "inv_testing3"
    try:
        sql = f"""COPY {tb} FROM STDIN DELIMITER ',' CSV HEADER;"""
        with open(input.name) as f:
            cur.copy_expert(sql, f)
        conn.commit()
        tkinter.messagebox.showinfo(
            "G&D Chillers", f"Your data has been imported from {input.name} to {tb}."
        )
    except Exception as e:
        print(f"this is your error for file_opener: \n {e}")
        words = """It is likely because it doesn't have the same column names.
        Please check and if you can't resolve the issue email hank@gdchillers.com"""
        tkinter.messagebox.showinfo(
            "G&D Chillers", f"There was an error uploading {input.name}. {words}"
        )


"""
This is mostly replaced by csv_2_xlsx, so feel free to delete this if you want.
"""


def save_file(event=None):
    # This is connected to add_to_csv
    # https://www.tutorialspoint.com/asksaveasfile-function-in-python-tkinter
    input = filedialog.asksaveasfilename(initialdir="/", filetypes=[("CSV", "*.csv")])
    if input == "":
        # This makes it so that the if they don't input a name it won't run the rest of the function.
        return
    try:
        sql1 = """ SELECT * FROM {}""".format(tb)
        rows = cur.execute(sql1)
        col_headers = [i[0] for i in cur.description]
        rows = [list(i) for i in cur.fetchall()]
        df = pd.DataFrame(rows, columns=col_headers)
        print(df)
        df.sort_values("tank_size", inplace=True)
        df.to_csv(input + ".csv", index=False)
        tkinter.messagebox.showinfo(
            "G&D Chillers", f"Your data has been exported to {input}"
        )
    except Exception as e:
        print(f"this is your error for save_file: \n {e}")
        words = "If this continues please email hank@gdchillers.com"
        tkinter.messagebox.showinfo(
            "G&D Chillers", f"There was an error downloading {input}.csv" + words
        )


def csv_2_xlsx(event=None):
    input = filedialog.asksaveasfilename(initialdir="/", filetypes=[("CSV", "*.csv")])
    if input == "":
        # This makes it so that the if they don't input a name it won't run the rest of the function.
        return
    try:
        import csv

        from openpyxl import Workbook

        # tb = "inv_testing3"
        sql1 = """ SELECT * FROM {}""".format(tb)
        rows = cur.execute(sql1)
        col_headers = [i[0] for i in cur.description]
        rows = [list(i) for i in cur.fetchall()]
        df = pd.DataFrame(rows, columns=col_headers)
        print(df)
        df.sort_values(
            "tank_size", inplace=True
        )  # This line is sorting the output of the database. FML, without having inplace=True it doesn't fucking work.
        print(df)
        df.to_csv(input + ".csv", index=False)
        print(f"{input}")
        tkinter.messagebox.showinfo("G&D Chillers", f"Your CSV was saved at {input}")
        ans = tkinter.messagebox.askquestion(
            "G&D Chillers", "Would you like to convert the CSV to an Excel file?"
        )
        if ans == "yes":
            print(f"{input}")
            wb = Workbook()
            ws = wb.active
            path = input + ".csv"
            print("Working Step 2")
            with open(path, "r") as f:
                for row in csv.reader(f):
                    ws.append(row)
            print("Working Step 3")
            xlsx_path = input + ".xlsx"
            wb.save(xlsx_path)
            print(
                f"Your csv has been converted to an Excel file and stored here {xlsx_path}"
            )
            tkinter.messagebox.showinfo(
                "G&D Chillers", f"Your Excel file was saved at {xlsx_path}"
            )
    except Exception as e:
        print(f"this is your error for csv_2_xlsx: \n {e}")
        tkinter.messagebox.showinfo(
            "G&D Chillers",
            f"You were unable to save your file {input}, {input}. If this issue continues please email hank@gdchillers.com",
        )


"""
Add a try and except and if it isn't an available option
to autofill/autocomplete then list the available chillers
that can be filled.

For some reason this isn't working. So right now it will run
whatever is done and won't ever throw up the exception.
It is also breaking in that if an entry doesn't have 
an entry for each grid then it will break the connection 
right there and stop filling out the columns.
So I am going to get rid of the try and except for now.
"""


def autofill(event=None):
    record_id = model.get()
    sql = f"SELECT * FROM {tb} where model = '{model.get()}'"
    print(sql)
    # try:
    cur.execute(sql)
    records = cur.fetchall()
    for record in records:
        dimensions.insert(0, record[1])
        frame.insert(0, record[2])
        housing.insert(0, record[3])
        tank_size.insert(0, record[4])
        tank_mat.insert(0, record[5])
        condenser.insert(0, record[6])
        compressor_hp.insert(0, record[7])
        process_pump_hp.insert(0, record[8])
        gpm_at_25psi.insert(0, record[9])
        weight.insert(0, record[10])
        conn_size.insert(0, record[11])
        conn_type.insert(0, record[12])
        connection_size.insert(0, record[13])
        chiller_pump_hp.insert(0, record[14])
        heat_exchanger.insert(0, record[15])
        controls.insert(0, record[16])
        electrical_enclosure.insert(0, record[17])
        shipping_weight.insert(0, record[18])
        decibals_at_10_feet.insert(0, record[19])
        refrigerant.insert(0, record[20])
        _230_1_FLA.insert(0, record[21])
        _230_1_MCA.insert(0, record[22])
        _230_1_MCO.insert(0, record[23])
        _230_3_FLA.insert(0, record[24])
        _230_3_MCA.insert(0, record[25])
        _230_3_MCO.insert(0, record[26])
        _460_3_FLA.insert(0, record[27])
        _460_3_MCA.insert(0, record[28])
        _460_3_MCO.insert(0, record[29])
        _20F.insert(0, record[30])
        _30F.insert(0, record[31])
        _40F.insert(0, record[32])

    # except:
    #    words = "Unable to auto complete the entries. Make sure you are spelling the model name properly"
    #    tkinter.messagebox.showinfo("G&D Chillers", f"{words}")


def delete_text(event=None):
    try:
        model.delete(0, END)
        dimensions.delete(0, END)
        frame.delete(0, END)
        housing.delete(0, END)
        tank_size.delete(0, END)
        tank_mat.delete(0, END)
        compressor_hp.delete(0, END)
        condenser.delete(0, END)
        process_pump_hp.delete(0, END)
        gpm_at_25psi.delete(0, END)
        weight.delete(0, END)
        conn_size.delete(0, END)
        conn_type.delete(0, END)
        connection_size.delete(0, END)
        chiller_pump_hp.delete(0, END)
        heat_exchanger.delete(0, END)
        controls.delete(0, END)
        electrical_enclosure.delete(0, END)
        shipping_weight.delete(0, END)
        decibals_at_10_feet.delete(0, END)
        refrigerant.delete(0, END)
        _230_1_FLA.delete(0, END)
        _230_1_MCA.delete(0, END)
        _230_1_MCO.delete(0, END)
        _230_3_FLA.delete(0, END)
        _230_3_MCA.delete(0, END)
        _230_3_MCO.delete(0, END)
        _460_3_FLA.delete(0, END)
        _460_3_MCA.delete(0, END)
        _460_3_MCO.delete(0, END)
        _20F.delete(0, END)
        _30F.delete(0, END)
        _40F.delete(0, END)
    except Exception as e:
        print(f"this is your error for delete_text: \n {e}")
        words = "I have never been able to produce this result so if you see this message please contact me at hank@gdchillers.com"
        tkinter.messagebox.showinfo(
            "G&D Chillers", f"Unable to delete entries for some reason. {words}"
        )


def contact_info(event=None):
    contact_email = "Please contact Hank at hank@gdchillers.com"
    tkinter.messagebox.showinfo("G&D Chillers", f"{contact_email}")


"""
Wanted to use a list here but there are issues printing lists to 
tkinters messagebox.
"""

def keyboard_shortcuts(event=None):
    ctrl_d = "Control+d = Delete Text \n"
    ctrl_a = "Control+a = Autofill \n"
    ctrl_s = "Control+s = Save to Excel \n"
    ctrl_i = "Control+i = Import CSV \n"
    ctrl_c = "Control+c = Contact Info \n"
    keyboard_shortcut_list = (
        f"A list of keyboard shortcuts: \n {ctrl_d} {ctrl_a} {ctrl_s} {ctrl_i} {ctrl_c}"
    )
    tkinter.messagebox.showinfo("G&D Chillers", f"{keyboard_shortcut_list}")


# ----------------Testing proper entries for DB ------------------------------
"""
There are 33 entries here so the only way to make it even is 3 rows of 11.
"""

model = Entry(root, width=30)
model.grid(row=0, column=1, padx=5)

dimensions = Entry(root, width=30)
dimensions.grid(row=1, column=1, padx=5)

frame = Entry(root, width=30)
frame.grid(row=2, column=1, padx=5)

housing = Entry(root, width=30)
housing.grid(row=3, column=1, padx=5)

tank_size = Entry(root, width=30)
tank_size.grid(row=4, column=1, padx=5)

tank_mat = Entry(root, width=30)
tank_mat.grid(row=5, column=1, padx=5)

compressor_hp = Entry(root, width=30)
compressor_hp.grid(row=6, column=1, padx=5)

condenser = Entry(root, width=30)
condenser.grid(row=7, column=1, padx=5)

process_pump_hp = Entry(root, width=30)
process_pump_hp.grid(row=8, column=1, padx=5)

gpm_at_25psi = Entry(root, width=30)
gpm_at_25psi.grid(row=9, column=1, padx=5)

weight = Entry(root, width=30)
weight.grid(row=10, column=1, padx=5)

conn_size = Entry(root, width=30)
conn_size.grid(row=0, column=3, padx=5)

conn_type = Entry(root, width=30)
conn_type.grid(row=1, column=3, padx=5)

connection_size = Entry(root, width=30)
connection_size.grid(row=2, column=3)

chiller_pump_hp = Entry(root, width=30)
chiller_pump_hp.grid(row=3, column=3, padx=5)

heat_exchanger = Entry(root, width=30)
heat_exchanger.grid(row=4, column=3, padx=5)

controls = Entry(root, width=30)
controls.grid(row=5, column=3, padx=5)

electrical_enclosure = Entry(root, width=30)
electrical_enclosure.grid(row=6, column=3, padx=5)

shipping_weight = Entry(root, width=30)
shipping_weight.grid(row=7, column=3, padx=5)

decibals_at_10_feet = Entry(root, width=30)
decibals_at_10_feet.grid(row=8, column=3, padx=5)

refrigerant = Entry(root, width=30)
refrigerant.grid(row=9, column=3, padx=5)

_230_1_FLA = Entry(root, width=30)
_230_1_FLA.grid(row=10, column=3, padx=5)

_230_1_MCA = Entry(root, width=30)
_230_1_MCA.grid(row=0, column=5, padx=5)

_230_1_MCO = Entry(root, width=30)
_230_1_MCO.grid(row=1, column=5, padx=5)

_230_3_FLA = Entry(root, width=30)
_230_3_FLA.grid(row=2, column=5, padx=5)

_230_3_MCA = Entry(root, width=30)
_230_3_MCA.grid(row=3, column=5, padx=5)

_230_3_MCO = Entry(root, width=30)
_230_3_MCO.grid(row=4, column=5, padx=5)

_460_3_FLA = Entry(root, width=30)
_460_3_FLA.grid(row=5, column=5, padx=5)

_460_3_MCA = Entry(root, width=30)
_460_3_MCA.grid(row=6, column=5, padx=5)

_460_3_MCO = Entry(root, width=30)
_460_3_MCO.grid(row=7, column=5, padx=5)

_20F = Entry(root, width=30)
_20F.grid(row=8, column=5, padx=5)

_30F = Entry(root, width=30)
_30F.grid(row=9, column=5, padx=5)

_40F = Entry(root, width=30)
_40F.grid(row=10, column=5, padx=5)


# ------------------Test Proper Entries for the database (text boxes) --------------------
model_label = Label(root, text="Model Name", pady=1)
model_label.grid(row=0, column=0)

dimensions_label = Label(root, text="Dimensions", pady=1)
dimensions_label.grid(row=1, column=0)

frame_label = Label(root, text="Frame", pady=1)
frame_label.grid(row=2, column=0)

housing_label = Label(root, text="Housing", pady=1)
housing_label.grid(row=3, column=0)

tank_size_label = Label(root, text="Tank Size", pady=1)
tank_size_label.grid(row=4, column=0)

tank_mat_label = Label(root, text="TankMat", pady=1)
tank_mat_label.grid(row=5, column=0)

compressor_hp_label = Label(root, text="Compressor HP", pady=1)
compressor_hp_label.grid(row=6, column=0)

condenser_label = Label(root, text="Condenser", pady=1)
condenser_label.grid(row=7, column=0)

process_pump_hp_label = Label(root, text="Process Pump HP", pady=1)
process_pump_hp_label.grid(row=8, column=0)

gpm_at_25psi_label = Label(root, text="GPM at 25 PSI", pady=1)
gpm_at_25psi_label.grid(row=9, column=0)

weight_label = Label(root, text="Weight", pady=1)
weight_label.grid(row=10, column=0)

conn_size_label = Label(root, text="ConnSize", pady=1)
conn_size_label.grid(row=0, column=2)

conn_type_label = Label(root, text="ConnType", pady=1)
conn_type_label.grid(row=1, column=2)

connection_size_label = Label(root, text="Connection Size", pady=1)
connection_size_label.grid(row=2, column=2)

chiller_pump_hp_label = Label(root, text="Chiller Pump HP", pady=1)
chiller_pump_hp_label.grid(row=3, column=2)

heat_exchanger_label = Label(root, text="Heat Exchanger", pady=1)
heat_exchanger_label.grid(row=4, column=2)

controls_label = Label(root, text="Controls", pady=1)
controls_label.grid(row=5, column=2)

electrical_enclosure_label = Label(root, text="Electrical Enlcosure", pady=1)
electrical_enclosure_label.grid(row=6, column=2)

shipping_weight_label = Label(root, text="Shipping Weight", pady=1)
shipping_weight_label.grid(row=7, column=2)

decibals_at_10_feet_label = Label(root, text="Decibals at 10 feet", pady=1)
decibals_at_10_feet_label.grid(row=8, column=2)

refrigerant_label = Label(root, text="Refrigerant", pady=1)
refrigerant_label.grid(row=9, column=2)

_230_1_FLA_label = Label(root, text="230-1-FLA", pady=1)
_230_1_FLA_label.grid(row=10, column=2)

_230_1_MCA_label = Label(root, text="230-1-MCA", pady=1)
_230_1_MCA_label.grid(row=0, column=4)

_230_1_MCO_label = Label(root, text="230-1-MCO", pady=1)
_230_1_MCO_label.grid(row=1, column=4)

_230_3_FLA_label = Label(root, text="230-3-FLA", pady=1)
_230_3_FLA_label.grid(row=2, column=4)

_230_3_MCA_label = Label(root, text="230-3-MCA", pady=1)
_230_3_MCA_label.grid(row=3, column=4)

_230_3_MCO_label = Label(root, text="230-3-MCO", pady=1)
_230_3_MCO_label.grid(row=4, column=4)

_460_3_FLA_label = Label(root, text="460-3-FLA", pady=1)
_460_3_FLA_label.grid(row=5, column=4)

_460_3_MCA_label = Label(root, text="460-3-MCA", pady=1)
_460_3_MCA_label.grid(row=6, column=4)

_460_3_MCO_label = Label(root, text="460-3-MCO", pady=1)
_460_3_MCO_label.grid(row=7, column=4)

_20F_label = Label(root, text="20 F", pady=1)
_20F_label.grid(row=8, column=4)

_30F_label = Label(root, text="30 F", pady=1)
_30F_label.grid(row=9, column=4)

_40F_label = Label(root, text="40 F", pady=1)
_40F_label.grid(row=10, column=4)


def change_dropdown(*args):
    if db_choices.get() == "Compressors":
        comp_db()
        print("Calling comp_db")
    if db_choices.get() == "Condensers":
        cond_db()
        print("Calling cond_db")
    if db_choices.get() == "Parts":
        parts_db()
        print("Calling parts_db")


# ------------------------Drop down menu---------------------------------------
db_choices = StringVar(root)
choices = {"Condensers", "Compressors", "Chillers", "Other", "Parts"}
db_choices.set("Chillers")
popup_menu = OptionMenu(root, db_choices, *choices)
popup_menu.grid(row=20, column=0)
db_choices.trace("w", change_dropdown)

# [X] Adding a menubar in the window
menubar = Menu(root)
files = Menu(menubar, tearoff=1)
"""
Might need to take this tearoff off.
I can see the usecase with it but at the same time others might not.
https://stackoverflow.com/questions/3485397/tkinter-dropdown-menu-with-keyboard-shortcuts
"""
menubar.add_cascade(label="Shortcuts", underline=0, menu=files)
files.add_command(label="Delete Inputs", accelerator="ctrl+d", command=delete_text)
files.add_command(label="Export CSV", accelerator="ctrl+s", command=csv_2_xlsx)
files.add_command(label="Import CSV", accelerator="ctrl+i", command=file_opener)
files.add_separator()
files.add_command(label="Contact Info", accelerator="ctrl+c", command=contact_info)
files.add_command(label="Keyboard Shortcuts", command=keyboard_shortcuts)

# -------------Create buttons to submit data------------------------------------
# Submits data to the database then clears the data.
# [X]This is completed with the new data
sub = "Add record to database"
submit_button = Button(root, text=sub, command=add_to_row)
submit_button.grid(row=18, column=1, columnspan=2, pady=5, padx=5, ipadx=100)

# ----------------------Creat query button--------------------------------------
# This will show all the records in the database, probably not useful.
# 9/14/2020 Commenting out this button because the database will almost certainly be too big to see
# In one window
# que = "See records"
# que_button = Button(root, text=que, command=query)
# que_button.grid(row=18, column=3, columnspan=2, pady=5, padx=5, ipadx=131)

# --------------------Autofill button-------------------------------------------
# [X] If there is an X here then this is working for all entries
fill = "Auto Complete Based on Model Name"
fill_button = Button(root, text=fill, command=autofill)
fill_button.grid(row=21, column=1, columnspan=4, pady=5, padx=5, ipadx=127)

# ---------------------Edit quantity button--------------------------------------
# [X]This needs to be verified
edit = "Edit Record"
edit_button = Button(root, text=edit, command=editing)
edit_button.grid(row=18, column=3, columnspan=2, pady=5, padx=5, ipadx=130)

# -------------------Create buttons to delete data-------------------------------
# [X]Hasn't been added into the backend
erase = "Delete record from database"
del_button = Button(root, text=erase, command=delete)
del_button.grid(row=19, column=1, columnspan=2, pady=5, padx=5, ipadx=85)

# ----------------Print out CSV button------------------------------------------
# [X] This works
csv_lab = "Print out to a CSV(Excel)"  # add_to_csv
csv_button = Button(root, text=csv_lab, command=csv_2_xlsx)
csv_button.grid(row=19, column=3, columnspan=2, pady=5, padx=5, ipadx=97.5)

# -------------Create buttons to add csv data------------------------------------
# Submits data to the database then clears the data.
# [X]This works but only when the columns are the same name but that will always be a restriction.
imp = "Import csv record to database"  # csv_to_postgres
submit_button = Button(root, text=imp, command=file_opener)
submit_button.grid(row=20, column=1, columnspan=4, pady=5, padx=5, ipadx=150)

# --------------------Key Bindings link below -------------------------------------
# https://stackoverflow.com/questions/56041280/accelerators-not-working-in-python-tkinter-how-to-fix
root.bind_all("<Control-d>", delete_text)
root.bind_all("<Control-a>", autofill)
root.bind_all("<Control-s>", csv_2_xlsx)
root.bind_all("<Control-i>", file_opener)
root.bind_all("<Control-c>", contact_info)
root.bind_all("<Control-e>", editing)

# This will make it so the window can't be resized. Might be worth doing if I
# Can't figure out how to make it change dynamically with grid.
root.config(menu=menubar)
root.resizable(0, 0)
root.mainloop()
