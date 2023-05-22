import json
import socket
import re
import urllib
import select


TARGET_HOST = '127.0.0.1'
TARGET_PORT = 8080
INVALID_REQUEST_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Invalid Request</title>
</head>
<body>
    <h1>Invalid Request</h1>
</body>
</html>
'''


def handle_request(client_socket):
    # Read client Request
    request = client_socket.recv(4096)
    # print(request)
    return request


def Unpack_request(request_lines):
    # Extract method, path
    method, path, version = request_lines[0].split()
    # Extract Headers
    headers = {}
    for line in request_lines[1:]:
        if not line:
            break
        key, value = line.split(': ', 1)
        headers[key] = value.strip()

    # Extract Path
    if '?' in path:
        path, query = path.split('?')
        query_params = {}
        for param in query.split('&'):
            key, value = param.split('=')
            query_params[key] = value
    else:
        query_params = {}
    # Extract Body
    # Json Body

    body = request_lines[-3]
    if 'Content-Type' in headers and headers['Content-Type'] == 'application/json':
        body_params = json.loads(f'{{{body}}}')
    else:
        body_params = dict(urllib.parse.parse_qsl(body))

    return method,headers,path,query_params,body_params



def redirect_to_backend(request,client_socket):
    
    # Create a new socket to connect to the target server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((TARGET_HOST, TARGET_PORT))
    
    # Forward the request to the target server
    server_socket.sendall(request)
    while True:
        # Wait until the server socket is ready to be read
        ready_sockets, _, _ = select.select([server_socket], [], [], 1)
        if ready_sockets:
            # Read the response from the server
            response = server_socket.recv(4096)

            client_socket.sendall(response)
            if not response:
                break
        else:

            break
    # Close the sockets
    client_socket.close()
    server_socket.close()

    return response
