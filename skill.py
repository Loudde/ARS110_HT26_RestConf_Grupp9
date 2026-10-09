import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
  "Content-Type": "application/yang-data+json",
  "Accept": "application/yang-data+json"
}

#Confa Hostnames

def hostname_enhet(mgmt_ip, hostname):

    url = f"https://{mgmt_ip}/restconf/data/Cisco-IOS-XE-native:native/hostname"

    payload = {
        "Cisco-IOS-XE-native:hostname": hostname
    }

    response = requests.patch(url, headers=headers, auth=("admin","class"),json=payload, verify=False)

    print(response.status_code, response.text)

hostname_enhet("10.10.10.1", "ISP")
hostname_enhet("10.10.10.2", "STO")
hostname_enhet("10.10.10.3", "GBG")                              






#Funktion för skapandet av loopbacks
def skapa_loopback(mgmt_ip, loopback_namn, loopback_ip, nätmask):

    url = f"https://{mgmt_ip}/restconf/data/ietf-interfaces:interfaces"
        
    payload = {
        "ietf-interfaces:interface": {
            "name": loopback_namn,
            "description": "CONFAD MED RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": loopback_ip,
                        "netmask": nätmask
                    }
                ]
            }
          
        }
    }


    response = requests.post(url, headers=headers, auth=("admin","class"),json=payload, verify=False)

    print(response.status_code)


#Skapa loopbacks genom funktion
skapa_loopback("10.10.10.1", "Loopback0", "172.16.0.1", "255.255.0.0")
skapa_loopback("10.10.10.2", "Loopback0", "172.17.0.1", "255.255.0.0")
skapa_loopback("10.10.10.3", "Loopback0", "172.18.0.1", "255.255.0.0")

#Funktion för att confa ip addresser
def conf_interface(mgmt_ip, interface_namn, ip_address, nätmask):

    interface_namn_url = interface_namn.replace("/", "%2F")
    
    url = f"https://{mgmt_ip}/restconf/data/ietf-interfaces:interfaces/interface={interface_namn_url}"

    payload = {
    "ietf-interfaces:interface": {
        "name": interface_namn,
        "description": "CONFAD MED RESTCONF",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": ip_address,
                    "netmask": nätmask
                }
            ]
        },

    }
}
    response = requests.patch(url, headers=headers, auth=("admin","class"),json=payload, verify=False)

    print(response.status_code, response.text)
        
conf_interface("10.10.10.1", "GigabitEthernet0/0/0", "192.168.12.1", "255.255.255.0")
conf_interface("10.10.10.2", "GigabitEthernet0/0/0", "192.168.12.2", "255.255.255.0")
conf_interface("10.10.10.3", "GigabitEthernet0/0/0", "192.168.12.3", "255.255.255.0")
conf_interface("10.10.10.3", "GigabitEthernet0/0/1", "12.12.12.13", "255.255.255.252")



#Funktionen för att sätta prioritet
    
def ospf_prioritet(mgmt_ip, interface_nummer, inställning, värde):

    nummer = interface_nummer.replace("/", "%2F")
    url = f"https://{mgmt_ip}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={nummer}/ip"

    payload = {
        "Cisco-IOS-XE-native:ip": {
            "Cisco-IOS-XE-ospf:router-ospf": {
                "ospf": {inställning: värde}
            }
        }
    }

    response = requests.patch(url, headers=headers, auth=("admin","class"), json=payload, verify=False)
    print(response.status_code, response.text)

ospf_prioritet("10.10.10.1", "0/0/0", "priority" , 0)
ospf_prioritet("10.10.10.2", "0/0/0", "priority" , 255)
ospf_prioritet("10.10.10.3", "0/0/1", "cost" , 14)

def ospf_konf(mgmt_ip, ospf_process, area_id, router_id, nätverk):

    url = f"https://{mgmt_ip}/restconf/data/Cisco-IOS-XE-native:native/router"

    network_list = []

    for nät, wildcard in nätverk:
        network_list.append({
            "ip": nät,
            "wildcard": wildcard,
            "area": area_id
        })

    payload = {
        "Cisco-IOS-XE-native:router": {
            "Cisco-IOS-XE-ospf:router-ospf": {
                "ospf": {
                    "process-id": [
                        {
                            "id": ospf_process,
                            "network": network_list,
                            "router-id": router_id
                        }
                    ]
                }
            }
        }
    }
    
    response = requests.patch(url, headers=headers, auth=("admin","class"),json=payload, verify=False)
    print(response.status_code, response.text)
ospf_konf("10.10.10.1", 1, 0, "1.1.1.1", [("172.16.0.0", "0.0.255.255"), ("192.168.12.0", "0.0.0.255")])
ospf_konf("10.10.10.2", 1, 0, "2.2.2.2", [("172.17.0.0", "0.0.255.255"), ("192.168.12.0", "0.0.0.255")])
ospf_konf("10.10.10.3", 1, 0, "3.3.3.3", [("172.18.0.0", "0.0.255.255"), ("192.168.12.0", "0.0.0.255"), ("12.12.12.12", "0.0.0.3")])







#if '192.168.1.1' in response.text:
    
#Funktion för default-route som skickas ut med OSPF
def default_route(mgmt_ip, ospf_prosess, ut_interface):
 
    #Del 1: statisk default-route
    url = f"https://{mgmt_ip}/restconf/data/Cisco-IOS-XE-native:native/ip/route"
 
    payload = {
        "Cisco-IOS-XE-native:route": {
            "ip-route-interface-forwarding-list": [
                {
                    "prefix": "0.0.0.0",
                    "mask": "0.0.0.0",
                    "fwd-list": [{"fwd": ut_interface}]
                }
            ]
        }
    }
 
    response = requests.patch(url, headers=headers, auth=("admin","class"),json=payload, verify=False)
    print(response.status_code, response.text)
 
    #Del 2: default-information originate i OSPF
    url = f"https://{mgmt_ip}/restconf/data/Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospf:router-ospf/ospf/process-id={ospf_prosess}"
 
    payload = {
        "Cisco-IOS-XE-ospf:process-id": [
            {
                "id": ospf_prosess,
                "default-information": {"originate": {}}
            }
        ]
    }
    
    response = requests.patch(url, headers=headers, auth=("admin","class"),json=payload, verify=False)
    print(response.status_code, response.text)

default_route("10.10.10.1", 1, "Loopback0")
