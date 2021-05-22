# List GCP Regional project quotas
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
    env_filter = {'projectId': project_Filter.project ,'lifecycleState': 'ACTIVE' }

# print csv header
print ('project_id;project_name;region;metric;limit;usage')

for project in client.list_projects(env_filter):
    
    region_request = compute.regions().list(project=project.project_id)        
    regions = region_request.execute()
    
    for region in regions['items']:
        for quota in region['quotas']:
            print(
                project.project_id, ';',
                project.name, ';',
                region.get('name'),';',
                quota.get('metric'),';',
                quota.get('limit'),';',
                quota.get('usage'),';'

            )            