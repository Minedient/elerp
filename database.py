### Python file to interact with the database ###
import sqlite3
from datetime import datetime as dt

# Function to create the database
# The database have two tables, one for the worksheets and another for the records of usage
# For the worksheets table, the columns are: sheet_id, name, description, upload_date, last_update, subject, form and teacher
# For the records table, the columns are: record_id, sheet_id (as foreign key), use_date, class, teacher

def findFormByClass(class_name):
    splited = list(class_name)
    return 'Form ' + splited[0]

def findStageByClass(class_name):
    splited = list(class_name)
    return 'Junior' if splited[0] == '1' or splited[0] == '2' or splited[0] == '3' else 'Senior'

def create_database(d_path):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE worksheets
                 (sheet_id INTEGER PRIMARY KEY, name TEXT, description TEXT, upload_date TEXT, last_update TEXT, subject TEXT, form TEXT)''')
    c.execute('''CREATE TABLE records
                 (record_id INTEGER PRIMARY KEY, sheet_id INTEGER, use_date TEXT, class TEXT, teacher TEXT)''')
    c.execute('''CREATE TABLE worksheet_paths 
                 (path_id INTEGER PRIMARY KEY, sheet_id INTEGER, file_path TEXT, FOREIGN KEY (sheet_id) REFERENCES worksheets(sheet_id))''')
    c.close()
    conn.commit()
    conn.close()

def insertWorksheet(d_path, name, description, upload_date, subject, form, last_update = dt.now().strftime('%Y-%m-%d %H:%M:%S')):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO worksheets (name, description, upload_date, last_update, subject, form) VALUES (?, ?, ?, ?, ?, ?)", (name, description, upload_date, last_update, subject, form))
    c.close()
    conn.commit()
    conn.close()

def checkWorksheet(d_path, name):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM worksheets WHERE name=?", (name,))
    worksheet = c.fetchone()
    conn.close()
    return worksheet

def getWorksheetId(d_path, name):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT sheet_id FROM worksheets WHERE name=?", (name,))
    sheet_id = c.fetchone()
    conn.close()
    return sheet_id[0]

def alterWorksheetDateById(d_path, sheet_id, upload_date):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("UPDATE worksheets SET upload_date=? WHERE sheet_id=?", (upload_date, sheet_id))
    c.close()
    conn.commit()
    conn.close()

def insertWorksheetPath(d_path, sheet_id, file_path):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO worksheet_paths (sheet_id, file_path) VALUES (?, ?, ?)", (sheet_id, file_path))
    c.close()
    conn.commit()
    conn.close()

def insertWorksheetAndPath(d_path, name, description, upload_date, subject, form, file_path, last_update = dt.now().strftime('%Y-%m-%d %H:%M:%S')):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO worksheets (name, description, upload_date, last_update, subject, form) VALUES (?, ?, ?, ?, ?, ?)", (name, description, upload_date, last_update, subject, form))
    sheet_id = c.lastrowid  # Get the last row id
    c.execute("INSERT INTO worksheet_paths (sheet_id, file_path) VALUES (?, ?)", (sheet_id, file_path))
    c.close()
    conn.commit()
    conn.close()

def findUnusedWorksheets(d_path, class_name):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT name, description, subject, form FROM worksheets WHERE sheet_id NOT IN (SELECT sheet_id FROM records WHERE class=?)", (class_name,))
    worksheets = c.fetchall()
    conn.close()
    return worksheets

def findUnusedWorksheetsMatchClass(d_path, class_name):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT name, description, subject, form FROM worksheets WHERE sheet_id NOT IN (SELECT sheet_id FROM records WHERE class=?) INTERSECT SELECT name, description, subject, form FROM worksheets WHERE form = ? OR form = ? OR form = 'All'", (class_name, findFormByClass(class_name), findStageByClass(class_name),))
    worksheets = c.fetchall()
    conn.close()
    return worksheets

def registerWorksheetUse(d_path, sheet_id, class_name, teacher):
    use_date = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO records (sheet_id, use_date, class, teacher) VALUES (?, ?, ?, ?)", (sheet_id, use_date, class_name, teacher))
    c.close()
    conn.commit()
    conn.close()

def getWorksheetPath(d_path, sheet_id):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT file_path FROM worksheet_paths WHERE sheet_id=?", (sheet_id,))
    file_path = c.fetchone()
    conn.close()
    return file_path[0]

def latestRecords(d_path, amount = 15):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT r.teacher, r.class, w.name, r.use_date AS worksheet_name FROM records r INNER JOIN worksheets w ON r.sheet_id = w.sheet_id ORDER BY r.use_date DESC LIMIT ?", (amount,))
    records = c.fetchall()
    conn.close()
    return records

def latestUploads(d_path, amount = 15):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT w.name, w.subject, w.form, w.last_update FROM worksheets w ORDER BY w.last_update DESC LIMIT ?", (amount,))
    worksheets = c.fetchall()
    conn.close()
    return worksheets

def getWorksheetsCount(d_path):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM worksheets")
    count = c.fetchone()
    conn.close()
    return count[0]

# Function to insert a new record in the database
def insert_record(d_path, sheet_id, use_date, class_name, teacher):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO records (sheet_id, use_date, class, teacher) VALUES (?, ?, ?, ?)", (sheet_id, use_date, class_name, teacher))
    c.close()
    conn.commit()
    conn.close()

def getWorksheets(d_path):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM worksheets")
    worksheets = c.fetchall()
    conn.close()
    return worksheets

def getRecords(d_path):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM records")
    records = c.fetchall()
    conn.close()
    return records

def getWorksheetPaths(d_path):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM worksheet_paths")
    worksheet_paths = c.fetchall()
    conn.close()
    return worksheet_paths

def updateWorksheet(d_path, column, value, condition):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    query = """UPDATE worksheets SET {} = ? WHERE sheet_id = ?""".format(column)
    c.execute(query, (value, condition))
    c.close()
    conn.commit()
    conn.close()

def resetRecordsTable(d_path):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("DELETE FROM records")
    c.close()
    conn.commit()
    conn.close()

def resetDatabaseToDefault(d_path):
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("DELETE FROM worksheets")
    c.execute("DELETE FROM records")
    c.execute("DELETE FROM worksheet_paths")
    c.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database('data/database.db')
    #resetDatabaseToDefault('data/database.db')
    #alterWorksheetDateById('data/database.db', 1, '2024-12-23 15:44:39')
    pass