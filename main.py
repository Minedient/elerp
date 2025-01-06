import base64
from datetime import datetime
import ui.mainUI_ui as mainUI
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog, QFileDialog, QListWidget, QListWidgetItem, QTableWidgetItem, QDialogButtonBox, QButtonGroup
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon
import os
import sys
import socket
import logging, colorlog
from ui.uploadWizard_ui import Ui_Dialog as UploadWizardDialog
from ui.registerWizard_ui import Ui_Dialog as RegisterWizardDialog
from src.helper import recvMessage, sendMessage
from src.protocol import STATUS, ExecutorScope, ProtocolHandler, REQUEST, RESPONSE
import time
import configparser

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

CLIENT_VERSION = '1.0.2'

def exceptionHook(exctype, value, traceback):
    logger.error(f'Uncaught exception: {exctype}, {value}, {traceback}')
    logger.info("Saving log to 'error.log'")
    with open('error.log', 'a') as f:
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{time}: Uncaught exception: {exctype}, {value}, {traceback}\n')
    sys.__excepthook__(exctype, value, traceback)

# Hook for excpetion
sys.excepthook = exceptionHook

# Using local network boardcast to find the server
def searchServer():
    """
    Send a boardcast message to all devices in local network and find the server.

    Returns:
        server_ip: The ip address of the server.
    """
    boardcast_ip = '255.255.255.255'
    port = 19864

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # New message
    message = handler.prepMessage(REQUEST.POST, mainCommand='elerp_client').serializeMessage()

    logger.debug(f'Sending boardcast message: {message}')
    s.sendto(message.encode(), (boardcast_ip, port))

    # Receive the server ip
    s.settimeout(2)
    try:
        data, addr = s.recvfrom(4096)
        response = handler.deserializeMessageAsProtocolData(data.decode())
        if response.getType() != RESPONSE.OK:
            raise ValueError(f'Invalid response: {response.getType()}')

        logger.debug(f'Received server ip: {addr}')
        logger.info(f'Server found!')
        return addr
    except socket.timeout:
        logger.debug('No server found')
        return None, None
    except socket.error as e:
        if e.errno == 10054:
            logger.info('Connection reset by peer')
        else:
            raise
    except ValueError as e:
        logger.error(f'Invalid message: {e}')
        return None, None
    s.close()

def establishConnection(server_ip):
    """
    Establish a TCP connection with the server.

    Args:
        server_ip (str): The ip address of the server.

    Returns:
        conn: The connection object.
    """
    port = 19865
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((server_ip, port))
    return s

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

def getGlobalData(conn):
    global subjects, forms, classes
    request = handler.prepMessage(REQUEST.GET, mainCommand='globalData').serializeMessage()
    response = sendRequest(conn, request)
    subjects = response['subjects'] # Extract the data
    forms = response['forms']
    classes = response['classes']
    logger.info(f'Received subjects information')
    logger.info(f'Received forms information')
    logger.info(f'Received classes information')

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
                QMessageBox.critical(None, 'Error', f'Invalid file name convention: {name}')
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
    addr = searchServer()
    if not addr[0] and addr[1]:
        QMessageBox.critical(None, 'Error', 'No server found')
        sys.exit(1)
    conn = establishConnection(addr[0])
    testConnection(conn)    # Test the connection, should return OK
    getGlobalData(conn)     # Get the global data

    # Check for updates
    request = handler.prepMessage(REQUEST.GET, mainCommand='checkVersion').serializeMessage()
    response = sendRequest(conn, request)
    if response > CLIENT_VERSION:
        updateBox = UpdateMessageBox()
        if updateBox.exec() == QMessageBox.Yes:
            # Handle the update process here
            logger.info('User chose to update the program')

        else:
            logger.info('User chose not to update the program, exiting...')
            sys.exit(0)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())