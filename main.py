import base64
from datetime import datetime
import ui.mainUI_ui as mainUI
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog, QFileDialog, QListWidget, QListWidgetItem, QTableWidgetItem, QDialogButtonBox, QButtonGroup
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon
import os
import sys
import logging, colorlog
from ui.uploadWizard_ui import Ui_Dialog as UploadWizardDialog
from ui.registerWizard_ui import Ui_Dialog as RegisterWizardDialog
from src.helper import recvMessage, sendMessage
from src.protocol import STATUS, ExecutorScope, ProtocolHandler, REQUEST, RESPONSE
import time
import configparser
from src.networking import searchServer, connectToServer
import argparse

TIER = ['F1','F2','F3','F4','F5','F6','J','S','A']

# Setup the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", 
    log_colors={ 'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red', }
) 
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Load the configuration file
config = configparser.ConfigParser()
handler = ProtocolHandler()

downloadFolderPath = ''

subjects = None
forms = None
classes = None

CLIENT_VERSION = '1.0.7'
SERVER_UDP_PORT = 19864
SERVER_TCP_PORT = 19865
D_SERVER_UDP_PORT = 19866
D_SERVER_TCP_PORT = 19867

def exceptionHook(exctype, value, traceback):
    logger.error(f'Uncaught exception: {exctype}, {value}, {traceback}')
    logger.info("Saving log to 'error.log'")
    with open('error.log', 'a') as f:
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{time}: Uncaught exception: {exctype}, {value}, {traceback}\n')
    sys.__excepthook__(exctype, value, traceback)

# Hook for excpetion
sys.excepthook = exceptionHook

def sendRequest(conn, request, scope=ExecutorScope.MESSAGE):
    """
    Send a request to the server and wait for replies.

    Args:
        conn: The connection object.
        request (str): The request message.
        scope (ExecutorScope): The scope of the of the reply message.
    Returns:
        ProtocolData: The response message.
    """
    sendMessage(conn, request.encode())
    obj = handler.deserializeMessageAsProtocolData(recvMessage(conn).decode())
    if scope == ExecutorScope.MESSAGE:
        return obj.getMessage()
    elif scope == ExecutorScope.RESPONSE:
        return obj.getType()
    elif scope == ExecutorScope.COMMAND:
        return obj.getCommand()
    elif scope == ExecutorScope.WHOLE:
        return obj
    else:
        raise ValueError(f'Invalid scope: {scope}')

def testConnection(conn):
    """
    Ask the server for a test connection.

    Args:
        conn: The connection object.
    """
    request = handler.prepMessage(REQUEST.GET, mainCommand='testConnection').serializeMessage()
    respond = sendRequest(conn, request, scope=ExecutorScope.RESPONSE)
    if respond == RESPONSE.OK:
        logger.info('Connection test successful')
    else:
        logger.error('Connection test failed')

def versionCompare(client: str, server: str) -> int:
    """
    Compare the client version with the server version.

    Args:
        client (str): The client version.
        server (str): The server version.

    Returns:
        int: 0 if the versions are the same, 1 if the server version is newer than the client, but it is compatible, 2 if the server version is newer than the client, but it is not compatible.
    """
    clientNum = [int(i) for i in client.split('.')]
    serverNum = [int(i) for i in server.split('.')]
    # The first number is the major version, the second number is the minor version, the third number is the patch version
    # Due to the nature of the versioning system, the server version should always be greater than the client version,
    for c, s in zip(clientNum, serverNum):
        if s > c:
            return 1 if serverNum[0] == clientNum[0] else 2
        elif s < c:
            return 0
    return 0

def checkUpdate(conn):
    """
    Compare the client version with the server version.
    If the server version is newer, return True, otherwise False.

    Args:
        conn: The connection object.
    """
    request = handler.prepMessage(REQUEST.GET, mainCommand='checkVersion').serializeMessage()
    respond = sendRequest(conn, request, scope=ExecutorScope.MESSAGE)
    result = versionCompare(CLIENT_VERSION, respond)
    if result == 1:
        QMessageBox.information(None, 'Update', 'A new update is available, please update the program to the latest version.')
    elif result == 2:
        QMessageBox.critical(None, 'Error', 'The server version is not compatible with the client version, please update the program to the latest version.')
    else:
        logger.info('Client version is up to date')


