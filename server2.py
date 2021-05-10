"""
 Простейший веб-сервер с главной страницей

"""

import socket


# Определяем хост и порт для сокета
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# CСоздаём сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print('Listening on port %s...' % SERVER_PORT)

while True:
    # Ожидаем подключения клиента
    client_connection, client_address = server_socket.accept()

    # Получаем запрос
    request = client_connection.recv(8192).decode()
    print(request)

    # Получаем содержимое файла index.html
    file = open('index.html')
    content = file.read()
    file.close()

    # Отправляем HTTP ответ
    response = 'HTTP/1.0 200 OK\n\n' + content
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()