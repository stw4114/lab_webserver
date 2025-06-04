# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))

    # Start listening with a queue of 1 connection
    serverSocket.listen(1)

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]

            # opens the client requested file in binary mode
            f = open(filename[1:], "rb")
            file_content = f.read()
            f.close()

            # HTTP response header
            header = (
                "HTTP/1.1 200 OK\r\n"
                "Server: MySimplePythonServer/1.0\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(file_content)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode()

            # Send header + content
            connectionSocket.send(header + file_content)

            connectionSocket.close()  # closing the connection socket

        except Exception as e:
            # 404 Not Found response
            error_message = (
                "<html><body><h1>404 Not Found</h1></body></html>"
            ).encode()
            header = (
                "HTTP/1.1 404 Not Found\r\n"
                "Server: MySimplePythonServer/1.0\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(error_message)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode()

            connectionSocket.send(header + error_message)

            connectionSocket.close()


if __name__ == "__main__":
    webServer(13331)
