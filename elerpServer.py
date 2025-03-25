from datetime import datetime
import json
import sys
import socket, threading
from src.protocol import REQUEST, ExecutorScope, ProtocolExecutor, ProtocolData, ProtocolHandler, RESPONSE, STATUS
from src.helper import sendMessage, recvMessage
import database as db
from src.networking import createUDPThread, createTCPThread
import argparse

import base64
import traceback
import os
import logging, colorlog

from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QMessageBox, QDialog
from PySide6.QtCore import QTimer, Qt

### GUI ###
from ui.management_ui import Ui_MainWindow
from ui.entryRemoveWizard_ui import Ui_EntryRemoveWizard

LOCAL_IP = socket.gethostbyname(socket.gethostname())
PRODUCTION_UDP_PORT = 19864
PRODUCTION_TCP_PORT = 19865
DEVELOPMENT_UDP_PORT = 19866
DEVELOPMENT_TCP_PORT = 19867
SOCKETS = {'udp': PRODUCTION_UDP_PORT, 'tcp': PRODUCTION_TCP_PORT, 'socket_udp': None, 'socket_tcp': None}

SERVER_VERSION = '2.0.0'

# Resources Path
RESOURCES_PATH = 'res/'

# Database Path
DATABASE_PATH = 'data/database.db'

# Worksheet Path
WORKSHEET_PATH = 'data/worksheets/'

# Setup logging module with colorlog, it should only log with WARNING level or higher
logger = logging.getLogger('elerpServer')
logger.setLevel(logging.DEBUG)

logHandler = logging.StreamHandler()
logHandler.setLevel(logging.WARNING)

# Setup file logging
fileHandler = logging.FileHandler('runtime.log')
fileHandler.setLevel(logging.INFO)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", 
    log_colors={ 'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red', }
)
fileFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logHandler.setFormatter(formatter)
fileHandler.setFormatter(fileFormatter)

logger.addHandler(logHandler)
logger.addHandler(fileHandler)

handler = ProtocolHandler()

addressbook = {}

stop = threading.Event()

progRes = None

database_metadata = {
    'count': db.getWorksheetsCount(DATABASE_PATH)   # Only update when there are changes on the database
}

def udpService(data: ProtocolData, addr: tuple):
    """
    The new UDP service function focus on handling the message from the client,
    while the loop is abstracted away in networking.py.

    Args:
        data (ProtocolData): The data received from the client.
        socket (socket): The socket object to send the message back to the client.
        The args have to match the signature of the function in networking.py
    Returns:
        None
    """
    def sendToClient(_):
        """
        Send a message to upcoming potential client.

        Returns:
            None
        """
        message = handler.prepMessage(RESPONSE.OK, mainMessage=LOCAL_IP).serializeMessage()
        logger.info(f'Client found: {addr}')
        logger.info(f'Sending server ip: {LOCAL_IP} to {addr} and wait for TCP connection')
        SOCKETS['socket_udp'].sendto(message.encode(), addr)

    executor = ProtocolExecutor(data)
    executor.addMessageHandler(sendToClient, REQUEST.POST, 'elerp_client', ExecutorScope.COMMAND)
    try:
        executor.executeHandlers()
    except ValueError as e:
        e.with_traceback()
        # The incoming message is send by an invalid client that uses the same protocol, but looking for other server
        message = handler.prepMessage(RESPONSE.ERROR, mainMessage=STATUS.INVALID_REQUEST).serializeMessage()
        logger.warning(f'Invalid client found: {addr} with message {data}')
        SOCKETS['socket_udp'].sendto(message.encode(), addr)

def tcpService(conn: socket.socket, addr: tuple):
    """
    The new TCP service function focus on handling the message from the client,
    while the loop is abstracted away in networking.py.
    
    Args:
        conn (socket): The connection object.
        addr (tuple): The address of the client.

    Returns:
        None
    """
    logger.info(f'Connected by {addr} via TCP')
    clientService = threading.Thread(target=clientHandler, args=(conn, addr, stop))
    clientService.daemon = True
    clientService.start()

