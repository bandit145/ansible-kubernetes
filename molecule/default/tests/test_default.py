import os
import kubernetes as k8s
import testinfra.utils.ansible_runner
# import requests
import logging
import subprocess

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')

k8s.config.load_kube_config('/tmp/kube_admin.conf')


def service_enabled(host, service):
    assert host.service(service).is_running
    assert host.service(service).is_enabled


def test_docker_service(host):
    service_enabled(host, 'docker')


def test_kubelet_running(host):
    service_enabled(host, 'kubelet')


# TODO: figure out why this returns three when a node is down and shoulr report 2 running
def test_flannel_deployment():
    v1_api = k8s.client.CoreV1Api()
    flannel_pods = v1_api.list_pod_for_all_namespaces(field_selector='status.phase=Running,', label_selector='app=flannel')
    logging.info(len(flannel_pods.items))
    assert len(flannel_pods.items) == 3


def test_linkerd():
    check = subprocess.run('linkerd check --kubeconfig /tmp/kube_admin.conf', shell=True)
    assert check.returncode == 0


def end_to_end_test():
    pass
