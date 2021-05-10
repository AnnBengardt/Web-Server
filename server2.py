"""
 Простейший веб-сервер с главной страницей

"""

import socket
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime


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

    # Парсим заголовки запроса
    headers = request.split('\n')
    # print(headers)
    filename = headers[0].split()[1]

    # Get the content of the file
    if filename == '/':
        filename = '/index.html'
    elif '.html' not in filename:
        filename += '.html'

    # Получаем содержимое запрошенного файла и составляем ответ с заголовками
    try:
        file = open(filename[1:])
        content = file.read()
        file.close()

        response = """HTTP/1.1 200 OK
            Server: SelfMadeServer v0.0.1
            Content-type: text/html
            Content-length: 5000
            Date: """ + format_date_time(mktime(datetime.now().timetuple())) + """\nConnection: close\n\n""" + content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\n<h2>Page Not Found!</h2>'

    # Отправляем HTTP ответ
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()