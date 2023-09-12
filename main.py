from kubernetes import client, config, watch

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import socket
import requests

def handle_namespace_event(event):
    if event['object'].status.phase == 'Active':
        add_namespace_to_policy(event['object'].metadata.name)
    elif event['object'].status.phase == 'Terminating':
        delete_namespace_from_policy({event['object'].metadata.name})


def add_namespace_to_policy(namespace):
    print(f"Calling Komodor API. Adding Namespace  {namespace} to Polcy")
    return

def delete_namespace_from_policy(namespace):
    print(f"#  #  #  #  #  #  #  #  Delete Namesapce {namespace} #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #")
    print(f"Calling Komodor API. Deleting Namespace {namespace} from Policy ")
    return


def call_rbac_api(namespace):

    posting = requests.get("https://api.komodor.com/mgmt/v1/rbac/policies/64b2de24-74bb-4c13-af91-463c35b7a354",
                            headers={"Content-Type":"application/json",
                                     "x-api-key":"32f6511d-fdbd-4673-93f9-7c505c8b06b8"})

    print(posting)
    status_code = str(posting.ok)

    result = {"http_return_code" : posting.status_code,
              "hostname": "shipping",
              "http_status": status_code }
    return result


class NamespaceHandler(FileSystemEventHandler):
    def on_created(self, event):
        handle_namespace_event(event)

    def on_deleted(self, event):
        handle_namespace_event(event)

def main():
    # Load Kubernetes configuration (use kubeconfig file or in-cluster config)
    print("Loading up kubeconfig")
    config.load_kube_config(config_file="./k3s-context.yaml")

    # Create a Kubernetes client
    print("Loading up kubeconfig")
    v1 = client.CoreV1Api()

    # Watch for Namespace events
    w = watch.Watch()
    for event in w.stream(v1.list_namespace):
        #print(event)
        handle_namespace_event(event)

if __name__ == "__main__":
    # Watch for changes in the /var/run/secrets/kubernetes.io/serviceaccount/ namespace folder
    print("Creating and Starting Observer")
    observer = Observer()
    observer.schedule(NamespaceHandler(), "./serviceaccount")
    observer.start()

    try:
        print("Calling main()")
        main()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

#kubectl create ns namespace-demo1;kubectl create ns namespace-demo2;kubectl create ns namespace-demo3
#kubectl delete ns namespace-demo1;kubectl delete ns namespace-demo2;kubectl delete ns namespace-demo3

