import socket as s


def recv(socket, buffer=4069):
    data = socket.recv(buffer)
    len_bytes = int.from_bytes(data[:4], "big")
    data = data[4:]
    while len(data) < len_bytes:
        data += socket.recv(buffer)
        print("Data is longer than buffer")
    return data


def add_len_bytes(data):
    return len(data).to_bytes(4, "big") + data


def send_request(socket, req_id, data):
    data = req_id.to_bytes(1, "big") + data
    socket.send(add_len_bytes(data))
    print("Sent to db")
    return recv(sock)


sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.connect(("192.168.68.137", 12345))
print("Connected to server")

open = True
while open:
    send_req = True

    print("Enter action:\n 0 for adding to db\n 1 for retrieving from db\n e to exit")
    action = input()
    if action == "0":
        print("Enter text to add to db")
        send_data = input().encode()
    elif action == "1":
        print("Enter start index of send_data points")
        s = input()
        print("Enter end index of send_data points")
        e = input()
        send_data = f"{s},{e}".encode()

    elif action == "e":
        sock.close()
        open = False
        send_req = False

    else:
        print("invalid action")
        send_req = False

    if send_req:
        print(send_request(sock, int(action), send_data).decode())

