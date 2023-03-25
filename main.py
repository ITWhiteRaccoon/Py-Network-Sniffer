import socket
import struct
from enum import Enum

from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

from util import atualizar_arvore, atualizar_tabela, portas, tam, tabela_tamanhos, pacotes as arvore_pacotes, qtd

ETH_P_ALL = 3
BUFFSIZE = 1518


class ProtocoloEthernet(Enum):
    arp = 0x0806
    ipv4 = 0x0800
    ipv6 = 0x86DD


class ProtocoloIP(Enum):
    icmp = 1
    tcp = 6
    udp = 17
    icmpv6 = 58


class OperacaoARP(Enum):
    req = 1
    rep = 2


class TipoICMP(Enum):
    echo_rep = 0
    echo_req = 8


class TipoICMPv6(Enum):
    echo_req = 128
    echo_rep = 129


def ler_ethernet(pacote):
    mac_destino, mac_origem, protocolo = struct.unpack('!6s 6s H', pacote[:14])
    return pacote[14:], mac_destino, mac_origem, ProtocoloEthernet(protocolo)


def ler_arp(pacote):
    operacao, = struct.unpack('!H', pacote[6:8])
    return pacote, OperacaoARP(operacao)


def ler_ipv4(pacote):
    tamanho, = struct.unpack('!H', pacote[2:4])
    ttl, protocolo = struct.unpack('!BB', pacote[8:10])
    return pacote[24:], tamanho, ttl, ProtocoloIP(protocolo)


def ler_ipv6(pacote):
    protocolo, = struct.unpack('!B', pacote[6:7])
    return pacote[40:], ProtocoloIP(protocolo)


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
                nome_pacote = protocolo_eth.name
                qtd[nome_pacote] += 1

                match protocolo_eth:
                    case ProtocoloEthernet.arp:
                        pacote, operacao = ler_arp(pacote)
                        nome_pacote += f'_{operacao.name}'
                        qtd[nome_pacote] += 1

                    case ProtocoloEthernet.ipv4:
                        pacote, tamanho, ttl, protocolo_ip = ler_ipv4(pacote)
                        nome_pacote += f'_{protocolo_ip.name}'
                        qtd[nome_pacote] += 1

                        if protocolo_ip == ProtocoloIP.icmp:
                            pacote, tipo = ler_icmp(pacote)
                            nome_pacote += f'_{tipo.name}'
                            qtd[nome_pacote] += 1

                        else:
                            pacote, porta_orig, porta_dest = ler_portas_tcp_udp(pacote)
                            contar_tcp_udp(nome_pacote, porta_dest, porta_orig, protocolo_ip)

                    case ProtocoloEthernet.ipv6:
                        pacote, protocolo_ip = ler_ipv6(pacote)
                        nome_pacote += f'_{protocolo_ip}'
                        qtd[nome_pacote] += 1

                        if protocolo_ip == ProtocoloIP.icmpv6:
                            pacote, tipo = ler_icmpv6(pacote)
                            nome_pacote += f'_{tipo.name}'
                            qtd[nome_pacote] += 1

                        else:
                            pacote, porta_orig, porta_dest = ler_portas_tcp_udp(pacote)
                            contar_tcp_udp(nome_pacote, porta_dest, porta_orig, protocolo_ip)

                atualizar_arvore()
                atualizar_tabela()
                print()
            except ValueError:
                continue


def contar_tcp_udp(nome_pacote, porta_dest, porta_orig, protocolo_ip):
    portas[protocolo_ip.name][porta_dest] += 1
    if porta_dest == 53 or porta_orig == 53:
        qtd[f'{nome_pacote}_dns'] += 1
    elif porta_dest == 67 or porta_orig == 67 or porta_dest == 68 or porta_orig == 68:
        qtd[f'{nome_pacote}_dhcp'] += 1
    elif porta_dest == 80 or porta_orig == 80:
        qtd[f'{nome_pacote}_http'] += 1
    elif porta_dest == 443 or porta_orig == 443:
        qtd[f'{nome_pacote}_https'] += 1


if __name__ == "__main__":
    main()
