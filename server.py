import socket
from src import serialize_resp, deserialize_resp, handle_ping, handle_set, handle_get, handle_echo, handle_default

HOST = '127.0.0.1'
PORT = 6380

data_store = {}

def handle_client(client_socket, data_store):
    command_handlers = {
        'ping': handle_ping,
        'set': lambda message: handle_set(message, data_store),
        'get': lambda message: handle_get(message, data_store),
        'echo': handle_echo,
    }

    while True:
        resp_message = client_socket.recv(4096)
        if not resp_message:
            break

        message, _ = deserialize_resp(resp_message)
        if not isinstance(message, list):
            response = "ERROR: Command must be an array with at least 2 elements"
        else:
            command = message[0].lower()
            handler = command_handlers.get(command, handle_default)
            response = handler(message)

        client_socket.send(serialize_resp(response))


def redis_lite_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Redis Lite server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Accepted connection from {client_address}")
                handle_client(client_socket, data_store)
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    redis_lite_server()