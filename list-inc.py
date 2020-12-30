# List in csv the public GCP incidents filtered by region
# Data source: https://status.cloud.google.com

import json
import requests


# Define the filtered regions
region=['southamerica', 'global']
req = requests.get('https://status.cloud.google.com/incidents.json').json()

# Print csv Header
print ('Inc. Number;Begin Date;End Date;Service;Severity;Desc')

# Look into the incident external description and updates for region match strings
for inc in req:
    if any(i in inc.get('external_desc') for i in region):
        print (inc.get('number'), ';', inc.get('begin'),';', inc.get('end'),';', inc.get('service_name'), ';', inc.get('severity')  , ';', inc.get('external_desc'))
    else:
        for updates in inc['updates']:
            if any(i in updates.get('text') for i in region):
                print (inc.get('number'), ';', inc.get('begin'),';', inc.get('end'),';', inc.get('service_name'), ';', inc.get('severity')  , ';', inc.get('external_desc'))
                break