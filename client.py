
import requests


def get_rbac_policy(policy_id):

    policy_entry = requests.get(f"https://api.komodor.com/mgmt/v1/rbac/policies/{policy_id}",
                            headers={"Content-Type":"application/json",
                                     "x-api-key":""})
    status_code = str(policy_entry.ok)
    print(policy_entry)
    json_results = policy_entry.json()
    print(json_results["id"])
    print(json_results["name"])
    statements = json_results["statements"]
    resources = statements[0]["resources"]
    namespaces = resources[0]["namespaces"]
    print(namespaces)

    result = {"http_return_code" : policy_entry.status_code,
              "http_status": status_code }
    return result

def get_rbac_polcies():

    posting = requests.get("https://api.komodor.com/mgmt/v1/rbac/policies",
                            headers={"Content-Type":"application/json",
                                     "x-api-key":"69b97c67-fa11-4125-8606-7ccc62d9bd53"})
    print(posting)
    status_code = str(posting.ok)
    for item in posting.json():
        print(item)

    result = {"http_return_code" : posting.status_code,
              "http_status": status_code }
    return result

if __name__ == "__main__":
    get_rbac_polcies()
    get_rbac_policy("64b2de24-74bb-4c13-af91-463c35b7a354")