def getGlobalData(conn):
    global subjects, forms, classes
    request = handler.prepMessage(REQUEST.GET, mainCommand='globalData').serializeMessage()
    response = sendRequest(conn, request)
    subjects = response['subjects'] # Extract the data
    forms = response['forms']
    classes = response['classes']
    logger.info('Global data received')

def checkFileNameConvention(name):
    """
    Check if the file name convention is correct.
    A correct name convention of the system consist for the following part
    1. Tier, which is either single letter like J, S, A or F1, F2, F3, F4, F5, F6
    2. Subject name, which is a single word, and it should be the same used in school
    3. Serial number, which is a number that is unqiue for the given tier and subject
    4. Title/Subject/Description of the file, which is a single word or a sentence seperated by underscore

    A correct file name should be in the format of:
    Tier_Subject_Serial_Title.extension (pdf, docx, zip, 7z etc.)

    You can see from above format, they are seperated by underscore.

    Args:
        name (str): The name of the file.

    Returns:
        bool: True if the name is correct, False otherwise.
    """
    #return True
    arr = name.split('_')
    if len(arr) < 4:
        return False
    if arr[0] not in TIER:
        return False
    if not arr[2].isdigit():
        return False
    return True

class ProgramLogHandler(logging.Handler):
    """
    A handler class that sends all log records to a QTextBrowser widget.
    """
    def __init__(self, browser):
        logging.Handler.__init__(self)
        self.browser = browser

    def emit(self, record):
        msg = self.format(record)
        self.browser.append(msg)

