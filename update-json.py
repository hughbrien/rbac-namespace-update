import json
import requests

# Example JSON data
#API_KEY=""
json_data = [
    {
        "actions": ["*"],
        "resources": [
            {
                "cluster": "k3s-ubuntu-hpb-cluster",
                "namespaces": [
                    "xlr8",
                    "pr-*",
                    "extraction",
                    "cloudconnector",
                ],
            }
        ],
    }
]

# Function to update a namespace element
def update_namespace(json_data, cluster_name, old_namespace, new_namespace):
    for entry in json_data:
        if "resources" in entry:
            for resource in entry["resources"]:
                if resource.get("cluster") == cluster_name:
                    namespaces = resource.get("namespaces", [])
                    if old_namespace in namespaces:
                        namespaces.remove(old_namespace)
                        namespaces.append(new_namespace)
    return json_data


def append_namespace(json_data, cluster_name, new_namespace):
    for entry in json_data:
        if "resources" in entry:
            for resource in entry["resources"]:
                if resource.get("cluster") == cluster_name:
                    namespaces = resource.get("namespaces", [])
                    namespaces.append(new_namespace)
    return json_data

# Function to delete a namespace element
def delete_namespace(json_data, cluster_name, namespace_to_delete):
    for entry in json_data:
        if "resources" in entry:
            for resource in entry["resources"]:
                if resource.get("cluster") == cluster_name:
                    namespaces = resource.get("namespaces", [])
                    if namespace_to_delete in namespaces:
                        namespaces.remove(namespace_to_delete)
    return json_data

def get_rbac_policy(policy_id):

    policy_entry = requests.get(f"https://api.komodor.com/mgmt/v1/rbac/policies/{policy_id}",
                            headers={"Content-Type":"application/json",
                                     "x-api-key": API_KEY})
    status_code = str(policy_entry.ok)
    print(policy_entry)
    json_results = policy_entry.json()
    result = {"http_return_code" : policy_entry.status_code,
              "http_status": status_code,
              "json_data": json_results }
    return result

def get_rbac_polcies():

    posting = requests.get("https://api.komodor.com/mgmt/v1/rbac/policies",
                            headers={"Content-Type":"application/json",
                                     "x-api-key":API_KEY})
    print(posting)
    status_code = str(posting.ok)
    for item in posting.json():
        print(item)

    result = {"http_return_code" : posting.status_code,
              "http_status": status_code }
    return result

def put_rbac_policy(policy_id, json_data):

    policy_entry = requests.post(f"https://api.komodor.com/mgmt/v1/rbac/policies/{policy_id}",
                            headers={"Content-Type":"application/json",
                                     "x-api-key":API_KEY},
                            data = json_data)

    status_code = str(policy_entry.ok)
    #print(policy_entry)
    json_results = policy_entry.json()
    result = {"http_return_code" : policy_entry.status_code,
              "http_status": status_code,
              "json_data": json_results }
    return result


# Update a namespace element
updated_json_data = update_namespace(json_data, "k3s-ubuntu-hpb-cluster", "pr-*", "new-namespace")

# Delete a namespace element
deleted_json_data = delete_namespace(json_data, "k3s-ubuntu-hpb-cluster", "new-namespace")

# Convert the updated/deleted JSON data back to a string
#updated_json_str = json.dumps(updated_json_data, indent=2)
#deleted_json_str = json.dumps(deleted_json_data, indent=2)

POLICY_ID = "64b2de24-74bb-4c13-af91-463c35b7a354"

api_result = get_rbac_policy(POLICY_ID)
policy_entry = api_result.get("json_data")
print(policy_entry)

added_namespace  = append_namespace(json_data, "k3s-ubuntu-hpb-cluster", "pr-33333333" )
print(added_namespace)
added_namespace  = append_namespace(json_data, "k3s-ubuntu-hpb-cluster", "pr-4444444" )
print(added_namespace)

put_result = put_rbac_policy(POLICY_ID, added_namespace)
print(put_result)












