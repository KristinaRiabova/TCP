import socket
import os

BUFFER_SIZE = 1024
CLIENT_FILES_DIRECTORY = 'client_files'


def save_file(filename, file_data):
    with open(os.path.join(CLIENT_FILES_DIRECTORY, filename), 'wb') as file:
        file.write(file_data)


def main():
    port = 12340
    server_ip = '127.0.0.1'

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, port))

        while True:
            user_input = input(
                "Enter command (GET <filename>, LIST, PUT <filename>, DELETE <filename>, INFO <filename>, EXIT): ")
            message = user_input.encode()
            client_socket.send(message)

            if user_input == "EXIT":
                break

            if user_input.startswith("PUT"):
                filename = user_input[4:]
                try:
                    with open(os.path.join(CLIENT_FILES_DIRECTORY, filename), 'rb') as file:
                        file_size = os.path.getsize(file.name)
                        client_socket.send(str(file_size).encode())

                        file_data = file.read(BUFFER_SIZE)
                        while file_data:
                            client_socket.send(file_data)
                            file_data = file.read(BUFFER_SIZE)

                    response = client_socket.recv(BUFFER_SIZE).decode()
                    print(f"Received from server: {response}")
                except FileNotFoundError:
                    print(f"Error opening file: {filename}")

            else:
                response = client_socket.recv(BUFFER_SIZE)
                if user_input.startswith("GET"):
                    filename = user_input[4:]
                    save_file(filename, response)
                    print(f"Received and saved file: {filename}")
                else:
                    print(f"Received from server: {response}")

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
