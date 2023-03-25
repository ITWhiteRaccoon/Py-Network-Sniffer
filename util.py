import heapq
from collections import defaultdict
from operator import itemgetter
from rich.panel import Panel
from rich.tree import Tree
from rich.align import Align
from rich.text import Text


class Galho:
    def __init__(self, tree, text):
        self.tree = tree
        self.text = text


tam = {
    'min'    : -1,
    'max'    : -1,
    'med'    : -1,
    'valores': []
}

portas = {
    'tcp': defaultdict(int),
    'udp': defaultdict(int),
}

__tamanhos = [
    Panel(Align.center(str(tam['min'])), title=Text('Mínimo', 'yellow')),
    Panel(Align.center(str(tam['max'])), title=Text('Máximo', 'yellow')),
    Panel(Align.center(str(tam['med'])), title=Text('Médio', 'yellow'))
]

__arvore_portas = Tree('Portas')
__arvore_portas_tcp = __arvore_portas.add(Tree(Text('TCP', 'yellow')))
__arvore_portas_udp = __arvore_portas.add(Tree(Text('UDP', 'yellow')))

__arvore_pacotes = Tree('Pacotes - 0')
__arvore = {}
__arvore['arp'] = Galho(__arvore_pacotes.add(''), '[yellow]ARP[/yellow] - {0} ({1})')
__arvore['arp_req'] = Galho(__arvore['arp'].tree.add(''), '[yellow]Request[/yellow] - {0} ({1})')
__arvore['arp_rep'] = Galho(__arvore['arp'].tree.add(''), '[yellow]Reply[/yellow] - {0} ({1})')
__arvore['ipv4'] = Galho(__arvore_pacotes.add(''), '[yellow]IPv4[/yellow] - {0} ({1})')
__arvore['ipv4_icmp'] = Galho(__arvore['ipv4'].tree.add(''), '[yellow]ICMP[/yellow] - {0} ({1})')
__arvore['ipv4_icmp_echo_req'] = Galho(__arvore['ipv4_icmp'].tree.add(''), '[yellow]Echo Request[/yellow] - {0} ({1})')
__arvore['ipv4_icmp_echo_rep'] = Galho(__arvore['ipv4_icmp'].tree.add(''), '[yellow]Echo Reply[/yellow] - {0} ({1})')
__arvore['ipv4_tcp'] = Galho(__arvore['ipv4'].tree.add(''), '[yellow]TCP[/yellow] - {0} ({1})')
__arvore['ipv4_tcp_http'] = Galho(__arvore['ipv4_tcp'].tree.add(''), '[yellow]HTTP[/yellow] - {0} ({1})')
__arvore['ipv4_tcp_https'] = Galho(__arvore['ipv4_tcp'].tree.add(''), '[yellow]HTTPS[/yellow] - {0} ({1})')
__arvore['ipv4_tcp_dns'] = Galho(__arvore['ipv4_tcp'].tree.add(''), '[yellow]DNS[/yellow] - {0} ({1})')
__arvore['ipv4_udp'] = Galho(__arvore['ipv4'].tree.add(''), '[yellow]UDP[/yellow] - {0} ({1})')
__arvore['ipv4_udp_dns'] = Galho(__arvore['ipv4_udp'].tree.add(''), '[yellow]DNS[/yellow] - {0} ({1})')
__arvore['ipv4_udp_dhcp'] = Galho(__arvore['ipv4_udp'].tree.add(''), '[yellow]DHCP[/yellow] - {0} ({1})')
__arvore['ipv6'] = Galho(__arvore_pacotes.add(''), '[yellow]IPv6[/yellow] - {0} ({1})')
__arvore['ipv6_icmpv6'] = Galho(__arvore['ipv6'].tree.add(''), '[yellow]ICMPv6[/yellow] - {0} ({1})')
__arvore['ipv6_icmpv6_echo_req'] = Galho(__arvore['ipv6_icmpv6'].tree.add(''), '[yellow]Echo Request[/yellow] - {0} ({1})')
__arvore['ipv6_icmpv6_echo_rep'] = Galho(__arvore['ipv6_icmpv6'].tree.add(''), '[yellow]Echo Reply[/yellow] - {0} ({1})')
__arvore['ipv6_tcp'] = Galho(__arvore['ipv6'].tree.add(''), '[yellow]TCP[/yellow] - {0} ({1})')
__arvore['ipv6_tcp_http'] = Galho(__arvore['ipv6_tcp'].tree.add(''), '[yellow]HTTP[/yellow] - {0} ({1})')
__arvore['ipv6_tcp_https'] = Galho(__arvore['ipv6_tcp'].tree.add(''), '[yellow]HTTPS[/yellow] - {0} ({1})')
__arvore['ipv6_tcp_dns'] = Galho(__arvore['ipv6_tcp'].tree.add(''), '[yellow]DNS[/yellow] - {0} ({1})')
__arvore['ipv6_udp'] = Galho(__arvore['ipv6'].tree.add(''), '[yellow]UDP[/yellow] - {0} ({1})')
__arvore['ipv6_udp_dns'] = Galho(__arvore['ipv6_udp'].tree.add(''), '[yellow]DNS[/yellow] - {0} ({1})')
__arvore['ipv6_udp_dhcp'] = Galho(__arvore['ipv6_udp'].tree.add(''), '[yellow]DHCP[/yellow] - {0} ({1})')

qtd = {'pacotes': 0}
for galho in __arvore:
    qtd[galho] = 0


def porcentagem_de(num_a, num_b):
    try:
        return f'{num_a / num_b:.2%}'
    except ZeroDivisionError:
        return '0'


def atualizar_tamanhos():
    __tamanhos[0].renderable = Align.center(f"{tam['min']:.02f}")
    __tamanhos[1].renderable = Align.center(f"{tam['max']:.02f}")
    __tamanhos[2].renderable = Align.center(f"{tam['med']:.02f}")
    return __tamanhos


def atualizar_pacotes():
    __arvore_pacotes.label = f'Pacotes - {qtd["pacotes"]}'
    for galho in __arvore:
        __arvore[galho].tree.label = Text.from_markup(__arvore[galho].text.format(qtd[galho], porcentagem_de(qtd[galho], qtd['pacotes'])))
    return __arvore_pacotes


def atualizar_portas():
    __arvore_portas_tcp.children = []
    __arvore_portas_udp.children = []

    mais_acessados_tcp = heapq.nlargest(5, portas['tcp'].items(), key=itemgetter(1))
    mais_acessados_udp = heapq.nlargest(5, portas['udp'].items(), key=itemgetter(1))

    for entry in mais_acessados_tcp:
        __arvore_portas_tcp.add(Text.from_markup(f"Porta [yellow]'{entry[0]}'[/yellow] - {entry[1]} acessos"))
    for entry in mais_acessados_udp:
        __arvore_portas_udp.add(Text.from_markup(f"Porta [yellow]'{entry[0]}'[/yellow] - {entry[1]} acessos"))

    return __arvore_portas
