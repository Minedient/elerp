"""
This module contains necessary functions to create a simple client-server network over a LAN using UDP and TCP protocols.
"""

import socket
import threading
import time
import sys
import os
import json


class UDPServingModule():
    """
    This class is responsible for creating a UDP server that listens for incoming messages on a specified port.
    """

    def __init__(self, port):
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('', self.port))
        self.server.settimeout(1)
        self.data = None

    def listen(self):
        """
        This method listens for incoming messages on the specified port.
        """
        try:
            self.data, _ = self.server.recvfrom(1024)
        except socket.timeout:
            pass

    def get_data(self):
        """
        This method returns the data received by the server.
        """
        return self.data

    def close(self):
        """
        This method closes the server.
        """
        self.server.close()