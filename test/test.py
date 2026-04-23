import socket

host = "127.0.0.1"
port = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

print("Server running on http://127.0.0.1:9000")

while True:
    client, addr = server.accept()
    request = client.recv(1024).decode()

    print("Request:")
    print(request)

    html = "<html><body><h1>Привет 👋</h1></body></html>"

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{html}"
    )

    client.sendall(response.encode())
    client.close()