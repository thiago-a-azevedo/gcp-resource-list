# List GCE instances
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

# print csv header
print ('project_id;project_name;zone;instance_name;cpuPlatform;machineType;',
'status;lastStartTimestamp;preemptible;automaticRestart;onHostMaintenance;',
'disk_amount;disk_total_size;publicIP;nic_amount;creationTimestamp')

for project in client.list_projects(env_filter):
    
    zone_request = compute.zones().list(project=project.project_id)        
    zones = zone_request.execute()

    for zone in zones['items']:

        resp = compute.instances().list(project=project.project_id, zone=zone.get('name')).execute()
         
        try:
            for gce in resp['items']:
                diskAmt = diskSiz =0
                ipAmt = 0
                ipExt = 'None'

                for disk in gce['disks']:
                    diskAmt +=1
                    diskSiz = diskSiz + float(disk.get('diskSizeGb'))

                for accessConfig in gce['networkInterfaces']:
                    ipAmt +=1
                    try:
                        for nats in accessConfig['accessConfigs']:
                            if nats.get('type',{}) == 'ONE_TO_ONE_NAT':
                                ipExt=nats.get('natIP')                                            
                    except KeyError: pass                                       
                
                # Remove the full url for machineType
                machineTypeUrl=gce.get('machineType').split(sep="/")
                machineType=machineTypeUrl[len(machineTypeUrl)-1]
        
                print (
                    project.project_id, ';',
                    project.name, ';',
                    zone.get('name'),';',
                    gce.get('name'), ';',                 
                    gce.get('cpuPlatform'), ';',
                    machineType, ';',
                    gce.get('status'), ';',
                    gce.get('lastStartTimestamp'), ';',
                    gce.get('scheduling').get('preemptible'), ';',
                    gce.get('scheduling').get('automaticRestart'), ';',
                    gce.get('scheduling').get('onHostMaintenance'), ';',                    
                    diskAmt, ';',
                    diskSiz, ';',
                    ipExt, ';',
                    ipAmt, ';',
                    gce.get('creationTimestamp')
                    )
                
        except KeyError: pass