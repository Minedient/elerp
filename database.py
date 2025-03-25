### Python file to interact with the database ###
import sqlite3
from datetime import datetime as dt

# Function to create the database
# The database have two tables, one for the worksheets and another for the records of usage
# For the worksheets table, the columns are: sheet_id, name, description, upload_date, last_update, subject, form and teacher
# For the records table, the columns are: record_id, sheet_id (as foreign key), use_date, class, teacher

def findFormByClass(class_name: str) -> str:
    """
    Find the form of a class by its name
    
    Args:
        class_name (str): The class name

    Returns:
        str: The form of the class
    """
    splited = list(class_name)
    return 'Form ' + splited[0]

def findStageByClass(class_name: str) -> str:
    """
    Find the stage of a class by its name
    
    Args:
        class_name (str): The class name
        
    Returns:
        str: The stage of the class
    """
    splited = list(class_name)
    return 'Junior' if splited[0] == '1' or splited[0] == '2' or splited[0] == '3' else 'Senior'

def createDatabase(d_path: str) -> None:
    """
    Create the database with the tables worksheets, records and worksheet_paths, if it doesn't exist

    This is used to initialize the database when the application is first run

    @since 1.0.0
    @updated 1.1.0

    Args:
        d_path (str): The path to the database
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE worksheets
                 (sheet_id INTEGER PRIMARY KEY, name TEXT, description TEXT, upload_date TEXT, last_update TEXT, subject TEXT, form TEXT)''')
    c.execute('''CREATE TABLE records
                 (record_id INTEGER PRIMARY KEY, sheet_id INTEGER, use_date TEXT, class TEXT, teacher TEXT)''')
    c.execute('''CREATE TABLE worksheet_paths 
                 (path_id INTEGER PRIMARY KEY, sheet_id INTEGER, file_path TEXT, FOREIGN KEY (sheet_id) REFERENCES worksheets(sheet_id))''')
    c.execute('''CREATE TABLE class_records
                 (class_record_id INTEGER PRIMARY KEY, record_id INTEGER, section INTEGER, substituted_teacher TEXT, FOREIGN KEY (record_id) REFERENCES records(record_id))''')
    c.close()
    conn.commit()
    conn.close()

def createClassRecordTable(d_path: str) -> None:
    """
    Create a new table called class_records in the database
    
    The table store data about the substituted class itself, including which teacher is substituting and the section

    Used to upgrade from version 1.0.7 to 1.1.0

    Args:
        d_path (str): The path to the database
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE class_records
                 (class_record_id INTEGER PRIMARY KEY, record_id INTEGER, section INTEGER, substituted_teacher TEXT, FOREIGN KEY (record_id) REFERENCES records(record_id))''')
    c.close()
    conn.commit()
    conn.close()

def insertWorksheet(d_path:str, name:str, description:str, upload_date:str, subject:str, form:str, last_update = dt.now().strftime('%Y-%m-%d %H:%M:%S')) -> None:
    """
    Insert a new worksheet in the database

    Args:
        d_path (str): The path to the database
        name (str): The name of the worksheet
        description (str): The description of the worksheet
        upload_date (str): The date of the upload
        subject (str): The subject of the worksheet
        form (str): The form of the worksheet
        last_update (str): The date of the last update

    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO worksheets (name, description, upload_date, last_update, subject, form) VALUES (?, ?, ?, ?, ?, ?)", (name, description, upload_date, last_update, subject, form))
    c.close()
    conn.commit()
    conn.close()

def checkWorksheet(d_path: str, name: str) -> bool:
    """
    Check if a worksheet with the name exists in the database
    
    Args:
        d_path (str): The path to the database
        name (str): The name of the worksheet
        
    Returns:
        bool: True if the worksheet exists, False otherwise
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM worksheets WHERE name=?", (name,))
    worksheet = c.fetchone()
    conn.close()
    return worksheet

def getWorksheetId(d_path: str, name: str) -> int:
    """
    Get the id of a worksheet by its name
    
    Args:
        d_path (str): The path to the database
        name (str): The name of the worksheet
        
    Returns:
        int: The id of the worksheet
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT sheet_id FROM worksheets WHERE name=?", (name,))
    sheet_id = c.fetchone()
    conn.close()
    return sheet_id[0]

def getLatestRecordId(d_path: str) -> int:
    """
    Get the id of the latest record in the database
    
    Args:
        d_path (str): The path to the database
    
    Returns:
        int: The id of the latest record
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT record_id FROM records ORDER BY record_id DESC LIMIT 1")
    record_id = c.fetchone()
    conn.close()
    return record_id[0]

def alterWorksheetDateById(d_path: str, sheet_id: int, upload_date: str) -> None:
    """
    Alter the upload date of a worksheet by its id
    
    Args:
        d_path (str): The path to the database
        sheet_id (int): The id of the worksheet
        upload_date (str): The new upload date
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("UPDATE worksheets SET upload_date=? WHERE sheet_id=?", (upload_date, sheet_id))
    c.close()
    conn.commit()
    conn.close()

def insertWorksheetPath(d_path: str, sheet_id: int, file_path: str) -> None:
    """
    Insert a new worksheet path in the database
    
    Args:
        d_path (str): The path to the database
        sheet_id (int): The id of the worksheet
        file_path (str): The path to the worksheet
        
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO worksheet_paths (sheet_id, file_path) VALUES (?, ?, ?)", (sheet_id, file_path))
    c.close()
    conn.commit()
    conn.close()

def insertWorksheetAndPath(d_path: str, name: str, description: str, upload_date: str, subject: str, form: str, file_path: str, last_update = dt.now().strftime('%Y-%m-%d %H:%M:%S')):
    """
    Insert a new worksheet and its path in the database
    
    Args:
        d_path (str): The path to the database
        name (str): The name of the worksheet
        description (str): The description of the worksheet
        upload_date (str): The date of the upload
        subject (str): The subject of the worksheet
        form (str): The form of the worksheet
        file_path (str): The path to the worksheet
        last_update (str): The date of the last update
        
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO worksheets (name, description, upload_date, last_update, subject, form) VALUES (?, ?, ?, ?, ?, ?)", (name, description, upload_date, last_update, subject, form))
    sheet_id = c.lastrowid  # Get the last row id
    c.execute("INSERT INTO worksheet_paths (sheet_id, file_path) VALUES (?, ?)", (sheet_id, file_path))
    c.close()
    conn.commit()
    conn.close()

def findUnusedWorksheets(d_path: str, class_name: str) -> list:
    """
    Find all worksheets that have not been used by a specific class
    
    Args:
        d_path (str): The path to the database
        class_name (str): The class name

    Returns:
        list: A list with all unused worksheets
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT name, description, subject, form FROM worksheets WHERE sheet_id NOT IN (SELECT sheet_id FROM records WHERE class=?)", (class_name,))
    worksheets = c.fetchall()
    conn.close()
    return worksheets

def findUnusedWorksheetsMatchClass(d_path: str, class_name: str) -> list:
    """
    Find all worksheets that have not been used by a specific class and match the class form
    
    Args:
        d_path (str): The path to the database
        class_name (str): The class name

    Returns:
        list: A list with all unused worksheets that match the class form
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT name, description, subject, form FROM worksheets WHERE sheet_id NOT IN (SELECT sheet_id FROM records WHERE class=?) INTERSECT SELECT name, description, subject, form FROM worksheets WHERE form = ? OR form = ? OR form = 'All'", (class_name, findFormByClass(class_name), findStageByClass(class_name),))
    worksheets = c.fetchall()
    conn.close()
    return worksheets

def registerWorksheetUse(d_path: str, sheet_id: int, class_name: str, teacher: str) -> None:
    """
    Register the use of a worksheet in the database
    
    Args:
        d_path (str): The path to the database
        sheet_id (int): The id of the worksheet
        class_name (str): The class name
        teacher (str): The teacher name
    
    Returns:
        None
    """
    use_date = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO records (sheet_id, use_date, class, teacher) VALUES (?, ?, ?, ?)", (sheet_id, use_date, class_name, teacher))
    c.close()
    conn.commit()
    conn.close()

def registerClassRecord(d_path: str, record_id: int, section: int, substituted_teacher: str) -> None:
    """
    Register a class record in the database
    
    Args:
        d_path (str): The path to the database
        record_id (int): The id of the record
        section (int): The section of the class
        substituted_teacher (str): The teacher that is substituting
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("INSERT INTO class_records (record_id, section, substituted_teacher) VALUES (?, ?, ?)", (record_id, section, substituted_teacher))
    c.close()
    conn.commit()
    conn.close()

def getWorksheetPath(d_path: str, sheet_id: int) -> str:
    """
    Get the path of a worksheet by its id

    Args:
        d_path (str): The path to the database
        sheet_id (int): The id of the worksheet
    
    Returns:
        str: The path of the worksheet
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT file_path FROM worksheet_paths WHERE sheet_id=?", (sheet_id,))
    file_path = c.fetchone()
    conn.close()
    return file_path[0]

def latestRecords(d_path, amount = 15):
    """
    Get the latest records from the database, by default 15 records are returned

    Args:
        d_path (str): The path to the database
        amount (int): The amount of records to be returned (default is 15)
    
    Returns:
        list: A list with the latest records
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT r.teacher, r.class, w.name, r.use_date AS worksheet_name FROM records r INNER JOIN worksheets w ON r.sheet_id = w.sheet_id ORDER BY r.use_date DESC LIMIT ?", (amount,))
    records = c.fetchall()
    conn.close()
    return records

def latestUploads(d_path, amount = 15):
    """
    Get the latest uploads from the database, by default 15 uploads are returned

    Args:
        d_path (str): The path to the database
        amount (int): The amount of uploads to be returned (default is 15)

    Returns:
        list: A list with the latest uploads
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT w.name, w.subject, w.form, w.last_update FROM worksheets w ORDER BY w.last_update DESC LIMIT ?", (amount,))
    worksheets = c.fetchall()
    conn.close()
    return worksheets

def getWorksheetsCount(d_path):
    """
    Get the amount of worksheets in the database

    Args:
        d_path (str): The path to the database
    
    Returns:
        int: The amount of worksheets in the database
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM worksheets")
    count = c.fetchone()
    conn.close()
    return count[0]

def getWorksheets(d_path: str) -> list:
    """"
    Get all worksheets from the database
    
    Args:
        d_path (str): The path to the database
        
    Returns:
        list: A list with all worksheets
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM worksheets")
    worksheets = c.fetchall()
    conn.close()
    return worksheets

def getRecords(d_path: str) -> list:
    """
    Get all records from the database

    Args:
        d_path (str): The path to the database
    
    Returns:
        list: A list with all records
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM records")
    records = c.fetchall()
    conn.close()
    return records

def getClassRecords(d_path: str) -> list:
    """
    Get all class records from the database

    Args:
        d_path (str): The path to the database

    Returns:
        list: A list with all class records
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM class_records")
    class_records = c.fetchall()
    conn.close()
    return class_records

def getRecordsByClass(d_path: str, class_name: str) -> list:
    """
    Get all records registered with a specific class

    Args:
        d_path (str): The path to the database
        class_name (str): The class name

    Returns:
        list: A list with all records with the class name
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM records WHERE class=?", (class_name,))
    records = c.fetchall()
    conn.close()
    return records

def getRecordsByTeacher(d_path: str, teacher: str) -> list:
    """
    Get all records registered with a specific teacher

    Args:
        d_path (str): The path to the database
        teacher (str): The teacher name

    Returns:
        list: A list with all records with the teacher name
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM records WHERE teacher=?", (teacher,))
    records = c.fetchall()
    conn.close()
    return records

def getWorksheetPaths(d_path: str) -> list:
    """
    Get all worksheet paths from the database

    Args:
        d_path (str): The path to the database
        
    Returns:
        list: A list with all worksheet paths 
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT * FROM worksheet_paths")
    worksheet_paths = c.fetchall()
    conn.close()
    return worksheet_paths

def getUsageDetails(d_path: str) -> list:
    """
    Get the details of each usage.
    Including the worksheet name, class, teacher name, use date, section and substituted teacher
    If the correponsding record doesn't have a class record, the section and substituted teacher will be ignored as we can't create imaginary data

    Args:
        d_path (str): The path to the database

    Returns:
        list: A list with all usage details
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("SELECT r.record_id, r.class, r.teacher, w.name, r.use_date, cr.section, cr.substituted_teacher FROM records r LEFT JOIN class_records cr ON r.record_id = cr.record_id INNER JOIN worksheets w ON r.sheet_id = w.sheet_id")
    usage_details = c.fetchall()
    conn.close()
    return usage_details

def updateWorksheet(d_path: str, column: str, value: str, condition: str) -> None:
    """
    Update a worksheet in the database
    
    Args:
        d_path (str): The path to the database
        column (str): The column to be updated
        value (str): The new value
        condition (str): The condition to be met
        
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    query = """UPDATE worksheets SET {} = ? WHERE sheet_id = ?""".format(column)
    c.execute(query, (value, condition))
    c.close()
    conn.commit()
    conn.close()

def resetRecordsTable(d_path: str) -> None:
    """
    Reset the records table in the database
    
    Args:
        d_path (str): The path to the database
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("DELETE FROM records")
    c.close()
    conn.commit()
    conn.close()

def resetDatabaseToDefault(d_path: str) -> None:
    """
    Reset the database to its default state
    
    Args:
        d_path (str): The path to the database

    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("DELETE FROM worksheets")
    c.execute("DELETE FROM records")
    c.execute("DELETE FROM worksheet_paths")
    c.close()
    conn.commit()
    conn.close()

def removeRecord(d_path: str, record_id: int) -> None:
    """
    Remove a record from the database by its id
    
    Args:
        d_path (str): The path to the database
        record_id (int): The id of the record
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("DELETE FROM records WHERE record_id=?", (record_id,))
    c.close()
    conn.commit()
    conn.close()

def removeWorksheet(d_path: str, sheet_id: int) -> None:
    """
    Remove a worksheet from the database by its id
    This method is not recommanded to use unless it's necessary

    Args:
        d_path (str): The path to the database
        sheet_id (int): The id of the worksheet
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("DELETE FROM worksheets WHERE sheet_id=?", (sheet_id,))
    c.close()
    conn.commit()
    conn.close()

def removeWorksheetPath(d_path: str, sheet_id: int) -> None:
    """
    Remove a worksheet path from the database by its id
    This method is not recommanded to use unless it's necessary

    Args:
        d_path (str): The path to the database
        sheet_id (int): The id of the worksheet
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute("DELETE FROM worksheet_paths WHERE sheet_id=?", (sheet_id,))
    c.close()
    conn.commit()
    conn.close()

def runSQLCommand(d_path: str, command: str) -> None:
    """
    Run a SQL command in the database
    
    Args:
        d_path (str): The path to the database
        command (str): The SQL command
    
    Returns:
        None
    """
    conn = sqlite3.connect(d_path)
    c = conn.cursor()
    c.execute(command)
    result = c.fetchall()
    print(result)
    c.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    createDatabase('data/database.db')