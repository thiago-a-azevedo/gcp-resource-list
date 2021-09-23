# List CloudSQL instances
# Official GCP SDK (Python) Documentation: https://googleapis.github.io/google-api-python-client/docs/dyn/

import json
import sys
import argparse
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.cloud import resource_manager

client = resource_manager.Client()
credentials = GoogleCredentials.get_application_default()
service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)

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

print ('project_name;project_id;instance_name;tier;dbversion;backendType;state;replicationType;'
       'diksType;diskSize(GB);storageAutoResize;availabilityType;automatedBackup;publicIP')

for project_validated in project_valid:    
    try:
        req = service.instances().list(project=project_validated)
        resp = req.execute()
        #print(resp)
        try: 
            for sql in resp['items']:
                public_ip='None'
                for ip in sql['ipAddresses']:
                    if ip.get('type') in ('PRIMARY'):
                        public_ip=ip.get('ipAddress')            
                print(
                project_validated, ';', 
                sql.get('project'),';', 
                sql.get('name'),';', 
                sql.get('settings').get('tier'),';', 
                sql.get('databaseVersion') ,';',
                sql.get('backendType'),';', 
                sql.get('settings').get('activationPolicy'), ';',
                sql.get('settings').get('replicationType'), ';',
                sql.get('settings').get('dataDiskType'), ';',
                sql.get('settings').get('dataDiskSizeGb'), ';',
                sql.get('settings').get('storageAutoResize'), ';',
                sql.get('availabilityType'), ';',
                sql.get('settings').get('backupConfiguration').get('enabled'), ';',
                public_ip
                )
        except : pass
    except : pass
