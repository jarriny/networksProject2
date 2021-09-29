# Yolanda Jarrin

# !/usr/bin/python3
import socket
import sys
import ssl
import os

args = sys.argv
length = len(args)

createFile = False
sendFile = False
delete = "none"

if length == 3:
    if args[2] == "ls":
        command = "LIST"
        url = args[3]
        message = "LIST " + url + "\r\n"
    elif args[2] == "mkdir":
        command = "MKD"
        url = args[3]
        message = "MKD " + url + "\r\n"
    elif args[2] == "rm":
        command = "DELE"
        url = args[3]
        message = "DELE " + url + "\r\n"
    elif args[2] == "rmdir":
        command = "RMD"
        url = args[3]
        command = "RMD " + url + "\r\n"
    else:
        raise ValueError
elif length == 4:
    if args[2] == "cp":
        if args[3].__contains__("ftps://"):
            # remote to local
            command = "RETR"
            createFile = True
            # CREATE THE FILE ON OUR LOCAL MACHINE@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            url = args[3]
            # now have to get the username and password from the remote FILE aka url
            localFile = args[4]
            command = "RETR " + url + "\r\n"
        else:
            # local to remote
            command = "STOR"
            url = args[4]
            sendFile = True
            # now have to get the username and password from the remote FILE aka url
            localFile = args[3]
            command = "STOR " + url + "\r\n"
    if args[2] == "mv":
        if args[3].__contains__("ftps://"):
            # remote to local
            command = "RETR"
            createFile = True
            # CREATE THE FILE ON OUR LOCAL MACHINE@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ f = open("myfile.txt", "x")
            url = args[3]
            # now have to get the username and password from the remote FILE aka url
            localFile = args[4]
            command = "RETR " + url + "\r\n"
            # DELETE REMOTELY
            delete = "remote"
            command2 = "DELE " + url + "\r\n"
        else:
            # local to remote
            command = "STOR"
            url = args[4]
            # now have to get the username and password from the remote FILE aka url
            sendFile = True
            localFile = args[3]
            command = "STOR " + url + "\r\n"
            delete = "local"
            # DELETE LOCALLY@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ os.remove(localFile) but not yet
    else:
        raise ValueError
else:
    raise ValueError

# now get the username and password from the url if possible

# first 7 characters are irrelevant
urlSearch = url[7:]
x = urlSearch.find("/")
path = urlSearch[x:]
urlSearch = urlSearch[:x]
y = urlSearch.find("@")
hostAndPort = urlSearch[y+1:]
userAndPass = urlSearch[:y]
z = hostAndPort.find(":")
if z == -1:
    port = 21
    host = hostAndPort
else:
    port = hostAndPort[z+1:]
    host = hostAndPort[:z]

w = userAndPass.find(":")
if z == -1:
    password = "none"
    username = userAndPass # may or may not be ""
