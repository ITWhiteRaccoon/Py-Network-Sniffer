from rich.tree import Tree
from rich.table import Table
from collections import defaultdict

from quantidade import quantidades as qtd

pacotes = Tree("Pacotes - 0")
arp = pacotes.add("ARP - 0 (0%)")
arp_req = arp.add("Request - 0 (0%)")
arp_rep = arp.add("Reply - 0 (0%)")
ipv4 = pacotes.add("IPv4 - 0 (0%)")
ipv4_icmp = ipv4.add("ICMP - 0 (0%)")
ipv4_icmp_echo_req = ipv4_icmp.add("Echo Request - 0 (0%)")
ipv4_icmp_echo_rep = ipv4_icmp.add("Echo Reply - 0 (0%)")
ipv4_tcp = ipv4.add("TCP - 0 (0%)")
ipv4_tcp_http = ipv4_tcp.add("HTTP - 0 (0%)")
ipv4_tcp_https = ipv4_tcp.add("HTTPS - 0 (0%)")
ipv4_tcp_dns = ipv4_tcp.add("DNS - 0 (0%)")
ipv4_udp = ipv4.add("UDP - 0 (0%)")
ipv4_udp_dns = ipv4_udp.add("DNS - 0 (0%)")
ipv4_udp_dhcp = ipv4_udp.add("DHCP - 0 (0%)")
ipv6 = pacotes.add("IPv6 - 0 (0%)")
ipv6_icmp = ipv6.add("ICMPv6 - 0 (0%)")
ipv6_icmp_echo_req = ipv6_icmp.add("Echo Request - 0 (0%)")
ipv6_icmp_echo_rep = ipv6_icmp.add("Echo Reply - 0 (0%)")
ipv6_tcp = ipv6.add("TCP - 0 (0%)")
ipv6_tcp_http = ipv6_tcp.add("HTTP - 0 (0%)")
ipv6_tcp_https = ipv6_tcp.add("HTTPS - 0 (0%)")
ipv6_tcp_dns = ipv6_tcp.add("DNS - 0 (0%)")
ipv6_udp = ipv6.add("UDP - 0 (0%)")
ipv6_udp_dns = ipv6_udp.add("DNS - 0 (0%)")
ipv6_udp_dhcp = ipv6_udp.add("DHCP - 0 (0%)")

tabela_tamanhos = Table("Min", "Max", "Média", title="Tamanho dos pacotes")

tam = {
    'min': -1,
    'max': -1,
    'med': -1,
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
    arp.label = f"ARP - {qtd['arp']} ({porcentagem_de(qtd['arp'], qtd['pacotes'])})"
    arp_req.label = f"Request - {qtd['arp_req']} ({porcentagem_de(qtd['arp_req'], qtd['pacotes'])})"
    arp_rep.label = f"Reply - {qtd['arp_rep']} ({porcentagem_de(qtd['arp_rep'], qtd['pacotes'])})"
    ipv4.label = f"IPv4 - {qtd['ipv4']} ({porcentagem_de(qtd['ipv4'], qtd['pacotes'])})"
    ipv4_icmp.label = f"ICMP - {qtd['ipv4_icmp']} ({porcentagem_de(qtd['ipv4_icmp'], qtd['pacotes'])})"
    ipv4_icmp_echo_req.label = f"Echo Request - {qtd['ipv4_icmp_echo_req']} ({porcentagem_de(qtd['ipv4_icmp_echo_req'], qtd['pacotes'])})"
    ipv4_icmp_echo_rep.label = f"Echo Reply - {qtd['ipv4_icmp_echo_rep']} ({porcentagem_de(qtd['ipv4_icmp_echo_rep'], qtd['pacotes'])})"
    ipv4_tcp.label = f"TCP - {qtd['ipv4_tcp']} ({porcentagem_de(qtd['ipv4_tcp'], qtd['pacotes'])})"
    ipv4_tcp_http.label = f"HTTP - {qtd['ipv4_tcp_http']} ({porcentagem_de(qtd['ipv4_tcp_http'], qtd['pacotes'])})"
    ipv4_tcp_https.label = f"HTTPS - {qtd['ipv4_tcp_https']} ({porcentagem_de(qtd['ipv4_tcp_https'], qtd['pacotes'])})"
    ipv4_tcp_dns.label = f"DNS - {qtd['ipv4_tcp_dns']} ({porcentagem_de(qtd['ipv4_tcp_dns'], qtd['pacotes'])})"
    ipv4_udp.label = f"UDP - {qtd['ipv4_udp']} ({porcentagem_de(qtd['ipv4_udp'], qtd['pacotes'])})"
    ipv4_udp_dns.label = f"DNS - {qtd['ipv4_udp_dns']} ({porcentagem_de(qtd['ipv4_udp_dns'], qtd['pacotes'])})"
    ipv4_udp_dhcp.label = f"DHCP - {qtd['ipv4_udp_dhcp']} ({porcentagem_de(qtd['ipv4_udp_dhcp'], qtd['pacotes'])})"
    ipv6.label = f"IPv6 - {qtd['ipv6']} ({porcentagem_de(qtd['ipv6'], qtd['pacotes'])})"
    ipv6_icmp.label = f"ICMPv6 - {qtd['ipv6_icmp']} ({porcentagem_de(qtd['ipv6_icmp'], qtd['pacotes'])})"
    ipv6_icmp_echo_req.label = f"Echo Request - {qtd['ipv6_icmp_echo_req']} ({porcentagem_de(qtd['ipv6_icmp_echo_req'], qtd['pacotes'])})"
    ipv6_icmp_echo_rep.label = f"Echo Reply - {qtd['ipv6_icmp_echo_rep']} ({porcentagem_de(qtd['ipv6_icmp_echo_rep'], qtd['pacotes'])})"
    ipv6_tcp.label = f"TCP - {qtd['ipv6_tcp']} ({porcentagem_de(qtd['ipv6_tcp'], qtd['pacotes'])})"
    ipv6_tcp_http.label = f"HTTP - {qtd['ipv6_tcp_http']} ({porcentagem_de(qtd['ipv6_tcp_http'], qtd['pacotes'])})"
    ipv6_tcp_https.label = f"HTTPS - {qtd['ipv6_tcp_https']} ({porcentagem_de(qtd['ipv6_tcp_https'], qtd['pacotes'])})"
    ipv6_tcp_dns.label = f"DNS - {qtd['ipv6_tcp_dns']} ({porcentagem_de(qtd['ipv6_tcp_dns'], qtd['pacotes'])})"
    ipv6_udp.label = f"UDP - {qtd['ipv6_udp']} ({porcentagem_de(qtd['ipv6_udp'], qtd['pacotes'])})"
    ipv6_udp_dns.label = f"DNS - {qtd['ipv6_udp_dns']} ({porcentagem_de(qtd['ipv6_udp_dns'], qtd['pacotes'])})"
    ipv6_udp_dhcp.label = f"DHCP - {qtd['ipv6_udp_dhcp']} ({porcentagem_de(qtd['ipv6_udp_dhcp'], qtd['pacotes'])})"
