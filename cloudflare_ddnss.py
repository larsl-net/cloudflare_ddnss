import requests
import json
import datetime
import pathlib
import os


#Set Work Dir to Script Folder
dir_path = pathlib.Path(__file__).parent.absolute()
os.chdir(dir_path)

with open("accounts.json") as accounts_file:
  accounts = json.load(accounts_file)
with open("domains.json") as domains_file:
  domains = json.load(domains_file)

 #Log
logfile = open('log.txt', "a+")
logfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))

ip4=requests.get('http://ipv4.icanhazip.com/').text.strip()
ip6=requests.get('http://ipv6.icanhazip.com/').text.strip()
print("Current IPv4: "+ip4)
print("Current IPv6: "+ip6)
logfile.write("Current IPv4: "+ip4+"\n")
logfile.write("Current IPv6: "+ip6+"\n")



for auth_email in domains.keys():
  print("Email:" + auth_email)
  logfile.write("Email:" + auth_email+"\n")
  for zone in domains[auth_email].keys():
    print("Zone: " + zone)
    logfile.write("Zone: " + zone+"\n")
    for record in domains[auth_email][zone].values():
      print("Record:" + record)
      logfile.write("Record:" + record+"\n")


      #Set Cloudflare API Settings
      url = 'https://api.cloudflare.com/client/v4/'
      headers = {
          'X-Auth-Email': auth_email,
          'X-Auth-Key': accounts[auth_email],
          'Content-Type': 'application/json',
      }


      #Get Zone ID
      zone_id = requests.get(url=url+'zones', headers=headers, params={'name':zone}).json()['result'][0]['id']


      #Get Record
      record4 = requests.get(url=url+'zones/'+zone_id+'/dns_records', headers=headers, params={'name':record, 'type': 'A'}).json()['result'][0]
      record6 = requests.get(url=url+'zones/'+zone_id+'/dns_records', headers=headers, params={'name':record, 'type': 'AAAA'}).json()['result'][0]

      if ip4 != record4['content']:
        print("IPv4 will be updated")
        logfile.write("IPv4 will be updated"+"\n")
        res4 = requests.put(url=url+'zones/'+zone_id+'/dns_records/'+record4['id'], headers=headers, json={'type':'A', 'name':record, 'content':ip4, 'ttl':'1', 'proxied':'true'}).json()
        if res4['success']:
          print("Update success")
          logfile.write("Update success"+"\n")
        else:
          print("Error Updating IPv4: "+res4['errors'][0]['message'])
          logfile.write("Error Updating IPv4: "+res4['errors'][0]['message']+"\n")

      if ip6 != record6['content']:
        print("IPv6 will be updated")
        logfile.write("IPv6 will be updated"+"\n")
        res6 = requests.put(url=url+'zones/'+zone_id+'/dns_records/'+record6['id'], headers=headers, json={'type':'AAAA', 'name':record, 'content':ip6, 'ttl':'1', 'proxied':'true'}).json()
        if res6['success']:
          print("Update success")
          logfile.write("Update success"+"\n")
        else:
          print("Error Updating IPv6: "+res6['errors'][0]['message'])
          logfile.write("Error Updating IPv6: "+res6['errors'][0]['message']+"\n")
