import re
import socket
import signal
import sys
import threading
import json

HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(5) # Increased backlog for multiple simultaneous connections
print(f"Server is listening on {HOST}:{PORT}")

def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()

    method = request_line[0]
    path = request_line[1]

    response_content = ''
    status_code = 200

    if path == '/':
        with open('home.html') as f:
            response_content = f.read()
    elif path == '/about':
        with open('about_us.html') as f:
            response_content = f.read()
    elif path == '/contacts':
        with open('contacts.html') as f:
            response_content = f.read()
    elif re.match('.*/product[0-9]+', path):
        with open('product.html') as f:
            j = open('./products.json')
            data = json.load(j)
            j.close()
            response_content = f.read()
            page = int(path.partition('product')[2])
            
            for key in data[page].keys():
                response_content = response_content.replace(key + '_key', key)
                response_content = response_content.replace(key +'_value', str(data[page][key]))
    elif path == '/productslist':
        with open('productslist.html') as f:
            response_content = f.read()
            j = open('./products.json')
            data = json.load(j)
            j.close()
            links = ''
            for item in data:
                links += '<a href = "http://127.0.0.1:8080/product' + str(data.index(item)) + '">' + item['name'] + '</a>'
            response_content = response_content.replace('<a></a>', links)
    else:
        response_content = '404 Not Found'
        status_code = 404

    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))

    client_socket.close()

def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()