Topologi


ISP 

Interface GigabitEthernetg0/0/0
Ip = 192.168.12.1
Subnet mask = 255.255.255.0

Interface Loopback0
Ip = 172.16.0.1 
Subnet mask = 255.255.0.0

default route till Loopback0

ospf 1.1.1.1

ospf priority 0

network 192.168.12.0 0.0.0.255


STO 

Interface GigabitEthernetg0/0/0
Ip = 192.168.12.2
Subnet mask = 255.255.255.0

Interface Loopback0
Ip = 172.17.0.1 
Subnet mask = 255.255.0.0

ospf 2.2.2.2

ospf priority 255

network 192.168.12.0 0.0.0.255


GBG 

Interface GigabitEthernetg0/0/0
Ip = 192.168.12.3
Subnet mask = 255.255.255.0

Interface Loopback0
Ip = 172.18.0.1 
Subnet mask = 255.255.0.0

Interface GigabitEthernetg0/0/1
Ip = 12.12.12.13
Subnet mask = 255.255.255.252

ospf 3.3.3.3

network 192.168.12.0 0.0.0.255

network 12.12.12.0 0.0.0.3


