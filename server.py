import socket
from src import serialize_resp, deserialize_resp

# Constants
HOST = '127.0.0.1'  
PORT = 6380         

def handle_client(client_socket):
    while True:
        resp_message = client_socket.recv(4096)
        if not resp_message:
            break  # no more data from client
        
        message, _ = deserialize_resp(resp_message)
        if not isinstance(message, list):
            continue  
        
        command = message[0].lower()
        if command == 'ping':
            response = 'PONG'
        elif command == 'echo' and len(message) > 1:
            response = message[1]
        else:
            response = f"ERROR: Unrecognized command '{command}'"
        
        # send the serialized response
        client_socket.send(serialize_resp(response))

def redis_lite_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Redis Lite server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            handle_client(client_socket)
            client_socket.close()
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    redis_lite_server()