def handelUpload(request:dict) -> str:
    """
    Handle the upload request from the client.
    The function will check if all infoormation is provided and then save the file to the server.
    Afterward it will return a message indicating the result of the upload action.

    request (dict): The upload request containing the following keys:
        - fileData (str): Base64 encoded file data.
        - form (str): The form identifier.
        - subject (str): The subject identifier.
        - name (str): The name of the file.
        - description (str): The description of the file.
        - creationDate (str): The creation date of the file.
    str: Serialized message indicating the result of the upload action.

    Args:
        request (dict): The upload request.

    Returns:
        result: The result of the upload action
    """
    fileData = request['fileData']
    form = request['form']
    subject = request['subject']
    name = request['name']
    description = request['description']
    creationDate = request['creationDate']
    
    # Check if the form, subject, name and data are provided
    if form is None or subject is None or name is None or fileData is None:
        return handler.prepMessage(RESPONSE.ERROR, mainMessage=STATUS.EMPTY_PARAMETER).serializeMessage()
    
    form = progRes['forms'][form]   # Get the form from the resources
    subject = progRes['subjects'][subject]  # Get the subject from the resources


    # Check if the form and subject are valid
    if form is None or subject is None:
        return handler.prepMessage(RESPONSE.ERROR, mainMessage=STATUS.INVALID_PARAMETER).serializeMessage()

    #try to convert the data back to file
    try:
        os.makedirs(WORKSHEET_PATH, exist_ok=True)
        with open(os.path.join(WORKSHEET_PATH, name), 'wb') as file:
            file.write(base64.b64decode(fileData.encode()))
            file.close()
    except:
        traceback.print_exc()
        return handler.prepMessage(RESPONSE.ERROR, mainMessage=STATUS.UPLOAD_FAILED).serializeMessage()

    db.insertWorksheetAndPath(DATABASE_PATH, name, description, creationDate, subject['name'], form['name'], os.path.join(WORKSHEET_PATH, name))
    return handler.prepMessage(RESPONSE.OK, mainMessage=STATUS.SUCCESS).serializeMessage()

def getTestHandler(_, conn, ip):
    logger.info(f'Test request received from {addressbook[ip]}')
    reply = handler.prepMessage(RESPONSE.OK).serializeMessage()
    sendMessage(conn, reply.encode())

def getVersionHandler(_, conn, ip):
    logger.info(f'Version request received from {addressbook[ip]}')
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=SERVER_VERSION).serializeMessage()
    sendMessage(conn, reply.encode())
    
def getGlobalDataHandler(_, conn, ip):
    logger.info(f'Global data request received from {addressbook[ip]}')
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=json.dumps(progRes)).serializeMessage()
    sendMessage(conn, reply.encode())

def getRecentUsageHandler(_, conn, ip):
    logger.info(f'Recent usage request received from {addressbook[ip]}')
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=json.dumps(db.latestRecords(DATABASE_PATH))).serializeMessage()
    sendMessage(conn, reply.encode())

def getRecentUploadedHandler(_, conn, ip):
    logger.info(f'Recent uploaded request received from {addressbook[ip]}')
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=json.dumps(db.latestUploads(DATABASE_PATH))).serializeMessage()
    sendMessage(conn, reply.encode())

def getUnusedWorksheets(message, conn, ip):
    logger.info(f'Unused worksheets request received from {addressbook[ip]}')
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=json.dumps(db.findUnusedWorksheetsMatchClass(DATABASE_PATH, message['class']))).serializeMessage()
    sendMessage(conn, reply.encode())

def postUploadWorksheet(message, conn, ip):
    logger.info(f'Upload request received from {addressbook[ip]}')
    reply = handelUpload(message)
    sendMessage(conn, reply.encode())

    # Update the database metadata to reflect the changes
    database_metadata['count'] = db.getWorksheetsCount(DATABASE_PATH)

