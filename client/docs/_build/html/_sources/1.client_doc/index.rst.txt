====================
Capture 'Client'
====================

Кратко
------
Клиент реализован классом Client. На стороне Клиента создается сокет.
Клиент запускается в параллельных потоках на чтение и отправку.

Объект класса Client
--------------------
Объект класса **Client** ...

Сокет
:::::
Создание сокета происходит при инициализации объекта класса **Client**:

в конструкторе::

    self.sock = socket.socket()
    self.sock.connect((self.host, self.port))

параметры *self.host* и *self.port* принимаются по умолчанию:

 * self.host == HOST
 * self.port == PORT

где *HOST* и *PORT* константы, имеют значения::

    HOST: 127.0.0.1 (localhost)
    PORT: 7777

Отправка сообщений
::::::::::::::::::
Отправка сообщений реализована методом **send_byte_request**:

*send_byte_request*::

    def send_byte_request(self, byte_data):
        try:
            self.sock.send(byte_data)
            return True
        except TypeError:
            print('Wrong data format!')
        except OSError:
            print('Disconnected!')

Прием сообщений
:::::::::::::::
Прием сообщений реализован методом **get_byte_response**:

*get_byte_response*::

    def get_byte_response(self):
        while True:
            client_authenticate(self.sock, self.__secret_key)  # *аутентификация клиента*
            byte_data = self.sock.recv(SIZE)
            if byte_data:
                self.get_byte_parse(byte_data)

метод *get_byte_parse* разбирает полученное сообщение
