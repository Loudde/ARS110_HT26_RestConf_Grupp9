


# 1. Topologi

devices = {
    "ISP": {
        "mgmt_ip": "11.11.11.1",

        "lan_interface": "GigabitEthernet0/0/0",

        "lan_ip": "192.168.1.1",
        "net_mask": "255.255.255.0"

        "loopback_interface": "loopback0",
        "loopback_ip": "172.16.0.1",
        "loopback_netmask": "255.255.0.0",





    "STO":{
        "mgmt_ip": "11.11.11.2",

        "lan_interface": "GigabitEthernet0/0/0",

        "lan_ip": "192.168.12.2",
        "net_mask": "255.255.255.0"

        "loopback_interface": "loopback0",
        "loopback_ip": "172.17.0.1",
        "loopback_netmask": "255.255.0.0",

    "GBG":{
        "mgmt_ip": "11.11.11.3",

         "lan_interface": "GigabitEthernet0/0/0",
    
        "lan_ip": "192.168.12.3",
        "net_mask": "255.255.255.0",

        "loopback_interface": "loopback0",
        "loopback_ip": "172.18.0.1",
        "loopback_netmask": "255.255.0.0",

        "pc_interface": "GigabitEthernet0/0/1",
        "pc_ip": "12.12.12.13",
        "pc_netmask": "255.255.255.252",
}