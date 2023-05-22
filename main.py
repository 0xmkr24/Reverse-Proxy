import socket
import Reverse_proxy
# import checkIPRepuration

if __name__ == '__main__':
    # Create a listening socket
    waf_ip = '127.0.0.1'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((waf_ip, 80))
    server_socket.listen(5)
    print(f'Reverse proxy is listening on http://{waf_ip} port 80...')


    while True:
        client_socket, client_address = server_socket.accept()
        print('Connection from', client_address)
        response = Reverse_proxy.handle_request(client_socket)
        request_lines = response.decode().split('\r\n')
        Reverse_proxy.redirect_to_backend(response,client_socket)
        print(request_lines)
        print(response)
        print(method, headers, path, query_params, body_params)
        # Extract Request Data
        method, headers, path, query_params, body_params = Reverse_proxy.Unpack_request(request_lines)


        # Reverse_proxy.redirect_to_backend(client_socket)