def postRegisterUsage(message, conn, ip):
    """
    Handle the register usage request from the client.
    Worksheet and class record will be registered in the database seperately as the old version did not track the class record.
    And logically, worksheet and class record should be seperated anyway.
    
    Args:
        message (dict): The message containing the following
            - worksheet (str): The name of the worksheet.
            - class (str): The class identifier.
            - teacher (str): The teacher identifier.
            - section (str): The section identifier.
            - subTeacher (str): The sub teacher identifier.
        conn (socket): The connection object.
        ip (str): The ip address of the client.
        
    Returns:
        None
    """
    logger.info(f'Register usage request received from {addressbook[ip]}')
    w_id = db.getWorksheetId(DATABASE_PATH, message['worksheet'])
    path = db.getWorksheetPath(DATABASE_PATH, w_id)
    with open(path, 'rb') as file:
        fileData = file.read()
        file.close()
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=fileData).serializeMessage()
    sendMessage(conn, reply.encode())
    logger.info(f'Sending worksheet to {addressbook[ip]}')
    db.registerWorksheetUse(DATABASE_PATH, w_id, message['class'], message['teacher'])  # Register the worksheet is used on class X by teacher Y
    r_id = db.getLatestRecordId(DATABASE_PATH)
    db.registerClassRecord(DATABASE_PATH, r_id, message['section'], message['subTeacher'])  # Register the class record

def getTotalWorksheets(_, conn, ip):
    logger.info(f'Total worksheets request received from {addressbook[ip]}')
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=database_metadata['count']).serializeMessage()
    sendMessage(conn, reply.encode())

def clientHandler(conn, addr, stop: threading.Event):
    """
    Handle the client connection. The function will keep listening for messages from the client.
    and send replies back to the client. The function will stop when the client disconnects.

    Args:
        conn: The connection object.
        addr: The address of the client.

    Returns:
        None
    """
    executor = ProtocolExecutor()

    # The GET requests
    executor.addMessageHandler(lambda _: getTestHandler(_, conn, ip), requestCommand='testConnection')
    executor.addMessageHandler(lambda _: getVersionHandler(_, conn, ip), requestCommand='checkVersion')
    executor.addMessageHandler(lambda _: getGlobalDataHandler(_, conn, ip), requestCommand='globalData')
    executor.addMessageHandler(lambda _: getRecentUsageHandler(_, conn, ip), requestCommand='recentUsage')
    executor.addMessageHandler(lambda _: getRecentUploadedHandler(_, conn, ip), requestCommand='recentUploaded')
    executor.addMessageHandler(lambda message: getUnusedWorksheets(message, conn, ip), requestCommand='unusedWorksheets', scope=ExecutorScope.MESSAGE)
    executor.addMessageHandler(lambda message: postUploadWorksheet(message, conn, ip), requestType=REQUEST.POST, requestCommand='uploadWorksheet', scope=ExecutorScope.MESSAGE)
    executor.addMessageHandler(lambda message: postRegisterUsage(message, conn, ip), requestType=REQUEST.POST, requestCommand='registerUsage', scope=ExecutorScope.MESSAGE)
    executor.addMessageHandler(lambda _: getTotalWorksheets(_, conn, ip), requestCommand='totalWorksheets')
    while not stop.is_set():
        try:
            data = recvMessage(conn) # Receive the message from the client
            if not data:
                break

            ip = addr[0]
            addressbook[ip] = socket.gethostbyaddr(ip)[0] if socket.gethostbyaddr(ip)[0] not in addressbook else addressbook[ip] # Add the client to the addressbook

            decoded = handler.deserializeMessageAsProtocolData(data.decode())
            executor.setMessage(decoded)
            executor.executeHandlers()

        except ConnectionResetError:
            logger.info(f'Closing connection with {addressbook[ip]}')
            conn.close()
            break
    conn.close()
        
class EditHistory:
    def __init__(self, table, row, column, oldValue, newValue):
        self.table = table
        self.row = row
        self.column = column
        self.oldValue = oldValue
        self.newValue = newValue

    def __str__(self):
        return f'{self.table} - Row: {self.row}, Column: {self.column}, Old Value: {self.oldValue}, New Value: {self.newValue}'

