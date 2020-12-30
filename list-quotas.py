# List GCP project quotas
# Official GCP SDK (Python) Documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/

import json
import ipcalc
import sys
import argparse
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.cloud import resource_manager

client = resource_manager.Client()

credentials = GoogleCredentials.get_application_default()
compute = discovery.build('compute', 'v1', credentials=credentials)

# Filter of Projects that will be scanned 
parser_args = argparse.ArgumentParser(description='Define the projetc_id filter.'
'if empity will looking for all the active project_id that the credential have access')
parser_args.add_argument('--project')

project_Filter = parser_args.parse_args()


if project_Filter.project is None:
    env_filter = {'lifecycleState': 'ACTIVE' }
else:
    env_filter = {'name': project_Filter.project ,'lifecycleState': 'ACTIVE' }


for project in client.list_projects(env_filter):
    
    region_request = compute.regions().list(project=project.project_id)        
    regions = region_request.execute()
    print (regions)
    for region in regions['items']:
        #print(zone.get('name'))
        resp = compute.addresses().list(project=project.project_id, zone=zone.get('name')).execute()
    
    zone_request = compute.zones().list(project=project.project_id)        
    zones = zone_request.execute()
    #print (zones)
    for zone in zones['items']:
        #print(zone.get('name'))
        
        resp = compute.addresses().list(project=project.project_id, zone=zone.get('name')).execute()
        #print(resp)
        #for instance in resp["items"]:
            #if instance["networkInterfaces"][0]["networkIP"] == internal_ip:
            #    internal_id = instance["id"]
        
        try:
            for gce in resp['items']:
                diskAmt = diskSiz =0

                for disk in gce['disks']:
                    diskAmt +=1
                    diskSiz = diskSiz + float(disk.get('diskSizeGb'))
                        
                
                print (
                    project.project_id, ';',
                    project.name, ';',
                    zone.get('name'),';',
                    gce.get('name'), ';',                 
                    gce.get('kind'), ';',
                    diskAmt, ';',
                    diskSiz, ';',
                    )
        except KeyError: pass