class UploadWizard(QDialog):
    def __init__(self):
        super(UploadWizard, self).__init__()
        self.ui = UploadWizardDialog()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        # Setup the comboboxes
        self.ui.subjectsComboBox.clear()
        self.ui.formComboBox.clear()
        self.ui.subjectsComboBox.addItems([f"{subject['name']}/{subject['cname']}" for subject in subjects])
        self.ui.formComboBox.addItems([f"{form['name']}/{form['cname']}" for form in forms])

        self.ui.filesSelectorButton.clicked.connect(self.on_filesSelectorButton_clicked)
        self.ui.fileListWidget.setDragDropMode(QListWidget.InternalMove)
        self.ui.resetButton.clicked.connect(self.on_resetButton_clicked)

    def addItemToList(self, actualItem):
        """
        Add an item to the list widget.

        Args:
            actualItem (str): The actual item to be added.
            displayItem (str): The item to be displayed.
        """
        item = QListWidgetItem()
        item.setData(Qt.DisplayRole, os.path.basename(actualItem))
        item.setData(Qt.UserRole, actualItem)
        self.ui.fileListWidget.addItem(item)
    
    def addItemsToList(self, items):
        for item in items:
            self.addItemToList(item)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        self.addItemsToList(url.toLocalFile() for url in urls)

    def exec(self):
        """
        Setup the comboboxes with the subjects information provided by server.
        """
        # Stupid, but it works for now
        self.ui.fileListWidget.clear()
        super(UploadWizard, self).exec()

    def accept(self):
        # Check the file name convention     
        num = self.ui.fileListWidget.count()
        if num == 0:
            logger.info('No files selected')
            return 

        for i in range(num):
            name = os.path.basename(self.ui.fileListWidget.item(i).data(Qt.UserRole))
            if not checkFileNameConvention(name):
                QMessageBox.critical(None, 'Error', f'Invalid file name convention: {name}\nPlease follow the correct file name convention\nYou can find the file naming convention in the help menu')
                return
        logger.info('Upload wizard input accepted')

        # Send the files to the server
        for i in range(num):
            file = self.ui.fileListWidget.item(i).data(Qt.UserRole)
            with open(file, 'rb') as f:
                data = f.read()
                createDate = datetime.strptime(time.ctime(os.path.getctime(file)), '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
                request = handler.prepMessage(REQUEST.POST, mainCommand='uploadWorksheet') \
                    .addAttribute('fileData', data) \
                    .addAttribute('form', self.ui.formComboBox.currentIndex()) \
                    .addAttribute('subject', self.ui.subjectsComboBox.currentIndex()) \
                    .addAttribute('name', os.path.basename(file)) \
                    .addAttribute('description', self.ui.textEdit.toPlainText()) \
                    .addAttribute('creationDate', createDate) \
                    .serializeMessage()
                response = sendRequest(conn, request) # This should return OK
                
                if response == STATUS.SUCCESS:
                    logger.info(f'File {file} uploaded successfully')
                else:
                    logger.error(f'Error uploading file {file} with error code: {response}')    
                f.close()

        super(UploadWizard, self).accept()

    def reject(self):
        super(UploadWizard, self).reject()
        logger.info('Upload wizard input rejected')

    def on_filesSelectorButton_clicked(self):
        """
        Slot function for the select file button.
        """
        files, _ = QFileDialog.getOpenFileNames(self, 'Select files')
        self.addItemsToList(files)
        # logger.info(f'Files selected: {files}')

    def on_resetButton_clicked(self):
        """
        Slot function for the reset button.
        """
        self.ui.fileListWidget.clear()
        logger.info('File list cleared')

class RegisterWizard(QDialog):
    def __init__(self):
        super(RegisterWizard, self).__init__()
        self.ui = RegisterWizardDialog()
        self.ui.setupUi(self)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setEnabled(True)

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(classes)
        self.ui.nameEdit.setText(config.get('SETTING', 'Teacher Name'))

        self.ui.tableWidget.cellClicked.connect(self.on_tableWidget_cellClicked)
        self.ui.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)

    def on_tableWidget_cellClicked(self, row, column):
        """
        Slot function for the table widget cell clicked event.

        Args:
            row (int): The row index.
            column (int): The column index.
        """
        item = self.ui.tableWidget.item(row, 0)
        self.ui.worksheetEdit.setText(item.text())

    def on_comboBox_currentIndexChanged(self, index):
        """
        Slot function for the combobox current index changed event.

        Args:
            index (int): The index of the combobox.
        """
        # Ask the server for the list of unused worksheets
        request = handler.prepMessage(REQUEST.GET, mainCommand='unusedWorksheets').addAttribute('class', self.ui.comboBox.currentText()).serializeMessage()
        reponse = sendRequest(conn, request)

        # Add the data to the table
        self.ui.tableWidget.setRowCount(len(reponse))
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Name', 'Description', 'Subject', 'Form'])
        for i, item in enumerate(reponse):
            for j, cell in enumerate(item):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(cell))
        # Edit the size of the columns that fit the content
        self.ui.tableWidget.resizeColumnsToContents()

    def exec(self):
        """
        Setup the comboboxes with the classes information provided by server.
        """
        
        # Ask the server for the list of unused worksheets
        request = handler.prepMessage(REQUEST.GET, mainCommand='unusedWorksheets').addAttribute('class', self.ui.comboBox.currentText()).serializeMessage()
        reponse = sendRequest(conn, request)

        # Add the data to the table
        self.ui.tableWidget.setRowCount(len(reponse))
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Name', 'Description', 'Subject', 'Form'])
        for i, item in enumerate(reponse):
            for j, cell in enumerate(item):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(cell))
        # Edit the size of the columns that fit the content
        self.ui.tableWidget.resizeColumnsToContents()
        if len(reponse) > 0:
            self.ui.tableWidget.selectRow(0)
            self.ui.worksheetEdit.setText(self.ui.tableWidget.item(0, 0).text())

        super(RegisterWizard, self).exec()

    def reject(self):
        super(RegisterWizard, self).reject()
        logger.info('Register wizard input rejected')

    def accept(self):
        # Check if the user has enter the name
        if self.ui.nameEdit.text() == '':
            QMessageBox.critical(None, 'Error', 'Please enter your name')
            return
        if self.ui.worksheetEdit.text() == '':
            QMessageBox.critical(None, 'Error', 'Please select a worksheet')
            return
        
        # Save the teacher name to the configuration file
        config.set('SETTING', 'Teacher Name', self.ui.nameEdit.text())
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        # Send the registration to the server
        request = handler.prepMessage(REQUEST.POST, mainCommand='registerUsage') \
            .addAttribute('class', self.ui.comboBox.currentText()) \
            .addAttribute('teacher', self.ui.nameEdit.text()) \
            .addAttribute('worksheet', self.ui.worksheetEdit.text()) \
            .serializeMessage()
        try:
            response = sendRequest(conn, request)  # This should return OK
            try:
                print(os.path.join(downloadFolderPath, self.ui.worksheetEdit.text()))
                with open(os.path.join(downloadFolderPath, self.ui.worksheetEdit.text()), 'wb') as f:   # join the save path with the file name
                    f.write(base64.b64decode(response))
                    f.close()
                    logger.info(f'Worksheet {self.ui.worksheetEdit.text()} saved successfully')
                    QMessageBox.information(None, 'Success', f'Worksheet {self.ui.worksheetEdit.text()} saved successfully to {os.getcwd()}')
            except Exception as e:
                logger.error(f'Error saving worksheet: {e}')
                QMessageBox.critical(None, 'Error', f'Error saving worksheet: {e}')
        except Exception as e:
            logger.error(f'Error happened during transition: {e}, exiting...')
            QMessageBox.critical(None, 'Error', f'Error happened during transition: {e}, exiting...')
        super(RegisterWizard, self).accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainUI.Ui_mainWindow()
        self.ui.setupUi(self)
        # Set the window icon
        self.setWindowIcon(QIcon('icon.ico'))

        # Setup logging function of the program
        pLogHandler = ProgramLogHandler(self.ui.logBrowser)
        logger.addHandler(pLogHandler)

        # Create button group for the download location buttons
        self.ui.downloadLocationButtonGroup = QButtonGroup()
        self.ui.downloadLocationButtonGroup.addButton(self.ui.nextToProgramButton)
        self.ui.downloadLocationButtonGroup.addButton(self.ui.downloadsFolderButton)
        self.ui.downloadLocationButtonGroup.buttonClicked.connect(self.on_downloadLocationButtonGroup_buttonClicked)
        self.ui.downloadLocationButtonGroup.setExclusive(True)
        self.ui.nextToProgramButton.setChecked(config.getint('SETTING', 'Store Location') == 1)
        self.ui.downloadsFolderButton.setChecked(config.getint('SETTING', 'Store Location') != 1)

        # Update the recent usage table
        self.updateRecentUsageTable(conn)
        self.updateRecentUploadedTable(conn)

        # Setup the buttons
        uploadWizard = UploadWizard()
        self.ui.uploadWidgetButton.clicked.connect(lambda: uploadWizard.exec())
        uploadWizard.accepted.connect(lambda: self.updateRecentUploadedTable(conn)) # Update the recent uploaded table after the upload is done or failed
        uploadWizard.rejected.connect(lambda: self.updateRecentUploadedTable(conn))

        registerWizard = RegisterWizard()
        self.ui.registerWidgetButton.clicked.connect(lambda: registerWizard.exec())
        registerWizard.accepted.connect(lambda: self.updateRecentUsageTable(conn))  # Update the recent usage table after the registration is done or failed
        registerWizard.rejected.connect(lambda: self.updateRecentUsageTable(conn))  

        self.ui.actionAbout_The_App.triggered.connect(lambda: QMessageBox.about(None, 'About', 'This is a simple application that allows teachers to upload worksheets and register usage of worksheets.'))
        self.ui.actionFile_Naming_Convention.triggered.connect(lambda: QMessageBox.about(None, 'File Naming Convention', 'The file naming convention of the system is as follows:\nTier_Subject_Serial_Title.extension\n\nTier: F1, F2, F3, F4, F5, F6, J, S, A\nSubject: The subject name\nSerial: A number that is unique for the given tier and subject\nTitle: The title of the file\n\nAn example of a correct file name is: F1_Math_1_Addition.pdf'))

        # Setup a timer to update the total worksheet count every minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateWorksheetCount)
        self.timer.start(60000)  # 60000 milliseconds = 1 minute
        self.updateWorksheetCount() # Update the total worksheet count

    def updateWorksheetCount(self):
        """
        Update the total worksheet count.
        """
        request = handler.prepMessage(REQUEST.GET, mainCommand='totalWorksheets').serializeMessage()
        response = sendRequest(conn, request)
        self.ui.worksheetCountLabel.setText(f'Total worksheets: {response}')

    def on_downloadLocationButtonGroup_buttonClicked(self, button):
        """
        Slot function for the download location button group.

        Args:
            button (QRadioButton): The button that is clicked.
        """
        if button == self.ui.nextToProgramButton:
            downloadFolderPath = os.path.dirname(os.path.abspath(__file__))
            config.set('SETTING', 'Store Location', '1')
        elif button == self.ui.downloadsFolderButton:
            downloadFolderPath = os.path.join(os.path.expanduser('~'), 'Downloads')
            config.set('SETTING', 'Store Location', '2')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        
        logger.info(f'Download location set to: {downloadFolderPath}')

    def updateRecentUsageTable(self, conn):
        """
        Update the recent usage table with the most recent usage.
        """
        request = handler.prepMessage(REQUEST.GET, mainCommand='recentUsage').serializeMessage()
        response = sendRequest(conn, request)
        for i, item in enumerate(response):
            for j, cell in enumerate(item):
                self.ui.recentUsageTable.setItem(i, j, QTableWidgetItem(cell))
        self.ui.recentUsageTable.resizeColumnsToContents()

    def updateRecentUploadedTable(self, conn):
        """
        Update the recent uploaded table with the most recent uploaded files.
        """
        request = handler.prepMessage(REQUEST.GET, mainCommand='recentUploaded').serializeMessage()
        response = sendRequest(conn, request)
        for i, item in enumerate(response):
            for j, cell in enumerate(item):
                self.ui.recentUploadedTable.setItem(i, j, QTableWidgetItem(cell))
        self.ui.recentUploadedTable.resizeColumnsToContents()