class ManagementUI(QMainWindow):
        
    def __init__(self):
        super(ManagementUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QTimer()
        self.editHistories: list[EditHistory] = []

        def setupTable(table: QTableWidget, headers: list):
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)

        # Set up the tables
        setupTable(self.ui.worksheetTable, ['ID', 'Name', 'Description', 'Upload Date', 'Last Update Date', 'Subject', 'Form'])
        setupTable(self.ui.recordTable, ['ID', 'WorksheetID', 'Use Date', 'Class', 'Teacher'])
        setupTable(self.ui.pathTable, ['ID', 'WorksheetID', 'File Path'])
        setupTable(self.ui.classRecordTable, ['ID', 'RecordID', 'Section', 'Substituted Teacher'])
            
        self.refreshTables()

        # Do the hook after the tables are set up
        self.ui.worksheetTable.itemChanged.connect(lambda item: self.addEditHistory('worksheet', item.row(), item.column(), self.allWorksheets[item.row()][item.column()], item.text()))

        self.ui.editTrigger.toggled.connect(self.setTableEditModes)
        self.ui.refreshButton.clicked.connect(self.refreshTables)
        self.ui.saveButton.clicked.connect(self.saveChanges)
        self.ui.masterDataButton.clicked.connect(self.saveMasterData)

        # Pass the tab names to the remove entry wizard
        self.ui.removeEntryButton.clicked.connect(lambda: self.runRemoveEntryWizard(['Worksheet', 'Record']))
        
    def closeEvent(self, event):
        if len(self.editHistories) > 0:
            isSave = QMessageBox.question(self, 'Save changes', 'There are unsaved changes. Are you sure you want to close?', QMessageBox.Yes | QMessageBox.No)
            if isSave == QMessageBox.Yes:
                self.saveChanges()
                return super().closeEvent(event)
            else:
                return event.ignore()

    def addEditHistory(self, table, row, column, oldValue, newValue):
        if oldValue != newValue:
            self.editHistories.append(EditHistory(table, row, column, oldValue, newValue))

    def columnName(self, table, column):
        if table == 'worksheet':
            return ['sheet_id', 'name', 'description', 'upload_date', 'last_update', 'subject', 'form'][column]

    def saveChanges(self):
        # if nothing is changed, do nothing
        if len(self.editHistories) == 0:
            self.setTempMessage('No changes to save')
            return

        # if the user doesn't want to save the changes, do nothing
        isSave = QMessageBox.question(self, 'Save changes', 'Are you sure you want to save the changes?', QMessageBox.Yes | QMessageBox.No)
        if isSave == QMessageBox.No:
            return

        logger.info('Saving changes in management GUI')
        for edit in self.editHistories:
            if edit.table == 'worksheet':
                db.updateWorksheet(DATABASE_PATH, self.columnName(edit.table, edit.column), edit.newValue, self.allWorksheets[edit.row][0])
        self.setTempMessage('Changes saved')
        self.editHistories.clear()  # Clear the edit histories

        self.ui.worksheetTable.blockSignals(True)
        self.refreshTables()    # Refresh the tables to reflect the changes, signal blocking is enabled to prevent the edit signals from being triggered
        self.ui.worksheetTable.blockSignals(False)

    def setTableEditModes(self):
        self.ui.worksheetTable.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed | QTableWidget.AnyKeyPressed if self.ui.editTrigger.isChecked() else QTableWidget.NoEditTriggers)
        self.setTempMessage('Edit mode enabled' if self.ui.editTrigger.isChecked() else 'Edit mode disabled')

    def setTempMessage(self, message: str):
        self.timer.stop() if self.timer.isActive() else None
        self.ui.tempMessageLabel.setText(message)
        self.timer.setInterval(3000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.ui.tempMessageLabel.setText(''))
        self.timer.start()

    def runRemoveEntryWizard(self, tablesNames: list[str]):
        wizard = EntryRemoveWizard(tablesNames)
        wizard.exec()

    def refreshTables(self):
        logger.info('Refreshing tables in management GUI')
        self.allWorksheets = db.getWorksheets(DATABASE_PATH)
        self.allWorksheetPaths = db.getWorksheetPaths(DATABASE_PATH)
        self.allRecords = db.getRecords(DATABASE_PATH)
        self.allClassRecords = db.getClassRecords(DATABASE_PATH)

        def populateTable(table: QTableWidget, data, non_editable_columns: list):
            table.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(item)))
                    if j in non_editable_columns:
                        table.item(i, j).setFlags(table.item(i, j).flags() & ~Qt.ItemIsEditable)
            table.resizeColumnsToContents()

        populateTable(self.ui.worksheetTable, self.allWorksheets, [0, 1, 3, 4])
        populateTable(self.ui.recordTable, self.allRecords, [0, 1, 2, 3, 4])
        populateTable(self.ui.pathTable, self.allWorksheetPaths, [0, 1, 2])
        populateTable(self.ui.classRecordTable, self.allClassRecords, [0, 1, 2, 3])

        self.editHistories.clear()  # Clear the edit histories, as the tables are refreshed
        self.setTempMessage('Tables refreshed')

    def saveMasterData(self):
        """
        Save the master data to the resources file.
        """
        logger.info('Saving master data')
        data = db.getUsageDetails(DATABASE_PATH)
        currentTime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        with open(f'{currentTime}_masterData.csv', 'w', encoding='utf-8') as file:
            file.write('Record ID, Class, Teacher, Worksheet, Use Date, Section, Substituted Teacher\n')
            for record in data:
                file.write(','.join(map(str, record)) + '\n')
        self.setTempMessage('Master data saved')


