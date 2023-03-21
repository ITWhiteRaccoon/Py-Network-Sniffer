import socket
import struct
from enum import Enum

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.align import Align

from arvores import atualizar_arvore, atualizar_tabela, portas, tam, tabela_tamanhos, pacotes as arvore_pacotes
from quantidade import quantidades as qtd

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

    layout = Layout()
    layout.split_column(
        Layout(Panel(Align.center(tabela_tamanhos)), name="tamanhos", ratio=1, minimum_size=6),
        Layout(Panel(Align.center(arvore_pacotes)), name="pacotes", ratio=3),
    )

    with Live(layout, refresh_per_second=1):
        while True:
            try:
                pacote = sockd.recv(BUFFSIZE)
                qtd['pacotes'] += 1

                tam_pacote = len(pacote) / 8 if len(pacote) > 0 else len(pacote)
                tam['valores'].append(tam_pacote)
                tam['med'] = sum(tam['valores']) / len(tam['valores'])
                if tam['min'] == -1 or tam_pacote < tam['min']:
                    tam['min'] = tam_pacote
                if tam['max'] == -1 or tam_pacote > tam['max']:
                    tam['max'] = tam_pacote

                pacote, _, _, protocolo_eth = ler_ethernet(pacote)
                match protocolo_eth:
                    case ProtocoloEthernet.ARP:
                        qtd['arp'] += 1
                        pacote, operacao = ler_arp(pacote)
                        if operacao == OperacaoARP.Request:
                            qtd['arp_req'] += 1
                        elif operacao == OperacaoARP.Reply:
                            qtd['arp_rep'] += 1
                    case ProtocoloEthernet.IPV4:
                        qtd['ipv4'] += 1
                        pacote, tamanho, ttl, protocolo_ipv4 = ler_ipv4(pacote)
                        if protocolo_ipv4 == ProtocoloIPv4.ICMP:
                            qtd['ipv4_icmp'] += 1
                            pacote, tipo = ler_icmp(pacote)
                            if tipo == TipoICMP.EchoReply:
                                qtd['ipv4_icmp_echo_req'] += 1
                            elif tipo == TipoICMP.EchoRequest:
                                qtd['ipv4_icmp_echo_req'] += 1
                        else:
                            pacote, porta_orig, porta_dest = ler_portas_tcp_udp(pacote)
                            if protocolo_ipv4 == ProtocoloIPv4.TCP:
                                qtd['ipv4_tcp'] += 1
                                portas['tcp'][porta_dest] += 1
                                if porta_dest == 80 or porta_orig == 80:
                                    qtd['ipv4_tcp_http'] += 1
                                if porta_dest == 443 or porta_orig == 443:
                                    qtd['ipv4_tcp_https'] += 1
                                if porta_dest == 53 or porta_orig == 53:
                                    qtd['ipv4_tcp_dns'] += 1
                            if protocolo_ipv4 == ProtocoloIPv4.UDP:
                                qtd['ipv4_udp'] += 1
                                portas['udp'][porta_dest] += 1
                                if porta_dest == 53 or porta_orig == 53:
                                    qtd['ipv4_udp_dns'] += 1
                                if porta_dest == 67 or porta_orig == 67 or porta_dest == 68 or porta_orig == 68:
                                    qtd['ipv4_udp_dhcp'] += 1

                    case ProtocoloEthernet.IPV6:
                        qtd['ipv6'] += 1
                        pacote, protocolo_ipv6 = ler_ipv6(pacote)
                        if protocolo_ipv6 == ProtocoloIPv6.ICMPv6:
                            qtd['ipv6_icmp'] += 1
                            pacote, tipo = ler_icmpv6(pacote)

                        else:
                            pacote, porta_orig, porta_dest = ler_portas_tcp_udp(pacote)
                            if protocolo_ipv6 == ProtocoloIPv6.TCP:
                                qtd['ipv6_tcp'] += 1
                                portas['tcp'][porta_dest] += 1
                                if porta_dest == 80 or porta_orig == 80:
                                    qtd['ipv6_tcp_http'] += 1
                                if porta_dest == 443 or porta_orig == 443:
                                    qtd['ipv6_tcp_https'] += 1
                                if porta_dest == 53 or porta_orig == 53:
                                    qtd['ipv6_tcp_dns'] += 1
                            if protocolo_ipv6 == ProtocoloIPv6.UDP:
                                qtd['ipv6_udp'] += 1
                                portas['udp'][porta_dest] += 1
                                if porta_dest == 53 or porta_orig == 53:
                                    qtd['ipv6_udp_dns'] += 1
                                if porta_dest == 67 or porta_orig == 67 or porta_dest == 68 or porta_orig == 68:
                                    qtd['ipv6_udp_dhcp'] += 1

                atualizar_arvore()
                atualizar_tabela()
                print()
            except ValueError:
                continue


if __name__ == "__main__":
    main()
