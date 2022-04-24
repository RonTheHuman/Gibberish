import socket as s
from functools import reduce
from select import select


def bind():
    ip = s.gethostbyname(s.gethostname())
    port = 12345
    addr = (ip, port)
    server_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_sock.bind(addr)
    server_sock.listen(5)
    return server_sock, server_sock.getsockname()[1]


dbase = ["text", "undulation", "werewolf", "porch", "qwerty", "apple"]
dbase.sort()
server_sock, port = bind()
buffer = 4096

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
            data = s.recv(buffer)
            if data:
                print(f"Got initial data: {data}")
                len_bytes = int.from_bytes(data[:4], "big")
                data = data[4:]
                while len(data) < len_bytes:
                    print("data is longer than buffer")
                    data += s.recv(buffer)
                print(f"Received data from {s.getsockname()}")

                if s not in outputs:
                    outputs.append(s)

                print(f"Got msg: {data}")
                request = data[0]
                data = data[1:]
                if request == 0:
                    dbase.append(data.decode())
                    dbase.sort()

                    msg_queues[s].append("ack".encode())
                if request == 1:
                    start, end = data.decode().split(",")
                    send_data = reduce(lambda x, y: f"{x}, {y}", dbase[int(start):int(end)]).encode()
                    send_data = len(send_data).to_bytes(4, "big") + send_data
                    msg_queues[s].append(send_data)
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




