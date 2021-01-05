# List GKE nodes
# Official GCP SDK (Python) Documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/

import json
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
    env_filter = {'name': project_Filter.project ,'lifecycleState': 'ACTIVE' }

# Print csv Header
print ('project_id; project_name;cluster_name;node_name;node_version;machineType;',
'diskSizeGb;diskType;autoscaling;minNodeCount;maxNodeCount;autoUpgrade;maxPodsPerNode;', 
'podIpv4CidrSize;locations')

zone='-'

for project in client.list_projects(env_filter):
    req = service.projects().zones().clusters().list(projectId=project.project_id, zone=zone)
    resp = req.execute()
    
    try: 
        for cluster in resp['clusters']:
            for node in cluster['nodePools']:
                print(
                    project.project_id, ';',
                    project.name, ';', 
                    cluster.get('name'),';',
                    node.get('name'),';',
                    node.get('version'),';',
                    node.get('config').get('machineType'),';',
                    node.get('config').get('diskSizeGb'),';',
                    node.get('config').get('diskType'),';',
                    node.get('autoscaling',{}).get('enabled',{}),';',
                    node.get('autoscaling',{}).get('minNodeCount',{}),';',
                    node.get('autoscaling',{}).get('maxNodeCount',{}),';',
                    node.get('management').get('autoUpgrade'),';',
                    node.get('maxPodsConstraint').get('maxPodsPerNode'),';',
                    node.get('podIpv4CidrSize'),';',
                    node.get('locations')
                    )
                        

    except KeyError: pass