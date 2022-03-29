import socket
import select
import threading

Send_Private = "2"
Setup_User = "1"
Close_Connection = "0"

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "127.0.0.1"
print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
client_sockets = []
all_clients = {}

""" 
def send_msg_private(name):
    recever = all_clients[name]
    #send to name
    print(recever)
"""




while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, [], [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data:
                """
                    if data[0] == Send_Private:
                    newdata = data[1:]
                    newdata = newdata.replace("private", "")
                    name = newdata
                    send_msg_private(name)
                """



                if data[0] == Setup_User:
                    i = 1
                    data_counter = 1
                    name = ""
                    while data[i] != "©":
                        name = name + data[i]
                        data_counter = data_counter + 1
                        i = i+1
                    #print(name)
                    j = 1
                    password = data[data_counter+1:]
                    # ליעל את הפעולה!
                    print(client_address, "client want to set up his username and password")
                    all_clients[name, password] = current_socket
                    print(data)
                    print(all_clients)

                if data[0] == Close_Connection:
                    print("Connection closed", client_address)
                    client_sockets.remove(current_socket)
                    current_socket.close()



"""
"ori": socket
"gilad: 
"""



