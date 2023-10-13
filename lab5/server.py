import os
import socket
import threading
import json

FOLDER_NAME = 'server_media'
HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

def upload_file(client_socket, request_data):
    room = clients[client_socket]['room']
    file_name = request_data['file_name']
    print(file_name)
    if not os.path.isdir(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)
    if not os.path.isdir(f"{FOLDER_NAME}/{room}"):
        os.mkdir(f"{FOLDER_NAME}/{room}")

    with open(f"{FOLDER_NAME}/{room}/{file_name}", f'{"w" if os.path.exists(f"{FOLDER_NAME}/{room}/{file_name}") else "x"}b') as received_file:
        received_file.write(client_socket.recv(request_data['file_size']))

    for client in rooms[clients[client_socket]['room']]:
                        if client != client_socket:
                            client.send(json.dumps(
                                {
                                    "type": "notification",
                                    "data":
                                    {
                                        "text": f"{clients[client_socket]['name']} uploaded {file_name}\n"
                                    }
                                }
                            ).encode('utf-8'))
    
    client_socket.send(json.dumps(
        {
            "type": "notification",
            "data":
            {
                "text": f"{file_name} uploaded succesfully\n"
            }
        }
    ).encode('utf-8'))

def download_file(client_socket, request_data):
    file_name = request_data['file_name']
    file_path = f"{FOLDER_NAME}/{clients[client_socket]['room']}/{file_name}"
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)

        client_socket.send(json.dumps(
            {
                "type": "download-ack",
                "data":
                {
                    "file_name": file_name,
                    "file_size": file_size
                }
            }
        ).encode('utf-8'))

        with open(file_path, 'rb') as file:
            client_socket.send(file.read(file_size))
    else:
        client_socket.send(json.dumps(
            {
                "type": "notification",
                "data":
                {
                    "text": f"The {file_name} doesn't exist.\n"
                }
            }
        ).encode('utf-8'))


def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    while True:
        try:
            temp = client_socket.recv(4096).decode('utf-8')
            if not temp:
                break

            request = json.loads(temp)
            message_type = request["type"]
            data = request["data"]


            match message_type:
                case "sending":
                    sender = clients[client_socket]["name"]
                    room = clients[client_socket]["room"]
                    text = data["text"]
                    print(f"Received from {sender} in '{room}': {text}")

                    for client in rooms[clients[client_socket]['room']]:
                        if client != client_socket:
                            client.send(json.dumps(request).encode('utf-8'))
                
                case "login":
                    clients[client_socket]['name'] = data["name"]
                    clients[client_socket]['room'] = data["room"]
                    
                    if not clients[client_socket]['room'] in rooms.keys():
                        rooms[clients[client_socket]['room']] = []
                    
                    rooms[clients[client_socket]['room']].append(client_socket)

                    for client in rooms[clients[client_socket]['room']]:
                        if client != client_socket:
                            client.send(json.dumps(
                                {
                                    "type" : "notification",
                                    "data":
                                    {
                                        "text" : f"{clients[client_socket]['name']} just joined your room"
                                    }
                                }
                            ).encode('utf-8'))
                
                case "leave":
                    for client in rooms[clients[client_socket]['room']]:
                        if client != client_socket:
                            client.send(json.dumps(
                                {
                                    "type" : "notification",
                                    "data":
                                    {
                                        "text" : f"{clients[client_socket]['name']} just jeft"
                                    }
                                }
                            ).encode('utf-8'))
                    clients.pop(client_socket)
                    client_socket.close()
                case "upload":
                    upload_thread = threading.Thread(target=upload_file, args=(client_socket, data))
                    upload_thread.start()
                    upload_thread.join()
                case "download":
                    download_thread = threading.Thread(target=download_file, args=(client_socket, data))
                    download_thread.start()
                    download_thread.join()
                case _:
                    print("Unknown message type")

        except Exception as e:
            print(f"Error handling client: {e}")
            break

clients = {}
rooms = {}

while True:
    client_socket, client_address = server_socket.accept()
    clients[client_socket] = {}
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()