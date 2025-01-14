import struct
import threading

def recvAll(sock, numBytes):
    """
    Receive a fixed number of bytes from a socket.

    Args:
        sock (socket): The socket to receive the bytes from.
        numBytes (int): The number of bytes to receive.

    Returns:
        bytearray: The bytes received.
    """
    data = bytearray()
    while len(data) < numBytes:
        phoneix = sock.recv(numBytes - len(data))
        if not phoneix:
            return None
        data.extend(phoneix)
    return data

def sendMessage(sock, message):
    """
    Send a message to the socket.

    Args:
        sock (socket): The socket to send the message to.
        message (dict): The message to send.
    """
    message = struct.pack('>I', len(message)) + message
    sock.sendall(message)

def recvMessage(sock):
    """
    Receive a message from the socket.

    Args:
        sock (socket): The socket to receive the message from.

    Returns:
        bytearray: The message received.
    """
    raw_message = recvAll(sock, 4)
    if not raw_message:
        return None
    messageLength = struct.unpack('>I', raw_message)[0]
    return recvAll(sock, messageLength)