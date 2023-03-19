import socket
import struct
from enum import Enum
from rich.live import Live
from rich.table import Table
from rich.layout import Layout

ETH_P_ALL = 3
BUFFSIZE = 1518


class ProtocoloEthernet(Enum):
    ARP = 0x0806
    IPV4 = 0x0800
    IPV6 = 0x86DD


class ProtocoloIPv4(Enum):
    ICMP = 1
    TCP = 6
    UDP = 17


class ProtocoloIPv6(Enum):
    TCP = 6
    UDP = 17
    ICMPv6 = 58


class OperacaoARP(Enum):
    Request = 1
    Reply = 2


class TipoICMP(Enum):
    EchoReply = 0
    EchoRequest = 8


class TipoICMPv6(Enum):
    EchoRequest = 128
    EchoReply = 129


def ler_ethernet(pacote):
    mac_destino, mac_origem, protocolo = struct.unpack('!6s 6s H', pacote[:14])
    return pacote[14:], mac_destino, mac_origem, ProtocoloEthernet(protocolo)


def ler_arp(pacote):
    operacao, = struct.unpack('!H', pacote[6:8])
    return pacote, OperacaoARP(operacao)


def ler_ipv4(pacote):
    tamanho, = struct.unpack('!H', pacote[2:4])
    ttl, protocolo = struct.unpack('!BB', pacote[8:10])
    return pacote[24:], tamanho, ttl, ProtocoloIPv4(protocolo)


def ler_ipv6(pacote):
    protocolo, = struct.unpack('!B', pacote[6:7])
    return pacote[40:], ProtocoloIPv6(protocolo)


def ler_icmp(pacote):
    tipo, = struct.unpack('!B', pacote[:1])
    return pacote, TipoICMP(tipo)


def ler_icmpv6(pacote):
    tipo, = struct.unpack('!B', pacote[:1])
    return pacote, TipoICMPv6(tipo)


def ler_portas_tcp_udp(pacote):
    porta_orig, porta_dest = struct.unpack('!HH', pacote[:4])
    return pacote, porta_orig, porta_dest


def main():
    sockd = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))

    tabela_tamanhos = Table("Min", "Max", "Media", title="Tamanho dos pacotes")
    tabela_rede = Table("Protocolo", "Porcentagem", "Quantidade", title="Nível de Rede")
    tabela_transporte = Table("Protocolo", "Porcentagem", "Quantidade", title="Nível de Transporte")
    tabela_aplicacao = Table("Protocolo", "Porcentagem", "Quantidade", title="Nível de Aplicacao")

    layout = Layout()
    layout.split_column(
        Layout(tabela_tamanhos, name="tamanhos", minimum_size=6),
        Layout(tabela_rede, name="rede", ratio=2),
        Layout(tabela_transporte, name="transporte", ratio=2),
        Layout(tabela_aplicacao, name="aplicacao", ratio=2)
    )

    with Live(layout, refresh_per_second=1):
        while True:
            try:
                pacote = sockd.recv(BUFFSIZE)
                pacote, mac_dest, mac_orig, protocolo_eth = ler_ethernet(pacote)
                print('\nMAC Dest: ', ':'.join(format(x, '02x') for x in mac_dest))
                print('MAC Orig: ', ':'.join(format(x, '02x') for x in mac_orig))
                match protocolo_eth:
                    case ProtocoloEthernet.ARP:
                        print('Tipo: ARP')
                        pacote, operacao = ler_arp(pacote)
                        print('ARP ', operacao.name)
                    case ProtocoloEthernet.IPV4:
                        print('Tipo: IPv4')
                        pacote, tamanho, ttl, protocolo_ipv4 = ler_ipv4(pacote)
                        print('IPv4 ', protocolo_ipv4.name)
                        print('TTL ', ttl)
                        print(tamanho, ' bytes')
                        if protocolo_ipv4 == ProtocoloIPv4.ICMP:
                            pacote, tipo = ler_icmp(pacote)
                            print(tipo.name)
                        elif protocolo_ipv4 == ProtocoloIPv4.TCP or protocolo_ipv4 == ProtocoloIPv4.UDP:
                            pacote, porta_orig, porta_dest = ler_portas_tcp_udp(pacote)
                            print('Porta origem: ', porta_orig)
                            print('Porta destino: ', porta_dest)
                    case ProtocoloEthernet.IPV6:
                        print('Tipo: IPv6')
                        pacote, protocolo_ipv6 = ler_ipv6(pacote)
                        if protocolo_ipv6 == ProtocoloIPv6.ICMPv6:
                            pacote, tipo = ler_icmpv6(pacote)
                            print(tipo.name)
                        elif protocolo_ipv6 == ProtocoloIPv6.TCP or protocolo_ipv6 == ProtocoloIPv6.UDP:
                            pacote, porta_orig, porta_dest = ler_portas_tcp_udp(pacote)
                            print('Porta origem: ', porta_orig)
                            print('Porta destino: ', porta_dest)
                    case _:
                        print('Pacote ignorado')
                print()
            except ValueError:
                continue


if __name__ == "__main__":
    main()
