import json
import socket, threading
from src.protocol import REQUEST, ExecutorScope, ProtocolExecutor, ProtocolHandler, RESPONSE, STATUS
from src.helper import sendMessage, recvMessage
import database as db

import base64
import traceback
import os
import logging, colorlog

LOCAL_IP = socket.gethostbyname(socket.gethostname())
UDP_PORT = 19864
TCP_PORT = 19865

SERVER_SOCKET_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_SOCKET_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
SERVER_SOCKET_UDP.bind((LOCAL_IP, UDP_PORT))

SERVER_SOCKET_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_SOCKET_TCP.bind((LOCAL_IP, TCP_PORT))

SERVER_VERSION = '1.0.2'

# Resources Path
RESOURCES_PATH = 'res/'

# Database Path
DATABASE_PATH = 'data/database.db'

# Worksheet Path
WORKSHEET_PATH = 'data/worksheets/'

# Setup logging module
logger = logging.getLogger('elerpServer')
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", 
    log_colors={ 'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red', }
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

handler = ProtocolHandler()

addressbook = {}

stop = False

progRes = None

database_metadata = {
    'count': db.getWorksheetsCount(DATABASE_PATH)   # Only update when there are changes on the database
}

def udpService():
    """
    UDP service to listen for boardcast messages from clients and announce the ip to them.

    This function should be run as a deamon thread to keep listening for boardcast messages.

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
        SERVER_SOCKET_UDP.sendto(message.encode(), addr)

    SERVER_SOCKET_UDP.settimeout(3)
    while not stop:
        try:
            conn, addr = SERVER_SOCKET_UDP.recvfrom(4096)
            logger.info(f'Connected by {addr} via UDP boardcast')   # Log the connection
            # Send the server ip to the client
            data = handler.deserializeMessage(conn.decode())
            executor = ProtocolExecutor(data)
            executor.addMessageHandler(sendToClient, REQUEST.POST, 'elerp_client', ExecutorScope.COMMAND)
            try:
                executor.executeHandlers()
            except ValueError as e:
                e.with_traceback()
                message = handler.prepMessage(RESPONSE.ERROR, mainMessage=STATUS.INVALID_REQUEST).serializeMessage()
                logger.warning(f'Invalid client found: {addr} with message {data}')
                SERVER_SOCKET_UDP.sendto(message.encode(), addr)

        except socket.timeout:
            continue

    SERVER_SOCKET_UDP.close()   # Stop when the program ends

def tcpService():
    """
    TCP service to listen for incoming connections from clients and handle necessary actions for the clients.

    This function should be run as a deamon thread to keep listening for incoming connections.
    
    Returns:
        None
    """
    SERVER_SOCKET_TCP.listen(5)
    SERVER_SOCKET_TCP.settimeout(3)
    while not stop:
        try:
            conn, addr = SERVER_SOCKET_TCP.accept()
            logger.info(f'Connected by {addr} via TCP')
            clientService = threading.Thread(target=clientHandler, args=(conn, addr))
            clientService.daemon = True
            clientService.start()
        except socket.timeout:
            continue
    SERVER_SOCKET_TCP.close()   # Stop when the program ends

def handelUpload(request):
    """
    Handle the upload request from the client.

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
    logger.info(f'Register usage request received from {addressbook[ip]}')
    w_id = db.getWorksheetId(DATABASE_PATH, message['worksheet'])
    path = db.getWorksheetPath(DATABASE_PATH, w_id)
    with open(path, 'rb') as file:
        fileData = file.read()
        file.close()
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=fileData).serializeMessage()
    sendMessage(conn, reply.encode())
    logger.info(f'Sending worksheet to {addressbook[ip]}')
    db.registerWorksheetUse(DATABASE_PATH, w_id, message['class'], message['teacher'])

def getTotalWorksheets(_, conn, ip):
    logger.info(f'Total worksheets request received from {addressbook[ip]}')
    reply = handler.prepMessage(RESPONSE.OK, mainMessage=database_metadata['count']).serializeMessage()
    sendMessage(conn, reply.encode())

def clientHandler(conn, addr):
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
    while not stop:
        try:
            data = recvMessage(conn) # Receive the message from the client
            if not data:
                break

            ip = addr[0]
            addressbook[ip] = socket.gethostbyaddr(ip)[0] if socket.gethostbyaddr(ip)[0] not in addressbook else addressbook[ip] # Add the client to the addressbook

            decoded = handler.deserializeMessage(data.decode())
            executor.setMessage(decoded)
            executor.executeHandlers()

        except ConnectionResetError:
            logger.warning(f'Closing connection with {addressbook[ip]}')
            conn.close()
            break
    conn.close()

if __name__ == '__main__':
    broadcastListenerThread = threading.Thread(target=udpService)
    broadcastListenerThread.daemon = True
    broadcastListenerThread.start()
    logger.info(f'UDP boardcast listener started at {LOCAL_IP}:{UDP_PORT}')

    dedicatedListenerThread = threading.Thread(target=tcpService)
    dedicatedListenerThread.daemon = True
    dedicatedListenerThread.start()
    logger.info(f'TCP listener started at {LOCAL_IP}:{TCP_PORT}')

    # Load resources
    progRes = json.loads(open(RESOURCES_PATH + 'data.json', 'r',encoding='utf-8').read())
    logger.info(f'Resource {RESOURCES_PATH + 'data.json'} loaded')

    while not stop:
        print('\n\nELERP Server management console')
        print('q --- Quit')
        print('list --- List all clients')
        print('message --- Show message')
        print('reset --- Reset database')
        print('version --- Show server version')
        print('database --- Database management tools')
        command = input('Enter command: ')
        if command == 'q':
            stop = True
        elif command == 'list':
            print(addressbook)
        elif command == 'message':
            print(progRes)
        elif command == 'reset':
            db.resetDatabaseToDefault(DATABASE_PATH)
        elif command == 'version':
            print(SERVER_VERSION)
        elif command == 'database':
            print('Working in progress')
        pass

    broadcastListenerThread.join()
    dedicatedListenerThread.join()
