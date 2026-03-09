from datetime import datetime
from enum import Enum


class MessageType(Enum):
    Direct = "Direct"
    Server = "Server"


user_id_counter = 1

server = None


class ServerInfo:
    def __init__(self, serverID: str, serverName: str):
        self.serverID = serverID
        self.serverName = serverName
        self.memberIDs = []


class UserInfo:
    def __init__(self, userName: str, password: str, profileImage: str, isAdmin: bool):
        global user_id_counter, server
        user_id_counter += 1
        self.userID = str(user_id_counter)
        self.userName = userName
        self.password = password
        self.profileImage = profileImage
        self.isAdmin = isAdmin

        if server is not None:
            server.memberIDs.append(self.userID)


class MessageInfo:
    def __init__(self, message: str, senderID: str, receiverID: str, serverID: str, messageType: MessageType, timestamp: datetime):
        self.message = message
        self.senderID = senderID
        self.receiverID = receiverID
        self.serverID = serverID
        self.messageType = messageType
        self.timestamp = timestamp


# Initialize the single server
server = ServerInfo(serverID="1", serverName="Harmony")
