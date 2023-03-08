#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/if_ether.h>
#include <net/if.h>
#include <linux/filter.h>
#include <sys/ioctl.h>
#include <string.h>
#include <sys/time.h>
#include <signal.h>

/* tamanho máximo de um datagrama IP*/
#define PCKT_LEN 1518

struct arp_packet {
	uint16_t hw_type;
	uint16_t prot_type;
	uint8_t hlen;
	uint8_t dlen;
	uint16_t operation;
	uint8_t sender_hwaddr[6];
	uint8_t sender_ip[4];
	uint8_t target_hwaddr[6];
	uint8_t target_ip[4];
};

union arp_packet_u {
	struct arp_packet arp;
	uint8_t raw_data[sizeof(struct arp_packet)];
};

int main(int argc, char **argv){
	int fd;
	struct ifreq ethreq;
	int size;
	unsigned char buffer[PCKT_LEN];
	union arp_packet_u arp_message;
	
	/* Cria o Socket Raw */
	if ((fd = socket (PF_PACKET, SOCK_RAW, htons(ETH_P_ALL))) < 0){
		perror("socket:");
		return -1;
	}
	
	/* Coloca o adaptador de rede em modo promíscuo */
	if (argc > 1){
		strncpy(ethreq.ifr_name, argv[1], IFNAMSIZ);
	}else{
		strncpy(ethreq.ifr_name, "eth0", IFNAMSIZ);
	}
	if (ioctl(fd,SIOCGIFFLAGS, &ethreq) == -1) {
		perror("ioctl");
		close(fd);
		exit(-1);
	}
	
	ethreq.ifr_flags |= IFF_PROMISC;
	if (ioctl(fd, SIOCSIFFLAGS, &ethreq) == -1) {
		perror("ioctl");
		close(fd);
		exit(-1);
	}


	while ((size = read (fd, buffer, PCKT_LEN)) > 0){
		if (((buffer[12] << 8) | buffer[13]) == 0x0806){
			memcpy(arp_message.raw_data, buffer + 14, sizeof(struct arp_packet));
			printf("\nhw type:		%04x", ntohs(arp_message.arp.hw_type));
			printf("\nl3 protocol:		%04x", ntohs(arp_message.arp.prot_type));
			printf("\nhlen:			%02x", arp_message.arp.hlen);
			printf("\ndlen:			%02x", arp_message.arp.dlen);
			printf("\noperation:		%02x", arp_message.arp.operation);
			printf("\nsender MAC:		%02x:%02x:%02x:%02x:%02x:%02x", arp_message.arp.sender_hwaddr[0], arp_message.arp.sender_hwaddr[1],
											arp_message.arp.sender_hwaddr[2], arp_message.arp.sender_hwaddr[3],
											arp_message.arp.sender_hwaddr[4], arp_message.arp.sender_hwaddr[5]);
			printf("\nsender IP:		%d.%d.%d.%d",	arp_message.arp.sender_ip[0], arp_message.arp.sender_ip[1],
									arp_message.arp.sender_ip[2], arp_message.arp.sender_ip[3]);
			printf("\ntarget MAC:		%02x:%02x:%02x:%02x:%02x:%02x",	arp_message.arp.target_hwaddr[0], arp_message.arp.target_hwaddr[1],
											arp_message.arp.target_hwaddr[2], arp_message.arp.target_hwaddr[3],
											arp_message.arp.target_hwaddr[4], arp_message.arp.target_hwaddr[5]);
			printf("\ntarget IP:		%d.%d.%d.%d\n",	arp_message.arp.target_ip[0], arp_message.arp.target_ip[1],
									arp_message.arp.target_ip[2], arp_message.arp.target_ip[3]);
		}
	}

	return 0;
}
