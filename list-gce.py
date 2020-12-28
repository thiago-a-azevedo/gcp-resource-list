# https://developers.google.com/resources/api-libraries/documentation/container/v1/python/latest/container_v1.projects.zones.clusters.html

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
    
    zone_request = compute.zones().list(project=project.project_id)        
    zones = zone_request.execute()

    for zone in zones['items']:
        #print(zone.get('name'))
        
        resp = compute.instances().list(project=project.project_id, zone=zone.get('name')).execute()
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
                    zone.get('name'),';',
                    project.name, ';',
                    gce.get('name'), ';',                 
                    gce.get('kind'), ';',
                    diskAmt, ';',
                    diskSiz, ';',
                    )
        except KeyError: pass

        #print(
        #    project.project_id, ';',
        #    project.name, ';', 
        #    cluster.get('name'),';', 
        
        '''
        name
        machineType
        id
        creationTimestamp
        status
        zone
        networkInterfaces[]
            -- fazer um count?
            -- nic zero?
        disks[]
            --type
            --boot
            --diskSizeGb
        metadada/item/key(instance-template)
        serviceAccounts
        scheduling/preemptible
        scheduling/automaticRestart
        scheduling/onHostMaintenance
        cpuPlatform
        lastStartTimestamp
        '''