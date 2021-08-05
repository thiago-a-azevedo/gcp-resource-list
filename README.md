# gcp-resource-list
If you need a consolidated list of your GCP components, these scripts can help you :)

Based on the python GCP SDK, you can check a list(\*.csv) of components (GCE, GKE, ClouSQL, Quota) of all the projects that you have access to, including some key properties that can help you to review operational analysis.

## Setup
After you download or clone the repository, install the pip requirements, and run the list* script related to the components you want to check.
```bash
pip install -r requirements.txt
```
## Listing your GCP components

Set your GCP credentials. Reference[GCP Default Credentials](https://developers.google.com/accounts/docs/application-default-credentials)
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/your-dir/your-credential.json 
```
**Permissions required:**
* cloudsql.instances.list
* compute.instances.list
* compute.zones.list
* container.clusters.list
* resourcemanager.projects.get

If you review how to create a service account and JSON, please check the link [Creating and managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).


You can use the **--project parameter** to define a project_id filter. If the parameter is empty, **all the active project_ids** that the credential has access will be listed.
```bash
python3 list-gce.py
```
or
```bash
python3 list-gce.py --project my-project-id
```


## Scripts


### list-vpc.py
List the VPC components in a CSV format.
### list-gce.py
List the GCE components in a CSV format.
### list-gke.py
List the GKE components in a CSV format.
### list-gke-nodes.py
List the GKE Node components in a CSV format.
### list-sql.py
List the CloudSQL components in a CSV format.
### list-quotas-project.py
List the project Quotas in a CSV format.
### list-quotas-regional.py
List the project Quotas, regional level, in a CSV format.
### list-inc.py
List public GCP incidents based in a CSV format, based on [GCP Status page](https://status.cloud.google.com/)


## To Do
* PubSub scripts
* MemoryStore scripts
* Review Project filter to support comma delimited
* Review GKE subnet sizing
