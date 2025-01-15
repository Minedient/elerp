import json
import base64
from enum import Enum
from typing import Union

class REQUEST(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'

class RESPONSE(Enum):
    OK = 'ok'
    ERROR = 'error'

class STATUS(Enum):
    SUCCESS = 'success'
    INVALID_REQUEST = 'invalid_request'
    EMPTY_PARAMETER = 'empty_parameter'
    INVALID_PARAMETER = 'invalid_parameter'
    UPLOAD_FAILED = 'upload_failed'

class ProtocolEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, REQUEST):
            return {'__REQUEST__': obj.value}
        elif isinstance(obj, RESPONSE):
            return {'__RESPONSE__': obj.value}
        elif isinstance(obj, STATUS):
            return {'__STATUS__': obj.value}
        elif isinstance(obj, bytes):
            return base64.b64encode(obj).decode()
        return json.JSONEncoder.default(self, obj)
        
def protocolHook(data):
    """
    The hook function for the JSON parser to parse the protocol data.
    """
    if '__REQUEST__' in data:
        return REQUEST(data['__REQUEST__'])
    elif '__RESPONSE__' in data:
        return RESPONSE(data['__RESPONSE__'])
    elif '__STATUS__' in data:
        return STATUS(data['__STATUS__'])
    else:
        return data

class ProtocolData():
    """
    The protocol data object to store the data of the protocol.
    """
    def __init__(self):
        self.data = {'type': None, 'command': None, 'message': {}}

    def setType(self, type: Union[REQUEST, RESPONSE]):
        """
        Set the type of the data.

        Args:
            type [REQUEST or RESPONSE]: The type of the data.
        """
        self.data['type'] = type

    def getType(self):
        """
        Get the type of the data.

        Returns:
            REQUEST or RESPONSE: The type of the data.
        """
        return self.data['type']

    def getWhole(self):
        """
        Get the whole data.

        Returns:
            dict: The whole data.
        """
        return self.data

    def getCommand(self):
        """
        Get the command of the data.

        Returns:
            str: The command of the data.
        """
        return self.data['command']

    def setCommand(self, command):
        """
        Set the command of the data.

        Args:
            command: The command to set.
        """
        self.data['command'] = command

    def getAttribute(self, key):
        """
        Get the attribute of the data.

        Args:
            key: The key of the attribute to get.

        Returns:
            Any: The value of the attribute.
        """
        return self.data['message'][key]

    def setAttribute(self, key, value):
        """
        Set the attribute of the data.

        Args:
            key: The key of the attribute to set.

            value: The value of the attribute to set.
        """
        self.data['message'][key] = value

    def setMessage(self, message):
        """
        Set the message of the data.

        Args:
            message: The message to set.
        """
        self.data['message'] = message

    def getMessage(self): 
        """
        Get the message of the data.

        Returns:
            dict: The message of the data.
        """
        return self.data['message']

    def reset(self):
        """
        Reset the data.
        """
        self.data = {'type': None, 'command': None, 'message': {}}


