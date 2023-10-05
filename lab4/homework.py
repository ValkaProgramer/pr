import socket
from bs4 import BeautifulSoup
import re
import os
import json

HOST = '127.0.0.1'
PORT = 8080

html_endpoints = ['/', '/about', '/contacts', '/productslist']
product_endpoint = '/product'

def send_endpoint_request(endpoint: str):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    request = f'GET {endpoint} HTTP/1.1\nHost: {HOST}:{PORT}'
    client_socket.send(request.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    header, body = response.split('\n', 1)
    print(f'Response status: {header}')
    client_socket.close()

    return body

def process_endpoints():
    for end_point in html_endpoints:
        body = send_endpoint_request(end_point)

        end_point = re.sub(r'/', r'loaded_', end_point)
        
        with open(f'./htmls/{end_point}.html', 'x' if len(os.listdir('./htmls')) == 0 else 'w') as f:
            f.write(body)

    body = send_endpoint_request('/productslist')
    soup = BeautifulSoup(body, 'html.parser')

    links = [item['href'] for item in soup.find_all('a')]
    json_list = []
    for link in links:
        dictionary = {}
        product_response = send_endpoint_request(link)
        parser = BeautifulSoup(product_response, 'html.parser').body

        some = [item.contents[0] for item in parser.find_all('span')]
        for item in some:
            dictionary[item.partition(':')[0][:-1]] = item.partition(':')[2][1:]

        json_list.append(dictionary)
        
    
    with open('./data_products.json', 'x' if len(os.listdir('./htmls')) == 0 else 'w') as prods:
        prods.write(json.dumps(json_list))
    

process_endpoints()