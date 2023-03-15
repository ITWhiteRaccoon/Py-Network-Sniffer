import socket
import struct
from enum import Enum

ETH_P_ALL = 3
BUFFSIZE = 1518


class Protocolo(Enum):
    ARP = 0x0806
    IPV4 = 0x0800
    IPV6 = 0x86DD


def ler_ethernet(pacote):
    mac_destino, mac_origem, protocolo = struct.unpack('!6s 6s H', pacote[:14])
    pacote = pacote[15:]
    return mac_destino, mac_origem, protocolo


def ler_arp(pacote):
    operacao = struct.unpack('!H', pacote[6:8])
    return operacao


def main():
    sockd = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

    while True:
        pacote = sockd.recv(BUFFSIZE)
        mac_dest, mac_orig, protocolo = ler_ethernet(pacote)
        print('\nMAC Dest: ', ':'.join(format(x, '02x') for x in mac_dest))
        print('MAC Orig: ', ':'.join(format(x, '02x') for x in mac_orig))
        if protocolo == 0x0806:
            print('Tipo: ARP')
            operacao = ler_arp(pacote)
            print(operacao)
        elif protocolo == 0x0800:
            print('Tipo: IPv4')
        elif protocolo == 0x86DD:
            print('Tipo: IPv6')
        else:
            print('Pacote ignorado')
        print()


if __name__ == "__main__":
    main()