class EntryRemoveWizard(QDialog):
    """
    A wizard GUI element used to remove entries from the database.

    The user first select the table to remove the entry from, then the user selects the row to remove.

    After pressing the remove button, the wizard will ask the user if they are sure to remove the entry.

    If the user confirms, the entry will be removed from the database, and a refresh signal will be sent to the main window to update the tables.

    When the user press the finish button, the wizard will close and the main management window will be updated.
    """
    def __init__(self, tablesNames: list[str]):
        super(EntryRemoveWizard, self).__init__()
        self.ui = Ui_EntryRemoveWizard()
        self.ui.setupUi(self)

        self.ui.tableCombox.currentIndexChanged.connect(self.fillTableData)
        self.ui.tableCombox.addItems(tablesNames)

        self.ui.removeButton.clicked.connect(self.removeEntry)
        self.ui.buttonBox.accepted.connect(self.accept)

    def fillTableData(self):
        table = self.ui.tableCombox.currentText()
        # Get the data from the database directly, usually this will be the same with the data in the main window
        # But this is to ensure that the data is up to date
        data = db.getWorksheets(DATABASE_PATH) if table == 'Worksheet' else db.getRecords(DATABASE_PATH) 
        #Dumb Me! The database is empty!
        self.ui.rowCombox.clear()
        self.ui.rowCombox.addItems(map(lambda x: str(x+1), range(len(data))))

        if len(data) == 0:
            self.ui.rowCombox.addItem('No data')
            return
        
        # Fill the table with database's data
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(len(data[0]))
        self.ui.tableWidget.setHorizontalHeaderLabels(['ID', 'Name', 'Description', 'Upload Date', 'Last Update Date', 'Subject', 'Form'] if table == 'Worksheet' else ['ID', 'WorksheetID', 'Use Date', 'Class', 'Teacher'])
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))
        self.ui.tableWidget.resizeColumnsToContents()

    def removeEntry(self):
        """
        Remove the entry from the database.
        The entry is removed based on the selected table and row.
        """
        table = self.ui.tableCombox.currentText()
        row = self.ui.rowCombox.currentText()

        if table == 'Worksheet':
            db.removeWorksheet(DATABASE_PATH, row)
            db.removeWorksheetPath(DATABASE_PATH, row)
        elif table == 'Record':
            db.removeRecord(DATABASE_PATH, row)

        self.accept()


