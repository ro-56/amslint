from amslint.messages.errorcodes import ErrorCodes


class Message():

    location: int
    path: str
    code: str

    def __init__(self, location: int, path: str, code: str):
        self.location = location
        self.path = path
        self.code = code


class MessageHandler():

    __messages: list[Message]


    def __init__(self):
        self.__messages = []


    def get_messages(self):
        return self.__messages


    def add(self, location: int, path: str, code: str):
        self.__messages.append(Message(location, path, code))
