import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {"Accept": "application/yang-data+json"}
auth = ("admin", "class")

#management-adresser routrar
ISP = "10.10.10.1"
STO = "10.10.10.2"
GBG = "10.10.10.3"

#sökvägar
HOSTNAME       = "Cisco-IOS-XE-native:native/hostname"
OSPF_KONFIG    = "Cisco-IOS-XE-native:native/router"
STATISKA_ROUTES = "Cisco-IOS-XE-native:native/ip/route"
OSPF_STATUS    = "Cisco-IOS-XE-ospf-oper:ospf-oper-data"
ROUTINGTABELL  = "ietf-routing:routing-state"

antal_fel = 0

# Hämtar data från router
def hämta(router, sökväg):
    url = f"https://{router}/restconf/data/{sökväg}"
    response = requests.get(url, headers=headers, auth=auth, verify=False)
    return response.text

# Skriva ut G eller U, räkna ut antal fel
def rätta(text, rätt):
    global antal_fel
    if rätt:
        print("GODKÄND   ", text)
    else:
        text = text.replace(" har ", " har inte ", 1)
        print("UNDERKÄND ", text)
        antal_fel += 1

#kolla IP, mask, no shutdown och description på ett interface
def kolla_interface(router, namn, interface, ip, mask):
    svar = hämta(router, "ietf-interfaces:interfaces/interface=" + interface.replace("/", "%2F"))

    rätta(f"{namn} {interface} har IP {ip}", f'"{ip}"' in svar)
    rätta(f"{namn} {interface} har mask {mask}", f'"{mask}"' in svar)
    rätta(f"{namn} {interface} är no shutdown", '"enabled": true' in svar)
    rätta(f"{namn} {interface} har description", '"description"' in svar)

#kolla OSPF process 1, router-ID och att alla nät är med i area 0
def kolla_ospf(router, namn, router_id, nät_lista):
    svar = hämta(router, OSPF_KONFIG)

    rätta(f"{namn} har OSPF process-ID 1", '"id": 1' in svar)
    rätta(f"{namn} har router-ID {router_id}", f'"router-id": "{router_id}"' in svar)

    for nät in nät_lista:
        rätta(f"{namn} annonserar {nät} i OSPF", f'"ip": "{nät}"' in svar)

    rätta(f"{namn} använder area 0", '"area": 0' in svar)


#kollar ip ospf priority eller cost på ett interface
def kolla_ospf_interface(router, namn, nummer, inställning, värde):
    svar = hämta(router, "Cisco-IOS-XE-native:native/interface/GigabitEthernet=" + nummer.replace("/", "%2F") + "/ip")

    rätta(f"{namn} Gi{nummer} har ip ospf {inställning} {värde}", f'"{inställning}": {värde}' in svar)


#kollar att routern har 2 OSPF-grannar i FULL.
#robban kollar 3 gånger med 5 sekunders paus för att upptäcka fladdrande grannar.
def kolla_grannar(router, namn):
    alltid_full = True

    for gång in range(3):
        svar = hämta(router, OSPF_STATUS)
        if svar.count("ospf-nbr-full") < 2:
            alltid_full = False
        time.sleep(5)

    rätta(f"{namn} har 2 grannar i FULL (kollat 3 gånger)", alltid_full)


#kollar att ett nät finns i routingtabellen
def kolla_route(router, namn, nät):
    svar = hämta(router, ROUTINGTABELL)

    rätta(f"{namn} har route till {nät}", f'"{nät}"' in svar)

#hostname, interface och description
print("\n===== DEL 1: HOSTNAME =====")
rätta("ISP heter ISP", '"ISP"' in hämta(ISP, HOSTNAME))
rätta("STO heter STO", '"STO"' in hämta(STO, HOSTNAME))
rätta("GBG heter GBG", '"GBG"' in hämta(GBG, HOSTNAME))

print("\n===== DEL 1: INTERFACE OCH DESCRIPTION =====")
kolla_interface(ISP, "ISP", "Loopback0", "172.16.0.1", "255.255.0.0")
kolla_interface(STO, "STO", "Loopback0", "172.17.0.1", "255.255.0.0")
kolla_interface(GBG, "GBG", "Loopback0", "172.18.0.1", "255.255.0.0")

