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
    mac_dest, mac_orig, protocol = ethernet_frame(pack)
    print('MAC Dest: ', ':'.join(format(x, '02x') for x in mac_dest))
    print('MAC Orig: ', ':'.join(format(x, '02x') for x in mac_orig))
    if protocol == 0x0806:
        print('Tipo: ARP')
        print(pack[48:64])
    elif protocol == 0x0800:
        print('Tipo: IPv4')
    elif protocol == 0x86DD:
        print('Tipo: IPv6')
    else:
        print('Pacote ignorado')
    print()
