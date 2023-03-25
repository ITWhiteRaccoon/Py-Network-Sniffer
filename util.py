from collections import defaultdict
from rich.table import Table
from rich.tree import Tree


class Galho:
    def __init__(self, tree, text):
        self.tree = tree
        self.text = text


pacotes = Tree("Pacotes - 0")
arvore = {}
arvore['arp'] = Galho(pacotes.add("ARP - 0 (0%)"), 'ARP - {0} ({1})')
arvore['arp_req'] = Galho(arvore['arp'].tree.add("Request - 0 (0%)"), 'Request - {0} ({1})')
arvore['arp_rep'] = Galho(arvore['arp'].tree.add("Reply - 0 (0%)"), 'Reply - {0} ({1})')
arvore['ipv4'] = Galho(pacotes.add("IPv4 - 0 (0%)"), 'IPv4 - {0} ({1})')
arvore['ipv4_icmp'] = Galho(arvore['ipv4'].tree.add("ICMP - 0 (0%)"), 'ICMP - {0} ({1})')
arvore['ipv4_icmp_echo_req'] = Galho(arvore['ipv4_icmp'].tree.add("Echo Request - 0 (0%)"), 'Echo Request - {0} ({1})')
arvore['ipv4_icmp_echo_rep'] = Galho(arvore['ipv4_icmp'].tree.add("Echo Reply - 0 (0%)"), 'Echo Reply - {0} ({1})')
arvore['ipv4_tcp'] = Galho(arvore['ipv4'].tree.add("TCP - 0 (0%)"), 'TCP - {0} ({1})')
arvore['ipv4_tcp_http'] = Galho(arvore['ipv4_tcp'].tree.add("HTTP - 0 (0%)"), 'HTTP - {0} ({1})')
arvore['ipv4_tcp_https'] = Galho(arvore['ipv4_tcp'].tree.add("HTTPS - 0 (0%)"), 'HTTPS - {0} ({1})')
arvore['ipv4_tcp_dns'] = Galho(arvore['ipv4_tcp'].tree.add("DNS - 0 (0%)"), 'DNS - {0} ({1})')
arvore['ipv4_udp'] = Galho(arvore['ipv4'].tree.add("UDP - 0 (0%)"), 'UDP - {0} ({1})')
arvore['ipv4_udp_dns'] = Galho(arvore['ipv4_udp'].tree.add("DNS - 0 (0%)"), 'DNS - {0} ({1})')
arvore['ipv4_udp_dhcp'] = Galho(arvore['ipv4_udp'].tree.add("DHCP - 0 (0%)"), 'DHCP - {0} ({1})')
arvore['ipv6'] = Galho(pacotes.add("IPv6 - 0 (0%)"), 'IPv6 - {0} ({1})')
arvore['ipv6_icmp'] = Galho(arvore['ipv6'].tree.add("ICMPv6 - 0 (0%)"), 'ICMPv6 - {0} ({1})')
arvore['ipv6_icmp_echo_req'] = Galho(arvore['ipv6_icmp'].tree.add("Echo Request - 0 (0%)"), 'Echo Request - {0} ({1})')
arvore['ipv6_icmp_echo_rep'] = Galho(arvore['ipv6_icmp'].tree.add("Echo Reply - 0 (0%)"), 'Echo Reply - {0} ({1})')
arvore['ipv6_tcp'] = Galho(arvore['ipv6'].tree.add("TCP - 0 (0%)"), 'TCP - {0} ({1})')
arvore['ipv6_tcp_http'] = Galho(arvore['ipv6_tcp'].tree.add("HTTP - 0 (0%)"), 'HTTP - {0} ({1})')
arvore['ipv6_tcp_https'] = Galho(arvore['ipv6_tcp'].tree.add("HTTPS - 0 (0%)"), 'HTTPS - {0} ({1})')
arvore['ipv6_tcp_dns'] = Galho(arvore['ipv6_tcp'].tree.add("DNS - 0 (0%)"), 'DNS - {0} ({1})')
arvore['ipv6_udp'] = Galho(arvore['ipv6'].tree.add("UDP - 0 (0%)"), 'UDP - {0} ({1})')
arvore['ipv6_udp_dns'] = Galho(arvore['ipv6_udp'].tree.add("DNS - 0 (0%)"), 'DNS - {0} ({1})')
arvore['ipv6_udp_dhcp'] = Galho(arvore['ipv6_udp'].tree.add("DHCP - 0 (0%)"), 'DHCP - {0} ({1})')

tabela_tamanhos = Table("Min", "Max", "Média", title="Tamanho dos pacotes")

tam = {
    'min'    : -1,
    'max'    : -1,
    'med'    : -1,
    'valores': []
}
portas = {
    'tcp': defaultdict(int),
    'udp': defaultdict(int)
}


def porcentagem_de(num_a, num_b):
    try:
        return f"{num_a / num_b:.2%}"
    except ZeroDivisionError:
        return "0"


def atualizar_tabela():
    global tabela_tamanhos
    tabela_tamanhos = Table("Min", "Max", "Média", title="Tamanho dos pacotes")
    tabela_tamanhos.add_row(str(tam['min']), str(tam['max']), str(tam['med']))


