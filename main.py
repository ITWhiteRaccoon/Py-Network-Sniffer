import socket
import struct
from enum import Enum

ETH_P_ALL = 3
BUFFSIZE = 1518


class ProtocoloEthernet(Enum):
    ARP = 0x0806
    IPV4 = 0x0800
    IPV6 = 0x86DD


class ProtocoloIPv4(Enum):
    ICMP = 1
    IGMP = 2
    TCP = 6
    IGRP = 9
    UDP = 17
    GRE = 47
    ESP = 50
    AH = 51
    SKIP = 57
    EIGRP = 88
    OSPF = 89
    L2TP = 115


class OperacaoARP(Enum):
    Request = 1
    Reply = 2


def ler_ethernet(pacote):
    mac_destino, mac_origem, protocolo = struct.unpack('!6s 6s H', pacote[:14])
    return mac_destino, mac_origem, protocolo, pacote[14:]


def ler_arp(pacote):
    operacao, = struct.unpack('!H', pacote[6:8])
    return operacao


def ler_ipv4(pacote):
    tamanho, = struct.unpack('!H', pacote[2:4])
    ttl, protocolo = struct.unpack('!BB', pacote[8:10])
    return tamanho, ttl, protocolo


def main():
    sockd = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

    while True:
        pacote = sockd.recv(BUFFSIZE)
        mac_dest, mac_orig, protocolo_eth, pacote = ler_ethernet(pacote)
        print('\nMAC Dest: ', ':'.join(format(x, '02x') for x in mac_dest))
        print('MAC Orig: ', ':'.join(format(x, '02x') for x in mac_orig))
        match ProtocoloEthernet(protocolo_eth):
            case ProtocoloEthernet.ARP:
                print('Tipo: ARP')
                operacao = OperacaoARP(ler_arp(pacote))
                print('ARP ', operacao.name)
            case ProtocoloEthernet.IPV4:
                print('Tipo: IPv4')
                tamanho, ttl, protocolo_ipv4 = ler_ipv4(pacote)
                print('IPv4 ', ProtocoloIPv4(protocolo_ipv4).name)
                print('TTL ', ttl)
                print(tamanho, ' bytes')
            case ProtocoloEthernet.IPV6:
                print('Tipo: IPv6')
            case _:
                print('Pacote ignorado')
        print()


if __name__ == "__main__":
    main()
