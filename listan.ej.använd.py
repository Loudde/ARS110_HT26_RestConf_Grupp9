


# 1. Topologi

devices = {
    "ISP": {
        "mgmt_ip": "11.11.11.1",
        "router_id": "1.1.1.1",
        "priority": 0, # aldrig dr/bdr

        "lan_interface": "GigabitEthernet0/0/0",
        "lan_ip": "192.168.12.1",
        "net_mask": "255.255.255.0",

        "loopback_interface": "Loopback0",
        "loopback_ip": "172.16.0.1",
        "loopback_netmask": "255.255.0.0",

        "ospf_networks": [
            ("192.168.12.0", "0.0.0.255"),
            ("172.16.0.0", "0.0.255.255"),
        ],
    },

    "STO":{
        "mgmt_ip": "11.11.11.2",
        "router_id": "2.2.2.2",
        "priority": 255, #för att bli dr

        "lan_interface": "GigabitEthernet0/0/0",
        "lan_ip": "192.168.12.2",
        "net_mask": "255.255.255.0",

        "loopback_interface": "Loopback0",
        "loopback_ip": "172.17.0.1",
        "loopback_netmask": "255.255.0.0",

        "ospf_networks": [
            ("192.168.12.0", "0.0.0.255"),
            ("172.17.0.0", "0.0.255.255"),
        ],
    },

    "GBG":{
        "mgmt_ip": "11.11.11.3",
        "router_id": "3.3.3.3",
        "priority": 1, #för bdr

        "lan_interface": "GigabitEthernet0/0/0",
        "lan_ip": "192.168.12.3",
        "net_mask": "255.255.255.0",

        "loopback_interface": "Loopback0",
        "loopback_ip": "172.18.0.1",
        "loopback_netmask": "255.255.0.0",

        "pc_interface": "GigabitEthernet0/0/1",
        "pc_ip": "12.12.12.13",
        "pc_netmask": "255.255.255.252",
        "pc_cost": 14,

        "ospf_networks": [
            ("192.168.12.0", "0.0.0.255"),
            ("12.12.12.12", "0.0.0.3"),
            ("172.18.0.0", "0.0.255.255"),
        ],
    },
}