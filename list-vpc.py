# List VPCs
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
'if empity will looking for all the active project_id that the credential have access.'
'Support for comma separeted projects')
parser_args.add_argument('--project')
project_filter = parser_args.parse_args()

# Project parameter validation
project_valid = []
if project_filter.project is None:
    env_filter = {'lifecycleState': 'ACTIVE' }
    for project_param in client.list_projects(env_filter):
        project_valid.append(project_param.project_id)
else:
    project_list = project_filter.project.split(',')
    for project_listed in project_list:
        env_filter = {'projectId': project_listed ,'lifecycleState': 'ACTIVE' }
        for project_param in client.list_projects(env_filter):
            project_valid.append(project_param.project_id)

# print csv header
print ('project_id;vpc;autoCreateSubnetworks;subnets_count')

for project_validated in project_valid:
    try:
        networks = compute.networks().list(project=project_validated)        
        vpcs = networks.execute()
        #print(vpc)
        for vpc in vpcs['items']:
            print(
                project_validated,';',
                vpc.get('name'),';',
                vpc.get('autoCreateSubnetworks'),';',
                len(vpc.get('subnetworks')),
                )
    except: pass