def exportToCSV():
    """
    Export the database to a csv file.
    The csv file is stored in the same directory with the exe with name by the current date and time.

    Returns:
        None
    """
    currentTime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    fileNames = [f'{currentTime}_worksheets.csv', f'{currentTime}_records.csv', f'{currentTime}_paths.csv']
    with open(fileNames[0], 'w', encoding='utf-8') as file:
        file.write('Worksheet ID, Name, Description, Upload Date, Last Update Date, Subject, Form\n')
        for worksheet in db.getWorksheets(DATABASE_PATH):
            file.write(','.join(map(str, worksheet)) + '\n')

    with open(fileNames[1], 'w', encoding='utf-8') as file:
        file.write('Record ID, Worksheet ID, Use Date, Class, Teacher\n')
        for record in db.getRecords(DATABASE_PATH):
            file.write(','.join(map(str, record)) + '\n')

    with open(fileNames[2], 'w', encoding='utf-8') as file:
        file.write('Path ID, Worksheet ID, File Path\n')
        for path in db.getWorksheetPaths(DATABASE_PATH):
            file.write(','.join(map(str, path)) + '\n')

def managementGUI():
    """
    The graphical management ui for the server.

    Returns:
        None
    """
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    window = ManagementUI()
    window.raise_()
    window.show()
    app.exec()

def initialize_sockets(LOCAL_IP, SOCKETS):
    # Initializing UDP sockets
    SOCKETS['socket_udp'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCKETS['socket_udp'].setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    SOCKETS['socket_udp'].bind((LOCAL_IP, SOCKETS['udp']))

    # Initializing TCP sockets
    SOCKETS['socket_tcp'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKETS['socket_tcp'].bind((LOCAL_IP, SOCKETS['tcp']))

if __name__ == '__main__':
    # Parse the command line arguments
    argparse.ArgumentParser(description='ELERP Server')
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--development', action='store_true', help='Run the server in development mode')
    parser.add_argument('-v', '--version', action='version', version=SERVER_VERSION)

    args = parser.parse_args()

    if args.development:
        logger.info("Running in development mode")
        logHandler.setLevel(logging.DEBUG)
        SOCKETS['udp'] = DEVELOPMENT_UDP_PORT
        SOCKETS['tcp'] = DEVELOPMENT_TCP_PORT
    else:
        logger.info("Running in production mode") 

    initialize_sockets(LOCAL_IP, SOCKETS)

    broadcastListenerThread = createUDPThread(SOCKETS['udp'], udpService, stop)
    broadcastListenerThread.start()
    logger.info(f'UDP boardcast listener started at {LOCAL_IP}:{SOCKETS['udp']}')

    dedicatedListenerThread = createTCPThread(SOCKETS['tcp'], tcpService, stop)
    dedicatedListenerThread.start()
    logger.info(f'TCP listener started at {LOCAL_IP}:{SOCKETS['tcp']}')

    # Load resources
    progRes = json.loads(open(RESOURCES_PATH + 'data.json', 'r',encoding='utf-8').read())
    logger.info(f'Resource {RESOURCES_PATH + 'data.json'} loaded')

    while not stop.is_set():
        print('\n\nELERP Server management console')
        print('quit/exit --- Quit')
        print('list --- List all clients')
        print('message --- Show message')
        print('reset --- Reset database')
        print('version --- Show server version')
        print('gui --- Database management tools')
        print('csv --- Export database to csv')
        print('sql --- Run SQL command')
        command = input('Enter command: ')
        if command == 'quit' or command == 'exit':
            stop.set()
            print('Stopping server... Please wait')
        elif command == 'list':
            print(addressbook)
        elif command == 'message':
            print(progRes)
        elif command == 'reset':
            db.resetDatabaseToDefault(DATABASE_PATH)
        elif command == 'r_record':
            db.resetRecordsTable(DATABASE_PATH)
        elif command == 'version':
            print(SERVER_VERSION)
        elif command == 'gui':
            print('Working in progress')
            managementGUI()
        elif command == 'csv':
            exportToCSV()
        elif command == 'sql':
            try:
                db.runSQLCommand(DATABASE_PATH, input('Enter SQL command: '))
            except Exception as e:
                print(e)

    print('Stopping broadcast listener thread...')
    broadcastListenerThread.join()
    print('Stopping dedicated listener thread...')
    dedicatedListenerThread.join()
    sys.exit(0)