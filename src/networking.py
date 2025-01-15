import socket
import threading
from typing import Callable

from src.protocol import REQUEST, RESPONSE, ProtocolHandler, ProtocolData

handler = ProtocolHandler()

# Type definition for the callback function that will be executed when a UDP message is received
UDPCallback = Callable[[ProtocolData, tuple], None]
TCPCallback = Callable[[socket.socket, tuple], None]

def searchServer(serverPort, identifier, logger = None):
    """
    Search for the target server on the local network.
    It works by sending a broadcast message to the local network using UDP protocol.
    The server will respond with its IP address and port number if receive the correct .

    Args:
        serverPort (int): The port number of the server.
        identifier (str): The identifier of the server.
        logger (logging.Logger): The logger object. (default is None)

    Returns:
        tuple: The IP address of the server.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    message = handler.prepMessage(REQUEST.POST, mainCommand=identifier).serializeMessage()

    if logger:
        logger.debug(f"Sending broadcast message: {message} to {serverPort}")
    s.sendto(message.encode(), ('255.255.255.255', serverPort))

    # Wait for the server to respond
    s.settimeout(3)
    try:
        data, addr = s.recvfrom(4096)
        response = handler.deserializeMessageAsProtocolData(data.decode())
        if response.getType() != RESPONSE.OK:
            raise ValueError(f'Invalid response: {response.getType()}')
        
        if logger:
            logger.debug(f"Received response from {addr}: {response}")
            logger.info(f'Server found!')
            return addr
    except socket.timeout:
        if logger:
            logger.debug('No server found')
            return None, None
    except socket.error as e:
        if e.errno == 10054:
            if logger:
                logger.info('Connection reset by peer')
        else:
            raise
    except ValueError as e:
        if logger:
            logger.warning(f'Invalid response: {e}')
        return None, None
    s.close()

def connectToServer(serverIP, serverPort, logger = None):
    """
    Establish a TCP connection with the server.

    Args:
        server_ip (str): The ip address of the server.

    Returns:
        conn: The connection object.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect((serverIP, serverPort))
    if logger:
        logger.info(f"Connected to server {serverIP}:{serverPort}")
    return s


def createUDPThread(serverPort: int, action: UDPCallback, globalStopFlag: threading.Event, logger = None):
    """
    Create a thread that listens for UDP broadcast messages.
    The action function will be executed when a message is received.
    The action function should take two arguments: the message and the socket object.
    Args:
        serverPort (int): The port number of the server.
        action (UDPCallback): The function to be executed when a message is received.
        globalStopFlag (boolean): The flag to stop the thread.
        logger (logging.Logger): The logger object. (default is None)
    Returns:
        udpThread: The thread object that listens for UDP broadcast messages.
    """

    SERVER_UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SERVER_UDP_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    SERVER_UDP_SOCKET.bind(('', serverPort))    # will it work?
    SERVER_UDP_SOCKET.settimeout(3)

    # Wrapper function #
    def actionWrapper(stop: threading.Event):
        while not stop.is_set():
            try:
                conn, addr = SERVER_UDP_SOCKET.recvfrom(4096)
                if logger:
                    logger.info(f"Received message from {addr}: {conn} via UDP")
                action(handler.deserializeMessageAsProtocolData(conn.decode()), addr)
            except socket.timeout:
                continue
        SERVER_UDP_SOCKET.close()

    udpListenerThread = threading.Thread(target = actionWrapper, args=(globalStopFlag,))
    udpListenerThread.daemon = True
    if logger:
        logger.info(f"Starting UDP listener thread on port {serverPort}")
    return udpListenerThread


def createTCPThread(serverPort: int, action: TCPCallback, globalStopFlag: threading.Event, logger = None):
    """
    Create a thread that listens for TCP messages.
    The action function will be executed when a message is received.
    The action function should take two arguments: the message and the socket object.
    Args:
        serverPort (int): The port number of the server.
        action (Callable): The function to be executed when a message is received.
        globalStopFlag (boolean): The flag to stop the thread.
        logger (logging.Logger): The logger object. (default is None)
    Returns:
        tcpThread: The thread object that listens for TCP messages.
    """
    SERVER_TCP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_TCP_SOCKET.bind(('', serverPort))
    SERVER_TCP_SOCKET.listen(5)
    SERVER_TCP_SOCKET.settimeout(3)

    def actionWrapper(stop: threading.Event):
        while not stop.is_set():
            try:
                conn, addr = SERVER_TCP_SOCKET.accept()
                action(conn, addr)
            except socket.timeout:
                continue
        SERVER_TCP_SOCKET.close()

    tcpListenerThread = threading.Thread(target = actionWrapper, args=(globalStopFlag,))
    tcpListenerThread.daemon = True
    if logger:
        logger.info(f"Starting TCP listener thread")
    return tcpListenerThread