import os
import re
import socket
import threading
import json

FOLDER_NAME = 'client_media'
HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

def upload_file(message):
    file_path = message.split()[1]
    file_name = file_path.split('\\')[-1]
    print(file_name)
    
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        client_socket.send(json.dumps(
            {
                "type": "upload",
                "data": {
                    "file_name": file_name,
                    "file_size": file_size,
                }
            }
        ).encode('utf-8'))

        with open(file_path, 'rb') as file:
            client_socket.send(file.read(file_size))
    else:
        print(f"The {file_name} doesn't exist")


def download_file(client_socket, data, name):
    file_name = data['file_name']
    
    with open(f"{FOLDER_NAME}/{name}/{file_name}", f'{"w" if os.path.exists(f"{FOLDER_NAME}/{name}/{file_name}") else "x"}b') as received_file:
        received_file.write(client_socket.recv(data['file_size']))

    print('File was downloaded succesfully')

def process_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break  

            message = json.loads(data)
            data = message["data"]

            match message["type"]:
                case "sending":
                    sender = data["name"]
                    message = data["text"]
                    print(f"{sender} : {message}\n")
                case "notification":
                    print(data['text'])
                case "download-ack":
                    download_thread = threading.Thread(target=download_file, args=(client_socket, data, name))
                    download_thread.start()
                    download_thread.join()
                case _:
                    print("Unknown message type")

        except Exception as e:
            print(f"Error receiving messages: {e}")
            break


room = input("Enter your room\n")
name = input("Enter your name\n")

login_data = {
        "type": "login",
        "data":
        {
            "name": name,
            "room": room,
        }
    }

client_socket.send(json.dumps(login_data).encode('utf-8'))

receive_thread = threading.Thread(target=process_messages)
receive_thread.daemon = True
receive_thread.start()

if not os.path.isdir(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)
if not os.path.isdir(f"{FOLDER_NAME}/{name}"):
    os.mkdir(f"{FOLDER_NAME}/{name}")

print("Enter a message (or 'exit' to quit):\n")

while True:
    message = input("")

    if message.lower() == 'exit':
        client_socket.send(json.dumps(
            {
                "type" : "leave"
            }
        ).encode('utf-8'))
        break
    elif re.match(r'upload: ([A-Za-z0-9\.:]+)', message):
        upload_thread = threading.Thread(target=upload_file, args=(message,))   
        upload_thread.start() 
        upload_thread.join()
    elif re.match(r'download: ([A-Za-z0-9\.]+)', message):
        client_socket.send(json.dumps(
            {
                "type": "download",
                "data":
                {
                    "file_name": message.split()[1]
                }
            }
        ).encode('utf-8'))
    else:
        client_socket.send(json.dumps(
            {
                "type": "sending",
                "data":
                { 
                    "text": message
                }
            }
        ).encode('utf-8'))

   