class ProtocolHandler():
    """
    The protocol handler for elerp network communication.
    """
    def __init__(self):
        self.data = {}
        pass
    
    def prepMessage(self, responseObj: Union[REQUEST, RESPONSE], mainCommand:str = None, mainMessage = {}):
        """
        Prepare the message to be sent over the elerp network.

        Args:
            responseObj (Request or Response): The reponseObj of the message.
            mainCommand (str): The command of the message. The command is used to identify the action to be performed.
            mainMessage (dict): The main message of the response.
        Returns:
            self: The handler object itself for chaining.
        """
        self.data['type'] = responseObj
        self.data['command'] = mainCommand
        self.data['message'] = mainMessage
        return self
    
    def addAttribute(self, key, value):
        """
        Add attributes to the message's body, this is used to add additional information in the message.

        Args:
            key (str): The key of the attribute to be added.
            value: The value of the attribute to be added.

        Returns:
            self: The handler object itself for chaining.
        """
        self.data['message'][key] = value
        return self
    
    def serializeMessage(self):
        """
        Serialize the message to JSON format, and reset the message

        Returns:
            str: The serialized message.
        """
        final = self.data
        self.data = {}
        return json.dumps(final, cls=ProtocolEncoder, ensure_ascii=False)
    
    def deserializeMessage(self, message):
        """
        Deserialize the message from JSON format.

        Args:
            message (str): The message to be deserialized.

        Returns:
            dict: The deserialized message.
        """

        # First, parse the string to JSON (Python dict) first
        message = json.loads(message, object_hook=protocolHook)
        return self.recursiveJSONParser(message)                                   # Then perform the recursive parsing and return the parsed data
    
    def deserializeMessageAsProtocolData(self, message: str) -> ProtocolData:
        """
        Deserialize the message from JSON format and return it as a ProtocolData object.

        Args:
            message (str): The message to be deserialized.
        
        Returns:
            data (ProtocolData): The deserialized message as a ProtocolData object.
        """
        raw = self.deserializeMessage(message)
        data = ProtocolData()
        data.setType(raw['type'])
        data.setCommand(raw['command'])
        data.setMessage(raw['message'])
        return data

    def recursiveJSONParser(self, data):
        """
        Recursively parse the JSON data to extract the values.

        Args:
            data (dict): The data to be parsed.

        Returns:
            dict: The data extracted from the response.
        """
        for key in data:
            try:
                if isinstance(data[key], str):
                    data[key] = json.loads(data[key], object_hook=protocolHook)
                elif isinstance(data[key], list):
                    for i in range(len(data[key])):
                        if isinstance(data[key][i], str):
                            data[key][i] = self.recursiveJSONParser(data[key][i])
                elif isinstance(data[key], dict):
                    data[key] = self.recursiveJSONParser(data[key])
            except:
                pass
        return data
    
class ExecutorScope(Enum):
    COMMAND = 'command'
    MESSAGE = 'message'
    WHOLE = 'whole'
    RESPONSE = 'response'
    
class ProtocolExecutor():

    def __init__(self, message: Union[ProtocolData, dict] =None ):
        self.message = message

    def setMessage(self, message):
        """
        Set the message to be executed.

        Args:
            message (dict): The message
        """
        self.message = message

    def getMessageTuple(self):
        """
        Get the message type and command tuple.

        Returns:
            tuple: The message type and command tuple.
        """
        if type(self.message) is ProtocolData:
            return (self.message.getType(), self.message.getCommand())
        else:
            return (self.message['type'], self.message['command'])

    def checkHandlers(self):
        """
        Check if the handlers attribute is available in the object.

        Returns:
            handlers: The handlers attribute of the object.
        """
        return self.handlers

    def addMessageHandler(self, action, requestType: Union[REQUEST, RESPONSE] = REQUEST.GET, requestCommand = None, scope: ExecutorScope = ExecutorScope.MESSAGE):
        """
        Register a custom action for a specific request or reponse type.

        Args:
            action (callable): The action to execute when the request type matches.
            requestType (REQUEST or RESPONSE): The request type to match.
            requestCommand (str): The request command to match.
            scope (ExecutorScope): The scope of the message to be passed to the action.
        """
        if not hasattr(self, 'handlers'):
            self.handlers = {}
        self.handlers[(requestType, requestCommand)] = (action, scope)

    def setDefaultHandler(self, action):
        """
        Set the default handler for the executor.
        This handler will be executed when no handler is registered for the request type.
        If no default handler is set, an error will be raised when no handler is registered for the request type.

        Args:
            scope (ExecutorScope): The scope of the message to be passed to the action.
            action (callable): The action to execute when the request type matches.
        """
        self.defaultHandler = action

    def executeHandlers(self, **kwargs):
        """
        Execute the registered action based on the message's request or response type.
        """
        request_tuple = self.getMessageTuple()
        if request_tuple in self.handlers:
            scope = self.handlers[request_tuple][1]
            action = self.handlers[request_tuple][0]
            if scope == ExecutorScope.MESSAGE:
                return action(self.message.getMessage(), **kwargs)
            elif scope == ExecutorScope.WHOLE:
                return action(self.message, **kwargs)
            elif scope == ExecutorScope.COMMAND:
                return action(self.message.getCommand(), **kwargs)
            elif scope == ExecutorScope.RESPONSE:
                return action(self.message.getType(), **kwargs)
        else:
            if not self.defaultHandler:
                raise ValueError(f"No handler registered for {request_tuple}")
            return self.defaultHandler(self.message, **kwargs)

            
        
                                            