"""Defautl test module."""
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9090")
    assert s.is_listening


def test_version(host):
    version = os.getenv("PROMETHEUS", "2.3.2")
    out = host.run("/opt/prometheus/prometheus --version").stderr
    assert "prometheus, version " + version in out
