import socket
from functools import reduce
from select import select


def recv(sock, buffer=4069):
    data = sock.recv(buffer)
    len_bytes = int.from_bytes(data[:4], "big")
    data = data[4:]
    while len(data) < len_bytes:
        data += sock.recv(buffer)
        print("Data is longer than buffer")
    return data


def add_len_bytes(data):
    return len(data).to_bytes(4, "big") + data


def reply(req_id, data):
    if req_id == 0:
        dbase.append(data.decode())
        dbase.sort()
        return add_len_bytes("ack".encode())
    elif req_id == 1:
        start, end = data.decode().split(",")
        send_data = reduce(lambda x, y: f"{x}, {y}", dbase[int(start):int(end)]).encode()
        return add_len_bytes(send_data)


def server(reply):
    ip = socket.gethostbyname(socket.gethostname())
    port = 12345
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


dbase = ["text", "undulation", "werewolf", "porch", "qwerty", "apple"]
dbase.sort()

server(reply)
