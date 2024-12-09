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

### exec data asset (in /01 folder path)
az ml data create --file yaml/data_asset.yml --workspace-name <WORKSPACE_NAME> --resource-group <RESOURCE_GROUP_NAME>

### exec job (in /01 folder path)
az ml job create --file yaml/job.yml --resource-group <RESOURCE_GROUP> --workspace-name <WORKSPACE_NAME>

### create service principal with RBAC roles
  az ad sp create-for-rbac --name "<service-principal-name>" \
    --role contributor \
    --scopes /subscriptions/<subscription-id>/resourceGroups/<your-resource-group-name> \
    --sdk-auth