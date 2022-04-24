import socket_util as su


sock = su.client("192.168.68.137", 12345)
running = True
while running:
    print("\nEnter action:\n 0 for adding to db\n 1 for retrieving from db\n e to exit")
    action = input()
    send_req = True
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
        running = False
        send_req = False
    else:
        print("invalid action")
        send_req = False
    if send_req:
        print(su.send_request(sock, int(action), send_data).decode())

