from kubernetes import client, config, watch

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def handle_namespace_event(event):
    if event['object'].status.phase == 'Active':
        print(f"Namespace created: {event['object'].metadata.name}")
        add_namespace_to_policy(event['object'].metadata.name)
    elif event['object'].status.phase == 'Terminating':
        print(f"Namespace deleted:  {event['object'].metadata.name}")

def add_namespace_to_policy(namespace ):
    print(f"Calling Komodor API. Adding Namespace  {namespace} to Polcy")
    return

def delete_namespace_from_policy(namespace):
    print(f"Calling Komodor API. Deleting Namespace {namespace} from Policy ")
    return
    
class NamespaceHandler(FileSystemEventHandler):
    def on_created(self, event):
        handle_namespace_event(event)

    def on_deleted(self, event):
        handle_namespace_event(event)

def main():
    # Load Kubernetes configuration (use kubeconfig file or in-cluster config)
    config.load_kube_config()

    # Create a Kubernetes client
    v1 = client.CoreV1Api()

    # Watch for Namespace events
    w = watch.Watch()
    for event in w.stream(v1.list_namespace):
        handle_namespace_event(event)

if __name__ == "__main__":
    # Watch for changes in the /var/run/secrets/kubernetes.io/serviceaccount/ namespace folder
    observer = Observer()
    observer.schedule(NamespaceHandler(), "/var/run/secrets/kubernetes.io/serviceaccount/namespace")
    observer.start()

    try:
        main()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


#kubectl create ns namespace-demo1;kubectl create ns namespace-demo2;kubectl create ns namespace-demo3
#kubectl delete ns namespace-demo1;kubectl delete ns namespace-demo2;kubectl delete ns namespace-demo3

