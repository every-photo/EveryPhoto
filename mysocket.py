import socket
import threading
import json
import db
import shrinkpic
import os


lock = threading.Lock()
target = {}


def parseJson( jsontxt):
    data = json.loads(jsontxt)
    print('index json data: ', data)
    if not data['labels']: return
    path = data['path']
    largepath = 'uploads' + path[len(os.environ['HOME']):]
    smallpath = shrinkpic.shrink(path)
    path = smallpath + ' ' + largepath + ' ' + path
    for label, score in zip(data['labels'], data['scores']):
        lock.acquire()
        if label not in target: target[label] = {}
        target[label][path] = score
        lock.release()


def getJson( connection):
    jsontxt = ''
    while True:
        try:
            txt = connection.recv(1024).decode('utf-8')
            if not txt: return
            jsontxt += txt
            while True:
                index = jsontxt.find('\n')
                if index < 0: break
                parseJson(jsontxt[:index])
                jsontxt = jsontxt[index+1 : ]
        except ConnectionResetError:
            while True:
                index = jsontxt.find('\n')
                if index < 0: break
                parseJson(jsontxt[:index])
                jsontxt = jsontxt[index+1 : ]
            connection.close()
            return
    return


def recvData(dbid, port = 8888):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", port))
    server.listen(10)
    threadlist = []
    print('Waiting for connection...')
    while len(threadlist) < 2:
        connection, address = server.accept()
        print("accept request from ", address)
        threadlist.append(threading.Thread(target = getJson, args = (connection,)))
        threadlist[-1].start()
    print('2 connection was created!')
    for thread in threadlist:
        thread.join()
    print('db data: ', target)
    db.input_info(target, dbid)


if __name__ == '__main__':
    recvData(0)
