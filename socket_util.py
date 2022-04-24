import socket
from select import select


def add_len_bytes(data):
    return len(data).to_bytes(4, "big") + data


def recv(sock, buffer=4069):
    data = sock.recv(buffer)
    len_bytes = int.from_bytes(data[:4], "big")
    data = data[4:]
    while len(data) < len_bytes:
        data += sock.recv(buffer)
        print("Data is longer than buffer")
    return data


def send_request(sock, req_id, data):
    data = req_id.to_bytes(1, "big") + data
    sock.send(add_len_bytes(data))
    print("Sent to db")
    return recv(sock)


def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print("Connected to server")
    return sock


def server(port, reply):
    ip = socket.gethostbyname(socket.gethostname())
    addr = (ip, port)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(addr)
    server_sock.listen(5)

    inputs = [server_sock]
    outputs = []
    msg_queues = {}

    while True:
        print("Waiting for the next event")
        readable, writeable, exceptional = select(inputs, outputs, inputs)
        for s in readable:
            if s is server_sock:
                client_sock, client_addr = server_sock.accept()
                print(f"Connected to {client_addr}")
                inputs.append(client_sock)
                msg_queues[client_sock] = list()
            else:
                recv_data = recv(s)
                if recv_data:
                    if s not in outputs:
                        outputs.append(s)
                    print(f"Got data: {recv_data}")
                    req_id = recv_data[0]
                    recv_data = recv_data[1:]
                    msg_queues[s].append(reply(req_id, recv_data))
                else:
                    print(f"Disconnected {s.getsockname()}")
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    del msg_queues[s]
                    s.close()
        for s in writeable:
            for msg in msg_queues[s]:
                print(f"Sent {msg} to {s.getsockname()}")
                s.send(msg_queues[s].pop(0))
            outputs.remove(s)
        for s in exceptional:
            inputs.remove(s)
            print(f"Removed {s} after error")
            if s in outputs:
                outputs.remove(s)
            s.close()
            del msg_queues[s]
