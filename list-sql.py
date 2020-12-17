# https://developers.google.com/resources/api-libraries/documentation/sqladmin/v1beta4/python/latest/sqladmin_v1beta4.instances.html#update

import json
import sys
import argparse
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.cloud import resource_manager

'''
Authenticating as an end user

from google_auth_oauthlib import flow

launch_browser = False
SCOPES = ['https://www.googleapis.com/auth/cloud-platform.read-only', 'https://www.googleapis.com/auth/sqlservice.admin']
appflow = flow.InstalledAppFlow.from_client_secrets_file(
    "/Users/tazevedo/mycode/creds/client_secrets.json",SCOPES
)

if launch_browser:
    appflow.run_local_server()
else:
    appflow.run_console()

credentials = appflow.credentials
'''

client = resource_manager.Client()
credentials = GoogleCredentials.get_application_default()
service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)

# Filter of Projects that will be scanned 
parser_args = argparse.ArgumentParser(description='Define the projetc_id filter.'
'if empity will looking for all the active project_id that the credential have access')
parser_args.add_argument('--project')

project_Filter = parser_args.parse_args()


if project_Filter.project is None:
    env_filter = {'lifecycleState': 'ACTIVE' }
else:
    env_filter = {'name': project_Filter.project ,'lifecycleState': 'ACTIVE' }


print ('project_name;project_id;instance_name;tier;dbversion;backendType;state;replicationType;'
       'diksType;diskSize(GB);storageAutoResize;availabilityType;automatedBackup;publicIP')

for project in client.list_projects(env_filter):
    req = service.instances().list(project=project.project_id)
    resp = req.execute()
    #print(resp)
    try: 
        for sql in resp['items']:
            public_ip='None'
            for ip in sql['ipAddresses']:
                if ip.get('type') in ('PRIMARY'):
                    public_ip=ip.get('ipAddress')            
            print(
            project.name, ';', 
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
    except KeyError: pass
    