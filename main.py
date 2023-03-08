import socket

ETH_P_ALL = 3
BUFFSIZE = 1518

sockd = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

pack = sockd.recv(BUFFSIZE)
ethHeader = pack[0][0:14]
print(ethHeader)
