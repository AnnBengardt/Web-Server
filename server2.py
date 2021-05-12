"""
 Простейший веб-сервер с главной страницей

"""

import socket
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import threading


settings_txt = open('settings.txt', 'r')
settings = {}
for i in settings_txt.readlines():
    settings[i.split("=")[0]] = i.split("=")[1]

# Определяем хост, порт для сокета и рабочую директорию из файла с настройками
SERVER_HOST = settings['SERVER_HOST'][:-1]
SERVER_PORT = int(settings['SERVER_PORT'])

server_folder = settings['SERVER_FOLDER'][:-1]

# Cоздаём сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print('Listening on port %s...' % SERVER_PORT)


def request_procees():
    request = client_connection.recv(int(settings['DATA_SIZE'])).decode()
    print(request)

    # Парсим заголовки запроса
    headers = request.split('\n')
    # print(headers)
    filename = headers[0].split()[1]

    # Get the content of the file
    supported_types = ['html', 'jpg', 'png']
    if filename == '/':
        filename = server_folder+'/index.html'
    elif '.' not in filename:
        filename += '.html'

    # Получаем содержимое запрошенного файла и составляем ответ с заголовками
    try:
        assert filename.split('.')[1] in supported_types

        print(filename, '2')
        file = open(server_folder+filename)
        content = file.read()
        file.close()
        response = """HTTP/1.1 200 OK
                Server: SelfMadeServer v0.0.1
                Content-type: text/html
                Content-length: 5000
                Date: """ + format_date_time(mktime(datetime.now().timetuple())) + """\nConnection: close\n\n""" + content

        with open('/home/anna-beng/PycharmProjects/WebServer/log.txt', 'a+') as log:
            log.write(str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + ' - ' + client_connection.getpeername()[0]
                      + ' - ' + filename + ' - None\n')

    except AssertionError:
        response = 'HTTP/1.0 403 FORBIDDEN\n\nForbidden file type!'
        with open('/home/anna-beng/PycharmProjects/WebServer/log.txt', 'a+') as log:
            log.write(str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + ' - ' + client_connection.getpeername()[0]
                      + ' - ' + filename + ' - 403\n')
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nPage Not Found!'
        with open('/home/anna-beng/PycharmProjects/WebServer/log.txt', 'a+') as log:
            log.write(str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + ' - ' + client_connection.getpeername()[0]
                      + ' - ' + filename + ' - 404\n')
    finally:
        client_connection.sendall(response.encode())
        client_connection.close()

while True:
    # Ожидаем подключения клиента
    client_connection, client_address = server_socket.accept()
    t = threading.Thread(target=request_procees)
    t.daemon = True
    t.start()
    # Отправляем HTTP ответ


# Close socket
server_socket.close()