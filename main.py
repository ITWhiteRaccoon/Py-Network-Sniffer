import socket
import struct

ETH_P_ALL = 3
BUFFSIZE = 1518


def ethernet_frame(raw_dados):
    mac_destino, mac_fonte, protocolo = struct.unpack('! 6s 6s H', raw_dados[:14])
    return mac_destino, mac_fonte, protocolo


sockd = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

while True:
    pack = sockd.recv(BUFFSIZE)
    mac_dest, mac_orig, tipo = ethernet_frame(pack)
    if tipo == 0x0800:
        print('IPv4')
    elif tipo == 0x0806:
        print('ARP')
    elif tipo == 0x86DD:
        print('IPv6')
