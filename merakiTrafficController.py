# -*- coding: utf-8 -*-
from meraki import *
from meraki.meraki import *
from colorama import Fore, Back,init
import csv
import argparse
import sys
init()

parser=argparse.ArgumentParser()
parser.add_argument("--list-clients",help="Permet de lister, puis de choisir un client",action="store_true")
args=parser.parse_args()

print(Fore.GREEN)
api_key=input("Meraki API key : ")
print(Fore.WHITE)

try:
    clients=Meraki(api_key)
    org=clients.organizations.get_organizations()
except:
    print(Fore.RED + "The provided api key is not valid or has expired...aborting" + Fore.WHITE)
    sys.exit(0)


params = {}
params["organization_id"] = org[0]["id"]
nets = clients.networks.get_organization_networks(params)

def get_devices(a):
	devices = clients.devices.get_network_devices(a)
	return(devices)

devices=get_devices(nets[1]["id"])

organization_id =nets[1]["organizationId"]

network_id=devices[0]["networkId"]
serial=devices[0]["serial"]


alert_settings_controller = clients.alert_settings
admins_controller=clients.admins
networks_controller = clients.networks
devices_controller = clients.devices
clients_controller = clients.clients


als = alert_settings_controller.get_network_alert_settings(network_id)


collect = {}

collect['network_id'] = network_id

timespan = 7200
collect['timespan'] = timespan

result = networks_controller.get_network_traffic(collect)



collect = {}
collect['serial'] = serial
devicessd = clients_controller.get_device_clients(collect)











devices=get_devices(nets[2]["id"])


organization_id =nets[2]["organizationId"]

network_id=devices[0]["networkId"]
serial=devices[0]["serial"]


alert_settings_controller = clients.alert_settings
admins_controller=clients.admins
networks_controller = clients.networks
devices_controller = clients.devices
clients_controller = clients.clients


als = alert_settings_controller.get_network_alert_settings(network_id)


collect = {}

collect['network_id'] = network_id

timespan = 7200
collect['timespan'] = timespan

result = networks_controller.get_network_traffic(collect)



collect = {}
collect['serial'] = serial
devicess = clients_controller.get_device_clients(collect)





def collect_client_traffic(id_or_mac_or_ip,network_id):
	collect = {}
	collect['network_id'] = network_id
	collect['id_or_mac_or_ip'] = id_or_mac_or_ip
	client_trafil_history = clients_controller.get_network_client_traffic_history(collect)
	return(client_trafil_history)





menu=["Active time","Url","Port","protocol","Application","Description","HostName","Ip","Mac"]
l=[]

if args.list_clients==True:
	i=0
	for el in devicess:
		i+=1
		change=False
		for n in devicessd:
			if el["ip"]==n["ip"]:
				hostname=n["dhcpHostname"]
				change=True
		if change==False:
			hostname=el["dhcpHostname"]
		if hostname==None:
			hostname="N/A"
		print("  " + Fore.WHITE + "[" + Fore.YELLOW + str(i) + Fore.WHITE + "]" + "  " + Fore.RED + str(el["ip"]) + Fore.BLUE + "  " + str(el["mac"]) + "   " + Fore.GREEN + str(el["description"]) + " " + Fore.WHITE + "(" + Fore.YELLOW + str(hostname) +  Fore.GREEN + ")")
	continuer=True
	while continuer==True:
		print("\n")
		print(Fore.BLUE + "Target" + Fore.WHITE + ">" + " " + Fore.WHITE,end="")
		target=input("")
		try:
			target=int(target)
			if target<=i and target>0:
				continuer=False
			else:
				print(6/0)
		except:
			print(Fore.RED + "ERREUR : L'entree n'est pas valide !" + Fore.WHITE)

	id_or_mac_or_ip=devicess[target-1]["id"]
	traffic_client=collect_client_traffic(id_or_mac_or_ip,network_id)

	for el in traffic_client:
		chang=False
		pr=""
		try:
			pr+=str(el["activeTime"])
		except:
			pr+=str(el["activeSeconds"])
		pr+="|" + str(el["destination"])
		pr+="|" + str(el["port"])
		pr+="|" + str(el["protocol"])
		pr+="|" + str(el["application"])
		pr+="|" + str(devicess[target-1]["description"])
		for n in devicessd:
			if n["ip"]==devicess[target-1]["ip"]:
				pr+="|"+ str(n["dhcpHostname"])
				chang=True
		if chang==False:
			pr+="|"+ str(devicess[target-1]["dhcpHostname"])
		pr+="|" + str(devicess[target-1]["ip"])
		pr+="|" + str(devicess[target-1]["mac"])

		pr=pr.split("|")
		l.append(pr)
		
	with open('traffic.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(menu)
		for g in l:
			spamwriter.writerow(g)

	print(Fore.GREEN + "Success : resultats enregistres dans \"traffic.csv\" !")
	sys.exit(0)


i=0
r=0
for b in devicess:
	r+=1 
for e in devicess:
	if i<r:
		id_or_mac_or_ip=devicess[i]["id"]
		traffic_client=collect_client_traffic(id_or_mac_or_ip,network_id)


		for el in traffic_client:
			chang=False
			pr=""
			try:
				pr+=str(el["activeTime"])
			except:
				pr+=str(el["activeSeconds"])
			pr+="|" + str(el["destination"])
			pr+="|" + str(el["port"])
			pr+="|" + str(el["protocol"])
			pr+="|" + str(el["application"])
			pr+="|" + str(e["description"])
			for n in devicessd:
				if n["ip"]==e["ip"]:
					pr+="|"+ str(n["dhcpHostname"])
					chang=True
			if chang==False:
				pr+="|"+ str(e["dhcpHostname"])
			pr+="|" + str(e["ip"])
			pr+="|" + str(e["mac"])

			pr=pr.split("|")
			l.append(pr)


	i+=1
			
with open('traffic.csv', 'w', newline='') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
				spamwriter.writerow(menu)
				for g in l:

					spamwriter.writerow(g)

print(Fore.GREEN + "Success : resultats enregistres dans \"traffic.csv\" !")