else:
    password = userAndPass[z+1:]
    username = userAndPass[:z] # may or may not be ""
    if username == "":
        raise ValueError

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, int(port)))
    # receiving the welcome message initially
    while True:
        Message = ""
        while not '\n' in Message:
            Message += sock.recv(8192).decode('utf-8')
        if len(Message) > 0:
            break

    sock.sendall(bytes("AUTH TLS\r\n", 'utf-8'))
    while True:
        Message = ""
        while not '\n' in Message:
            Message += sock.recv(8192).decode('utf-8')
        Message1 = Message.split(' ')
        code = Message1[0]
        int(code)
        if code / 200 == 1:
            break
        else:
            raise ValueError
    s = ssl.wrap_socket(sock)

    if username == "":
        s.sendall(bytes("USER anonymous\r\n", 'utf-8'))
    else:
        s.sendall(bytes("USER " + username + "\r\n", 'utf-8'))
    while True:
        Message = ""
        while not '\n' in Message:
            Message += s.recv(8192).decode('utf-8')
        Message1 = Message.split(' ')
        code = Message1[0]
        int(code)
        if code / 200 == 1 or code / 300 == 1:
            break
        else:
            raise ValueError

    if password != "none":
        s.sendall(bytes("PASS " + password + "\r\n", 'utf-8'))
        while True:
            Message = ""
            while not '\n' in Message:
                Message += s.recv(8192).decode('utf-8')
            Message1 = Message.split(' ')
            code = Message1[0]
            int(code)
            if code / 200 == 1:
                break
            else:
                raise ValueError

    s.sendall(bytes("PBSZ 0\r\n", 'utf-8'))
    while True:
        Message = ""
        while not '\n' in Message:
            Message += s.recv(8192).decode('utf-8')
        Message1 = Message.split(' ')
        code = Message1[0]
        int(code)
        if code / 200 == 1:
            break
        else:
            raise ValueError

    s.sendall(bytes("PROT P\r\n", 'utf-8'))
    while True:
        Message = ""
        while not '\n' in Message:
            Message += s.recv(8192).decode('utf-8')
        Message1 = Message.split(' ')
        code = Message1[0]
        int(code)
        if code / 200 == 1:
            break
        else:
            raise ValueError

    if command == "DELE" or command == "MKD" or command == "RMD":
        s.sendall(bytes(command, 'utf-8'))
        while True:
            Message = ""
            while not '\n' in Message:
                Message += s.recv(8192).decode('utf-8')
            Message1 = Message.split(' ')
            code = Message1[0]
            int(code)
            if code / 200 == 1:
                break
            else:
                raise ValueError
    else:
        s.sendall(bytes("TYPE I\r\n", 'utf-8'))
        while True:
            Message = ""
            while not '\n' in Message:
                Message += s.recv(8192).decode('utf-8')
            Message1 = Message.split(' ')
            code = Message1[0]
            int(code)
            if code / 200 == 1:
                break
            else:
                raise ValueError

        s.sendall(bytes("MODE S\r\n", 'utf-8'))
        while True:
            Message = ""
            while not '\n' in Message:
                Message += s.recv(8192).decode('utf-8')
            Message1 = Message.split(' ')
            code = Message1[0]
            int(code)
            if code / 200 == 1:
                break
            else:
                raise ValueError

        s.sendall(bytes("STRU F\r\n", 'utf-8'))
        while True:
            Message = ""
            while not '\n' in Message:
                Message += s.recv(8192).decode('utf-8')
            Message1 = Message.split(' ')
            code = Message1[0]
            int(code)
            if code / 200 == 1:
                break
            else:
                raise ValueError

        s.sendall(bytes("PASV\r\n", 'utf-8'))
        while True:
            Message = ""
            while not '\n' in Message:
                Message += s.recv(8192).decode('utf-8')
            Message1 = Message.split(' ')
            code = Message1[0]
            int(code)
            if code != 227:
                raise ValueError
            else:
                ipAndPort = Message1[4]
                length = len(ipAndPort)
                ipAndPort = ipAndPort[1:length-2]
                nums = ipAndPort.split(',')
                IP = nums[0] + "." + nums[1] + "." + nums[2] + "." + nums[3]
                port1 = bin(nums[4])
                port2 = bin(nums[5])
                port1 = port1[2:]
                port2 = port2[2:]
                fullPortSTR = str(port1) + str(port1)
                fullPortINT = int(fullPortSTR, 2)
                # converted back from binary string to int
                break

        s.sendall(bytes(command, 'utf-8'))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock2:
            sock2.connect((IP, fullPortINT))
            while True:
                Message = ""
                while not '\n' in Message:
                    Message += s.recv(8192).decode('utf-8')
                Message1 = Message.split(' ')
                code = Message1[0]
                int(code)
                if code / 400 == 1 or code / 500 == 1 or code / 600 == 1:
                    sock2.close()
                    raise ValueError
                else:
                    break

            s2 = ssl.wrap_socket(sock2)
            if sendFile:
                with open(localFile, "rb") as f:
                    while True:
                        readSoFar = f.read(4096)
                        if not readSoFar:
                            break
                        s2.sendall(readSoFar)
            elif createFile:
                # receive file and create it
                with open(localFile, "wb") as f:
                    while True:
                        readSoFar = s2.recv(4096)
                        if not readSoFar:
                            break
                        f.write(readSoFar)

            if delete == "local":
                # delete the file locally
                os.remove(localFile)
            elif delete == "remote":
                s2.sendall(bytes(command2, 'utf-8'))
                # delete the file remotely

            s2.close()
            while True:
                Message = ""
                while not '\n' in Message:
                    Message += s.recv(8192).decode('utf-8')
                Message1 = Message.split(' ')
                code = Message1[0]
                int(code)
                if code / 200 == 1:
                    break
                else:
                    raise ValueError
            s.close()
