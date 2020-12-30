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
    globalddresses = compute.globalAddresses().list(project=project.project_id).execute()
    print(globalddresses)



    region_request = compute.regions().list(project=project.project_id)        
    regions = region_request.execute()
    #print (regions)
    for region in regions['items']:
        #print(region.get('selfLink'))
        addresses = compute.addresses().list(project=project.project_id, region=region.get('name')).execute()
        #addresses = compute.addresses().list(project=project.project_id, region=region.get('name'), filter='addressType=EXTERNAL').execute()
        #print(addresses)