kolla_interface(ISP, "ISP", "GigabitEthernet0/0/0", "192.168.12.1", "255.255.255.0")
kolla_interface(STO, "STO", "GigabitEthernet0/0/0", "192.168.12.2", "255.255.255.0")
kolla_interface(GBG, "GBG", "GigabitEthernet0/0/0", "192.168.12.3", "255.255.255.0")
kolla_interface(GBG, "GBG", "GigabitEthernet0/0/1", "12.12.12.13", "255.255.255.252")


#ospf

print("\n===== DEL 2: OSPF PROCESS, AREA OCH ROUTER-ID (punkt 1-2) =====")
kolla_ospf(ISP, "ISP", "1.1.1.1", ["192.168.12.0", "172.16.0.0"])
kolla_ospf(STO, "STO", "2.2.2.2", ["192.168.12.0", "172.17.0.0"])
kolla_ospf(GBG, "GBG", "3.3.3.3", ["192.168.12.0", "172.18.0.0", "12.12.12.12"])

print("\n===== DEL 2: PRIORITET OCH KOSTNAD (punkt 3-5) =====")
kolla_ospf_interface(STO, "STO", "0/0/0", "priority", 255)   # punkt 3: STO så hög som möjligt
kolla_ospf_interface(ISP, "ISP", "0/0/0", "priority", 0)     # punkt 4: ISP aldrig DR/BDR
kolla_ospf_interface(GBG, "GBG", "0/0/1", "cost", 14)        # punkt 5: kostnad 14 mot PC:n


#static route

print("\n===== DEL 3: DEFAULT-ROUTE PÅ ISP =====")
svar = hämta(ISP, STATISKA_ROUTES)
rätta("ISP har ip route 0.0.0.0 0.0.0.0", '"prefix": "0.0.0.0"' in svar)
rätta("ISP default-route pekar på Loopback0", '"fwd": "Loopback0"' in svar)

rätta("ISP har default-information originate", "originate" in hämta(ISP, OSPF_KONFIG))

#grannar
print("\n===== DEL 4: OSPF-GRANNAR =====")
kolla_grannar(ISP, "ISP")
kolla_grannar(STO, "STO")
kolla_grannar(GBG, "GBG")

print("\n===== DEL 4: DR OCH BDR =====")
# ISP har prioritet 0 och är varken DR eller BDR, så ISP ser tydligt vem som är det
svar = hämta(ISP, OSPF_STATUS)
rätta("STO (192.168.12.2) är DR", '"dr": "192.168.12.2"' in svar)
rätta("GBG (192.168.12.3) är BDR", '"bdr": "192.168.12.3"' in svar)

print("\n===== DEL 4: ROUTINGTABELL (full connectivity) =====")
# OSPF annonserar loopbacks som /32, därför letar Robert efter /32
kolla_route(ISP, "ISP", "172.17.0.1/32")
kolla_route(ISP, "ISP", "172.18.0.1/32")
kolla_route(ISP, "ISP", "12.12.12.12/30")

kolla_route(STO, "STO", "172.16.0.1/32")
kolla_route(STO, "STO", "172.18.0.1/32")
kolla_route(STO, "STO", "12.12.12.12/30")

kolla_route(GBG, "GBG", "172.16.0.1/32")
kolla_route(GBG, "GBG", "172.17.0.1/32")

print("\n===== DEL 4: DEFAULT-ROUTEN HAR KOMMIT UT MED OSPF =====")
# STO och GBG har ingen egen statisk route, så har de 0.0.0.0/0 kommer den från ISP via OSPF
kolla_route(STO, "STO", "0.0.0.0/0")
kolla_route(GBG, "GBG", "0.0.0.0/0")


#slutresultat

print("\n==============================")
if antal_fel == 0:
    print("ROBERT SÄGER: GODKÄND (G)")
else:
    print("ROBERT SÄGER: UNDERKÄND (U)")
    print("Antal fel:", antal_fel)
print("==============================")