from rich.tree import Tree

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
ipv4_tcp_tls = ipv4_tcp.add("TLS - 0 (0%)")
ipv4_udp = ipv4.add("UDP - 0 (0%)")
ipv4_udp_dns = ipv4_udp.add("DNS - 0 (0%)")
ipv4_udp_dhcp = ipv4_udp.add("DHCP - 0 (0%)")
ipv6 = pacotes.add("IPv6 - 0 (0%)")
ipv6_icmp = ipv6.add("ICMPv6 - 0 (0%)")
ipv6_icmp_echo_req = ipv6_icmp.add("Echo Request - 0 (0%)")
ipv6_icmp_echo_rep = ipv6_icmp.add("Echo Reply - 0 (0%)")
ipv6_tcp = ipv6.add("TCP - 0 (0%)")
ipv6_tcp_http = ipv6_tcp.add("HTTP - 0 (0%)")
ipv6_tcp_tls = ipv6_tcp.add("TLS - 0 (0%)")
ipv6_udp = ipv6.add("UDP - 0 (0%)")


def porcentagem_de(num_a, num_b):
    try:
        return f"{num_a / num_b:.2%}"
    except ZeroDivisionError:
        return "0"


def raiz():
    return pacotes


def atualizar_arvore():
    pacotes.label = f"Pacotes - {qtd['pacotes']}"
    arp.label = f"ARP - {qtd['arp']} ({porcentagem_de(qtd['arp'], qtd['pacotes'])})"
    arp_req.label = f"Request - {qtd['arp_req']} ({porcentagem_de(qtd['arp_req'], qtd['arp'])})"
    arp_rep.label = f"Reply - {qtd['arp_rep']} ({porcentagem_de(qtd['arp_rep'], qtd['arp'])})"
    ipv4.label = f"IPv4 - {qtd['ipv4']} ({porcentagem_de(qtd['ipv4'], qtd['pacotes'])})"
    ipv4_icmp.label = f"ICMP - {qtd['ipv4_icmp']} ({porcentagem_de(qtd['ipv4_icmp'], qtd['ipv4'])})"
    ipv4_icmp_echo_req.label = f"Echo Request - {qtd['ipv4_icmp_echo_req']} ({porcentagem_de(qtd['ipv4_icmp_echo_req'], qtd['ipv4_icmp'])})"
    ipv4_icmp_echo_rep.label = f"Echo Reply - {qtd['ipv4_icmp_echo_rep']} ({porcentagem_de(qtd['ipv4_icmp_echo_rep'], qtd['ipv4_icmp'])})"
    ipv4_tcp.label = f"TCP - {qtd['ipv4_tcp']} ({porcentagem_de(qtd['ipv4_tcp'], qtd['ipv4'])})"
    ipv4_tcp_http.label = f"HTTP - {qtd['ipv4_tcp_http']} ({porcentagem_de(qtd['ipv4_tcp_http'], qtd['ipv4_tcp'])})"
    ipv4_tcp_tls.label = f"TLS - {qtd['ipv4_tcp_tls']} ({porcentagem_de(qtd['ipv4_tcp_tls'], qtd['ipv4_tcp'])})"
    ipv4_udp.label = f"UDP - {qtd['ipv4_udp']} ({porcentagem_de(qtd['ipv4_udp'], qtd['ipv4'])})"
    ipv4_udp_dns.label = f"DNS - {qtd['ipv4_udp_dns']} ({porcentagem_de(qtd['ipv4_udp_dns'], qtd['ipv4_udp'])})"
    ipv4_udp_dhcp.label = f"DHCP - {qtd['ipv4_udp_dhcp']} ({porcentagem_de(qtd['ipv4_udp_dhcp'], qtd['ipv4_udp'])})"
    ipv6.label = f"IPv6 - {qtd['ipv6']} ({porcentagem_de(qtd['ipv6'], qtd['pacotes'])})"
    ipv6_icmp.label = f"ICMPv6 - {qtd['ipv6_icmp']} ({porcentagem_de(qtd['ipv6_icmp'], qtd['ipv6'])})"
    ipv6_icmp_echo_req.label = f"Echo Request - {qtd['ipv6_icmp_echo_req']} ({porcentagem_de(qtd['ipv6_icmp_echo_req'], qtd['ipv6_icmp'])})"
    ipv6_icmp_echo_rep.label = f"Echo Reply - {qtd['ipv6_icmp_echo_rep']} ({porcentagem_de(qtd['ipv6_icmp_echo_rep'], qtd['ipv6_icmp'])})"
    ipv6_tcp.label = f"TCP - {qtd['ipv6_tcp']} ({porcentagem_de(qtd['ipv6_tcp'], qtd['ipv6'])})"
    ipv6_tcp_http.label = f"HTTP - {qtd['ipv6_tcp_http']} ({porcentagem_de(qtd['ipv6_tcp_http'], qtd['ipv6_tcp'])})"
    ipv6_tcp_tls.label = f"TLS - {qtd['ipv6_tcp_tls']} ({porcentagem_de(qtd['ipv6_tcp_tls'], qtd['ipv6_tcp'])})"
    ipv6_udp.label = f"UDP - {qtd['ipv6_udp']} ({porcentagem_de(qtd['ipv6_udp'], qtd['ipv6'])})"
