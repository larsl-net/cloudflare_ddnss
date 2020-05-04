import requests
import json
import datetime
import pathlib
import os


#Set Work Dir to Script Folder and Load Domains
dir_path = pathlib.Path(__file__).parent.absolute()
os.chdir(dir_path)

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


for auth_name in domains.keys():
  print("Email:" + auth_name)
  logfile.write("Auth Name:" + auth_name+"\n")

  #Set Cloudflare API Settings
  url = 'https://api.cloudflare.com/client/v4/'
  if domains[auth_name]['config']['token_mode']:
    headers = {
      'Authorization': 'Bearer '+ domains[auth_name]['config']['token'],
      'Content-Type': 'application/json'
    }
  else:
    headers = {
      'X-Auth-Email': domains[auth_name]['config']['email'],
      'X-Auth-Key': domains[auth_name]['config']['key'],
      'Content-Type': 'application/json'
    }


  for zone in domains[auth_name]['zones'].keys():
    print("Zone: " + zone)
    logfile.write("Zone: " + zone+"\n")


    #Get Settings for Zone
    settings_zone = {}
    settings_zone.update({"ttl":  domains[auth_name]['config'].get('ttl', 1)})
    settings_zone.update({"proxied":  domains[auth_name]['config'].get('proxied', True)})
    settings_zone.update({"ip4":  domains[auth_name]['config'].get('ip4', True)})
    settings_zone.update({"ip6":  domains[auth_name]['config'].get('ip6', True)})
    settings_zone.update({"force_settings":  domains[auth_name]['config'].get('force_settings', True)})


    #Get Zone ID
    zone_id = requests.get(url=url+'zones', headers=headers, params={'name':zone}).json()
    if zone_id['success']:
      zone_id = zone_id['result'][0]['id']


      #Run Records
      for record in domains[auth_name]['zones'][zone].keys():
        print("Record:" + record)
        logfile.write("Record:" + record+"\n")


        #Get Settings for Record
        settings = settings_zone
        settings = {}
        settings["ttl"] = domains[auth_name]['zones'][zone][record].get('ttl', settings_zone['ttl'])
        settings["proxied"] = domains[auth_name]['zones'][zone][record].get('proxied', settings_zone['proxied'])
        settings["ip4"] = domains[auth_name]['zones'][zone][record].get('ip4', settings_zone['ip4'])
        settings["ip6"] = domains[auth_name]['zones'][zone][record].get('ip6', settings_zone['ip6'])
        settings["force_settings"] = domains[auth_name]['zones'][zone][record].get('force_settings', settings_zone['force_settings'])


        #Ipv4
        if settings["ip4"]:
          if 'record4_id' in domains[auth_name]['zones'][zone][record]:
            record4 = requests.get(url=url+'zones/'+zone_id+'/dns_records/'+domains[auth_name]['zones'][zone][record]['record4_id'], headers=headers, params={'name':record, 'type': 'A'}).json()
            if record4['success']:
              record4 = record4['result']
            else:
              print("No Record with this ID found")
          else:
            record4 = requests.get(url=url+'zones/'+zone_id+'/dns_records', headers=headers, params={'name':record, 'type': 'A'}).json()
            if record4['success'] and (record4['result_info']['total_count']):
              record4 = record4['result'][0]
            else:
              print("No Record found")

          #Update Records if IP is changed
          if ip4 != record4['content'] or (settings['force_settings'] and ((record4['ttl'] != settings['ttl']) or ((record4['proxied'] != settings['proxied']) and (record4['proxiable'] == True)))):
            print("A Record will be updated")
            logfile.write("IPv4 will be updated"+"\n")
            res4 = requests.put(url=url+'zones/'+zone_id+'/dns_records/'+record4['id'], headers=headers, json={'type':'A', 'name':record, 'content':ip4, 'ttl':settings["ttl"], 'proxied':settings["proxied"]}).json()
            if res4['success']:
              print("Update success")
              logfile.write("Update success"+"\n")
            else:
              print("Error Updating A Record: "+res4['errors'][0]['message'])
              logfile.write("Error Updating A Record: "+res4['errors'][0]['message']+"\n")
          


        #Ipv6
        if settings["ip6"]:
          if 'record6_id' in domains[auth_name]['zones'][zone][record]:
            record4 = requests.get(url=url+'zones/'+zone_id+'/dns_records/'+domains[auth_name]['zones'][zone][record]['record6_id'], headers=headers, params={'name':record, 'type': 'AAAA'}).json()
            if record6['success']:
              record6 = record6['result']
            else:
              print("No Record with this ID found")
          else:
            record6 = requests.get(url=url+'zones/'+zone_id+'/dns_records', headers=headers, params={'name':record, 'type': 'AAAA'}).json()
            if record6['success'] and (record6['result_info']['total_count']):
              record6 = record6['result'][0]
            else:
              print("No Record found")

          #Update Records if IP is changed
          if ip6 != record6['content'] or (settings['force_settings'] and ((record6['ttl'] != settings['ttl']) or ((record6['proxied'] != settings['proxied']) and (record6['proxiable'] == True)))):
            print("AAAA Record will be updated")
            logfile.write("IPv6 will be updated"+"\n")
            res6 = requests.put(url=url+'zones/'+zone_id+'/dns_records/'+record6['id'], headers=headers, json={'type':'AAAA', 'name':record, 'content':ip6, 'ttl':settings["ttl"], 'proxied':settings["proxied"]}).json()
            if res6['success']:
              print("Update success")
              logfile.write("Update success"+"\n")
            else:
              print("Error Updating AAAA Record: "+res6['errors'][0]['message'])
              logfile.write("Error Updating A Record: "+res6['errors'][0]['message']+"\n")
    
    
    #IF Zone not found/exists
    else:
      print("Error: " + zone_id['errors'][0]['message'])