# https://googleapis.github.io/google-api-python-client/docs/dyn/
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
         
        try:
            for gce in resp['items']:
                diskAmt = diskSiz =0
                ipAmt = 0
                ipExt = 'None'

                for disk in gce['disks']:
                    diskAmt +=1
                    diskSiz = diskSiz + float(disk.get('diskSizeGb'))

                for accessConfig in gce['networkInterfaces']:
                    #print(accessConfig)
                    try:
                        for nats in accessConfig['accessConfigs']:
                            #print(nats)
                            if nats.get('type',{}) == 'ONE_TO_ONE_NAT':
                                ipExt=nats.get('natIP')                                            
                                ipAmt +=1
                                #print(ipExt)
                    except KeyError: pass                                       
                
                machineTypeUrl=gce.get('machineType').split(sep="/")
                machineType=machineTypeUrl[len(machineTypeUrl)-1]

                
                print (
                    project.project_id, ';',
                    project.name, ';',
                    zone.get('name'),';',
                    gce.get('name'), ';',                 
                    gce.get('cpuPlatform'), ';',
                    machineType, ';',
                    #gce.get('machineType').split(sep="/"), ';',
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