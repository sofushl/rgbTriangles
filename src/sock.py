import json
import socket

import network

wlan = network.WLAN(network.STA_IF)
wlan.config(pm=0xA11140)
print(wlan.ifconfig())

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))
s.listen(1)
print("Listening on port 80")


def read_request(conn):
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(512)
        if not chunk:
            break
        data += chunk

    head, _, body = data.partition(b"\r\n\r\n")

    length = 0
    for line in head.split(b"\r\n"):
        if line.lower().startswith(b"content-length:"):
            length = int(line.split(b":", 1)[1])
    while len(body) < length:
        chunk = conn.recv(512)
        if not chunk:
            break
        body += chunk

    return body.decode()


def listen():
    while True:
        conn, addr = s.accept()
        try:
            body = read_request(conn)
            conn.send(
                "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nok\n"
            )
            conn.close()
            data = json.loads(body)
            return (
                data.get("mode"),
                data.get("brightness"),
                data.get("speed"),
                data.get("r"),
                data.get("g"),
                data.get("b"),
            )
        except Exception as e:
            print("Error:", e)
            try:
                conn.send(
                    "HTTP/1.1 400 ERROR\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nErr\n"
                )
            except:
                print("Error:", e)
            conn.close()
