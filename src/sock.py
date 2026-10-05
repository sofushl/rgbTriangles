import socket
import json
import network

wlan = network.WLAN(network.STA_IF)
wlan.config(pm=0xa11140)
print(wlan.ifconfig())

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))
s.listen(1)
print("Listening on port 80")


def read_request(conn):
    data = b""
# read until the end of the headers
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(512)
        if not chunk:
            break
        data += chunk

    head, _, body = data.partition(b"\r\n\r\n")

    # read the rest of the body if it's longer than what we've got
    length = 0
    for line in head.split(b"\r\n"):
        if line.lower().startswith(b"content-length:"):
            length = int(line.split(b":", 1)[1])
    while len(body) < length:
        chunk = conn.recv(512)
        if not chunk:
            break
        body += chunk

    return head.decode(), body.decode()

def listen():
    while True:
        conn, addr = s.accept()
        print("Connection from", addr)
        try:
            head, body = read_request(conn)
            print(head.split("\r\n")[0])  # request line, e.g. "POST / HTTP/1.1"
            try:
                print("Parsed:", json.loads(body))
            except ValueError:
                print("Body:", body)
            conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nok")
            conn.close()
            data = json.loads(body)
            return data.get("mode") 
        except Exception as e:
            print("Error:", e)
            conn.close()