def atualizar_arvore():
    pacotes.label = f"Pacotes - {qtd['pacotes']}"
    for galho in arvore:
        arvore[galho].tree.label = arvore[galho].text.format(qtd[galho], porcentagem_de(qtd[galho], qtd['pacotes']))
    # arp.label = f"ARP - {qtd['arp']} ({porcentagem_de(qtd['arp'], qtd['pacotes'])})"
    # arp_req.label = f"Request - {qtd['arp_req']} ({porcentagem_de(qtd['arp_req'], qtd['pacotes'])})"
    # arp_rep.label = f"Reply - {qtd['arp_rep']} ({porcentagem_de(qtd['arp_rep'], qtd['pacotes'])})"
    # ipv4.label = f"IPv4 - {qtd['ipv4']} ({porcentagem_de(qtd['ipv4'], qtd['pacotes'])})"
    # ipv4_icmp.label = f"ICMP - {qtd['ipv4_icmp']} ({porcentagem_de(qtd['ipv4_icmp'], qtd['pacotes'])})"
    # ipv4_icmp_echo_req.label = f"Echo Request - {qtd['ipv4_icmp_echo_req']} ({porcentagem_de(qtd['ipv4_icmp_echo_req'], qtd['pacotes'])})"
    # ipv4_icmp_echo_rep.label = f"Echo Reply - {qtd['ipv4_icmp_echo_rep']} ({porcentagem_de(qtd['ipv4_icmp_echo_rep'], qtd['pacotes'])})"
    # ipv4_tcp.label = f"TCP - {qtd['ipv4_tcp']} ({porcentagem_de(qtd['ipv4_tcp'], qtd['pacotes'])})"
    # ipv4_tcp_http.label = f"HTTP - {qtd['ipv4_tcp_http']} ({porcentagem_de(qtd['ipv4_tcp_http'], qtd['pacotes'])})"
    # ipv4_tcp_https.label = f"HTTPS - {qtd['ipv4_tcp_https']} ({porcentagem_de(qtd['ipv4_tcp_https'], qtd['pacotes'])})"
    # ipv4_tcp_dns.label = f"DNS - {qtd['ipv4_tcp_dns']} ({porcentagem_de(qtd['ipv4_tcp_dns'], qtd['pacotes'])})"
    # ipv4_udp.label = f"UDP - {qtd['ipv4_udp']} ({porcentagem_de(qtd['ipv4_udp'], qtd['pacotes'])})"
    # ipv4_udp_dns.label = f"DNS - {qtd['ipv4_udp_dns']} ({porcentagem_de(qtd['ipv4_udp_dns'], qtd['pacotes'])})"
    # ipv4_udp_dhcp.label = f"DHCP - {qtd['ipv4_udp_dhcp']} ({porcentagem_de(qtd['ipv4_udp_dhcp'], qtd['pacotes'])})"
    # ipv6.label = f"IPv6 - {qtd['ipv6']} ({porcentagem_de(qtd['ipv6'], qtd['pacotes'])})"
    # ipv6_icmp.label = f"ICMPv6 - {qtd['ipv6_icmp']} ({porcentagem_de(qtd['ipv6_icmp'], qtd['pacotes'])})"
    # ipv6_icmp_echo_req.label = f"Echo Request - {qtd['ipv6_icmp_echo_req']} ({porcentagem_de(qtd['ipv6_icmp_echo_req'], qtd['pacotes'])})"
    # ipv6_icmp_echo_rep.label = f"Echo Reply - {qtd['ipv6_icmp_echo_rep']} ({porcentagem_de(qtd['ipv6_icmp_echo_rep'], qtd['pacotes'])})"
    # ipv6_tcp.label = f"TCP - {qtd['ipv6_tcp']} ({porcentagem_de(qtd['ipv6_tcp'], qtd['pacotes'])})"
    # ipv6_tcp_http.label = f"HTTP - {qtd['ipv6_tcp_http']} ({porcentagem_de(qtd['ipv6_tcp_http'], qtd['pacotes'])})"
    # ipv6_tcp_https.label = f"HTTPS - {qtd['ipv6_tcp_https']} ({porcentagem_de(qtd['ipv6_tcp_https'], qtd['pacotes'])})"
    # ipv6_tcp_dns.label = f"DNS - {qtd['ipv6_tcp_dns']} ({porcentagem_de(qtd['ipv6_tcp_dns'], qtd['pacotes'])})"
    # ipv6_udp.label = f"UDP - {qtd['ipv6_udp']} ({porcentagem_de(qtd['ipv6_udp'], qtd['pacotes'])})"
    # ipv6_udp_dns.label = f"DNS - {qtd['ipv6_udp_dns']} ({porcentagem_de(qtd['ipv6_udp_dns'], qtd['pacotes'])})"
    # ipv6_udp_dhcp.label = f"DHCP - {qtd['ipv6_udp_dhcp']} ({porcentagem_de(qtd['ipv6_udp_dhcp'], qtd['pacotes'])})"


qtd = {
    'pacotes'           : 0,
    'arp'               : 0,
    'arp_req'           : 0,
    'arp_rep'           : 0,
    'ipv4'              : 0,
    'ipv4_icmp'         : 0,
    'ipv4_icmp_echo_req': 0,
    'ipv4_icmp_echo_rep': 0,
    'ipv4_tcp'          : 0,
    'ipv4_tcp_http'     : 0,
    'ipv4_tcp_https'    : 0,
    'ipv4_tcp_dns'      : 0,
    'ipv4_udp'          : 0,
    'ipv4_udp_dns'      : 0,
    'ipv4_udp_dhcp'     : 0,
    'ipv6'              : 0,
    'ipv6_icmp'         : 0,
    'ipv6_icmp_echo_req': 0,
    'ipv6_icmp_echo_rep': 0,
    'ipv6_tcp'          : 0,
    'ipv6_tcp_http'     : 0,
    'ipv6_tcp_https'    : 0,
    'ipv6_tcp_dns'      : 0,
    'ipv6_udp'          : 0,
    'ipv6_udp_dns'      : 0,
    'ipv6_udp_dhcp'     : 0,
}
