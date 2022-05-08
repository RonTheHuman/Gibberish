import socket_util as su

sock = su.client("192.168.68.137", 12345)
# forum_data_arr = su.send_request(sock, 10, ("_id", "text", "description"))
# print("All forms:")
# for forum_data in forum_data_arr:
#     print(f"id: {forum_data['_id']}| Name: {forum_data['name']}, description: {forum_data['description']}")
with open("wordlist_10000.txt") as f:
    words = f.read().splitlines()
for word in words:
    su.send_request(sock, 1, (word, word*2))
