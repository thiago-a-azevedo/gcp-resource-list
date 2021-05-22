# List GKE clusters
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
service = discovery.build('container', 'v1', credentials=credentials)

# Filter of Projects that will be scanned 
parser_args = argparse.ArgumentParser(description='Define the projetc_id filter.'
'if empity will looking for all the active project_id that the credential have access')
parser_args.add_argument('--project')

project_Filter = parser_args.parse_args()


if project_Filter.project is None:
    env_filter = {'lifecycleState': 'ACTIVE' }
else:
    env_filter = {'projectId': project_Filter.project ,'lifecycleState': 'ACTIVE' }

# print csv header
print ('project_id;project_name;cluster_name;master_version;locations;',
'currentNodeCount;maxPodsPerNode;useIpAliases;clusterIpv4CidrBlock;ipRangeSizePod;',
'servicesIpv4CidrBlock;ipRangeSizeService;NodesubnetRange;ipRangeSizeNode;', 
'enablePrivateNodes;enablePrivateEndpoint;masterIpv4CidrBlock;privateEndpoint;',
'publicEndpoint;dnsCacheConfig;loggingService;monitoringService;',
'consumptionMeteringConfig;releaseChannel')

zone='-'

for project in client.list_projects(env_filter):
    req = service.projects().zones().clusters().list(projectId=project.project_id, zone=zone)
    resp = req.execute()
 
    try: 
        for cluster in resp['clusters']:
            # nodeIpv4CidrBlock is only available if the cluster is created is a create-subnetwork param
            if not cluster.get('ipAllocationPolicy',{}).get('nodeIpv4CidrBlock'):
                subnet_range='Shared'
                ipRangeNodeSize='Shared'
            else:
                subnet_range=cluster.get('ipAllocationPolicy',{}).get('nodeIpv4CidrBlock')
                ipRangeNodeSize=ipcalc.Network(cluster.get('ipAllocationPolicy',{}).get('nodeIpv4CidrBlock')).size()-4
            
            # IP Range Calculation 
            # -4 Reserved IPs: Network,Default gateway,Second-to-last address,Broadcast
            
            if cluster.get('ipAllocationPolicy',{}).get('clusterIpv4CidrBlock') is not None:
                ipRangePodSize=ipcalc.Network(cluster.get('ipAllocationPolicy',{}).get('clusterIpv4CidrBlock')).size()-4
                ipRangeServiceSize=ipcalc.Network(cluster.get('ipAllocationPolicy',{}).get('servicesIpv4CidrBlock')).size()-4
            else:
                ipRangePodSize = ipRangeServiceSize = None

            print(
            project.project_id, ';',
            project.name, ';', 
            cluster.get('name'),';', 
            cluster.get('currentMasterVersion'),';', 
            cluster.get('locations'),';', 
            cluster.get('currentNodeCount'),';', 
            cluster.get('defaultMaxPodsConstraint',{}).get('maxPodsPerNode'),';', 
            cluster.get('ipAllocationPolicy',{}).get('useIpAliases'),';', 
            cluster.get('ipAllocationPolicy',{}).get('clusterIpv4CidrBlock'),';',
            ipRangePodSize ,';',            
            cluster.get('ipAllocationPolicy',{}).get('servicesIpv4CidrBlock'),';',
            ipRangeServiceSize ,';', 
            subnet_range,';', 
            ipRangeNodeSize,';', 
            cluster.get('privateClusterConfig',{}).get('enablePrivateNodes'),';',
            cluster.get('privateClusterConfig',{}).get('enablePrivateEndpoint'),';',
            cluster.get('privateClusterConfig',{}).get('masterIpv4CidrBlock'),';',
            cluster.get('privateClusterConfig',{}).get('privateEndpoint'),';',
            cluster.get('privateClusterConfig',{}).get('publicEndpoint'),';',
            cluster.get('addonsConfig',{}).get('dnsCacheConfig',{}).get('enabled','None'),';',
            cluster.get('loggingService') ,';',
            cluster.get('monitoringService'),';', 
            cluster.get('consumptionMeteringConfig'),';',
            cluster.get('releaseChannel',{}).get('channel')            
            )
    except KeyError: pass
   