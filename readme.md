### pip config
pip install --upgrade pip setuptools
python.exe -m pip install --upgrade pip

### launch train.py (in /01 folder path)
python train.py --training_data ./data --reg_rate 0.1

### select az account
az account list --output table
az account set --subscription <SUB_NAME>
az account show
az group show <RG_NAME>

### install azure machine learning 
az extension add -n ml --allow-preview true -y

* in azure/azure ai/machine learning studio
* in manage/compute : create a new compute that you need to insert in compute parameter in job.yml file
* <COMPUTE_INSTANCE_NAME>

### create compute cluster
az ml compute create \
  --name <nom_du_cluster> \
  --size <type_de_machine> \
  --min-instances <nombre_minimum_d_instances> \
  --max-instances <nombre_maximum_d_instances> \
  --resource-group <nom_du_groupe_de_ressources> \
  --workspace-name <nom_de_l_espace_de_travail> \
  --type amlcompute

### check compute cluster
az ml compute list \
  --resource-group <resource-group> \
  --workspace-name <workspace-name>

### exec data asset (in /01 folder path)
az ml data create --file yaml/data_asset.yml --workspace-name <WORKSPACE_NAME> --resource-group <RESOURCE_GROUP_NAME>

### exec job (in /01 folder path)
az ml job create --file yaml/job.yml --resource-group <RESOURCE_GROUP> --workspace-name <WORKSPACE_NAME>

### show job
az ml job show --name <JOB_NAME> --resource-group <RESOURCE_GROUP_NAME> --workspace-name <WORKSPACE_NAME>

### show datastore
az ml datastore list --workspace-name <WORKSPACE_NAME> --resource-group <RESOURCE_GROUP_NAME>

### create service principal with RBAC roles
az ad sp create-for-rbac --name "<service-principal-name>" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/<your-resource-group-name> \
  --sdk-auth

### show <client-id-du-service-principal>
az ad sp list --display-name "<service-principal-name>" --query "[].appId" -o tsv

------------------

git checkout master</br>
git pull origin master</br>
git checkout -b feature/dev</br>

git add .</br>
git commit -m 'blabla'</br>
git push origin feature/dev

------------------

### Variables après avoir un créer un managed identity pour le clustered compute
$MANAGED_IDENTITY_ID="<ID_DE_VOTRE_MANAGED_IDENTITY>"
$STORAGE_ACCOUNT_NAME="<NOM_DU_COMPTE_DE_STOCKAGE>"
$RESOURCE_GROUP="<GROUPE_DE_RESSOURCES_DU_COMPTE_DE_STOCKAGE>"

# Récupérer l'ID du compte de stockage
$STORAGE_ACCOUNT_ID=$(az storage account show --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query "id" -o tsv)

### Assigner le rôle "Storage Blob Data Contributor" pour ECRITURE
az role assignment create \
  --assignee $MANAGED_IDENTITY_ID \
  --role "Storage Blob Data Contributor" \
  --scope $STORAGE_ACCOUNT_ID

echo "Permissions assignées avec succès."

------------------

### for manual-trigger2.yml


## OPTIONAL

### add service principal to assigned user
az ml compute update 
  --name <nom-de-l-instance-de-calcul> \
  --resource-group <nom-du-groupe-de-ressources> \
  --workspace-name <nom-du-workspace-aml> \
  --add assigned_user=<client-id-du-service-principal>

### show if compute instance is ok
az ml compute show --name <nom-de-l-instance-de-calcul> \
 --resource-group <nom-du-groupe-de-ressources> \ 
 --workspace-name <nom-du-workspace-aml>

### add user to azure ml workspace
az ml workspace update --name <nom-du-workspace-aml> \
  --resource-group <nom-du-groupe-de-ressources> \
  --add assigned_user=<client-id-du-service-principal>

### RBAC on service principal to aml_workspace
### <sub_id> : az account show and go to "id" under "homeTenantId"
az role assignment create \
  --assignee <client-id-du-service-principal> \
  --role Contributor \
  --scope /subscriptions/<sub_id>/resourceGroups/d<rg_name>/providers/Microsoft.MachineLearningServices/workspaces/<aml_workspace_name>

### RBAC list
az role assignment list --assignee <service-principal-id> \
  --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>/computes/<compute-name>

### RBAC on service principal to compute instance
az role assignment create --assignee <service-principal-id> \
  --role Contributor \ 
  --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>/computes/<compute-name>

----------------




  