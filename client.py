import socket as s


sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.connect(("192.168.68.137", 12345))
buffer = 4096
print("Connected to server")

while 1:
    print("Enter request type:\n 0 for adding to db\n 1 for retrieving from db\ne to exit")
    request = input()
    if request == "0":
        print("Enter text to add to db")
        send_data = b"\x00" + input().encode()
        send_data = len(send_data).to_bytes(4, "big") + send_data

        sock.send(send_data)
        print("Sent to db")
        sock.recv(8)
        print("Added to db")
    if request == "1":
        print("Enter start index of send_data points")
        s = input()
        print("Enter end index of send_data points")
        e = input()

        send_data = f"{s},{e}"
        send_data = b"\x01" + str(send_data).encode()
        send_data = len(send_data).to_bytes(4, "big") + send_data
        sock.send(send_data)

        recv_data = sock.recv(buffer)
        len_bytes = int.from_bytes(recv_data[:4], "big")
        recv_data = recv_data[4:]
        while len(recv_data) < len_bytes:
            recv_data += sock.recv(buffer)
            print("data is longer than buffer")
        print(recv_data.decode())
    if request == "e":
        sock.close()