class UpdateMessageBox(QMessageBox):
    def __init__(self):
        super(UpdateMessageBox, self).__init__()
        self.setWindowTitle('Update')
        self.setText('A new update is available, please update the program to the latest version.')
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)

    def accept (self):
        """
        Slot function for the accept button.
        """
        self.done(QMessageBox.Yes)
    
    def reject(self):
        """
        Slot function for the reject button.
        """
        self.done(QMessageBox.No)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ELERP Client')
    parser.add_argument('-d', '--development', action='store_true', help='Use development server')
    args = parser.parse_args()

    udpPort = D_SERVER_UDP_PORT if args.development else SERVER_UDP_PORT
    tcpPort = D_SERVER_TCP_PORT if args.development else SERVER_TCP_PORT

    app = QApplication(sys.argv)

    # Load configuration, if it is empty, create a new file
    config_file = 'config.ini'
    if not os.path.exists(config_file):
        config['SETTING'] = {'Teacher Name': '', 'Store Location': '2'}
    else:
        config.read(config_file)
        if not config.has_option('SETTING', 'Store Location'):
            config['SETTING']['Store Location'] = '2'
    
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    downloadFolderPath = os.path.dirname(os.path.abspath(__file__)) if config.getint('SETTING', 'Store Location') == 1 else os.path.join(os.path.expanduser('~'), 'Downloads')

    # Attempt to find the server and collect necessary information
    addr = searchServer(udpPort, 'elerp_client', logger)
    if not addr[0] and addr[1]:
        QMessageBox.critical(None, 'Error', 'No server found')
        sys.exit(1)

    # Create a QMessageBox that disappear after loading all the data from the server
    box = QMessageBox()
    box.setWindowTitle('Loading')
    box.setInformativeText('Please wait...')
    box.setText('Loading data from server...')
    box.setStandardButtons(QMessageBox.NoButton)
    box.accepted.connect(box.close)
    box.show()

    conn = connectToServer(addr[0], tcpPort, logger)
    testConnection(conn)    # Test the connection, should return OK
    checkUpdate(conn)       # Check for update
    getGlobalData(conn)     # Get the global data

    window = MainWindow()
    box.accept()    # Close the loading box
    window.show()

    sys.exit(app.exec())