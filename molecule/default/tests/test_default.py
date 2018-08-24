"""Defautl test module."""
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_group(host):
    """Test group."""
    group = host.group("prometheus")
    assert group.exists


def test_user(host):
    """Test user."""
    user = host.user("prometheus")
    assert user.exists
    assert "prometheus" in user.groups


def test_config(host):
    """Test config."""
    config = host.file("/etc/prometheus/prometheus.yml")
    assert config.exists
    assert config.is_file
    assert config.user == "root"
    assert config.group == "prometheus"
    assert config.mode == 0o640


def test_service(host):
    """Test service."""
    service = host.service("prometheus")
    assert service.is_enabled
    assert service.is_running


def test_socket(host):
    """Test socket connection."""
    socket = host.socket("tcp://0.0.0.0:9090")
    assert socket.is_listening


def test_log(host):
    """Test log."""
    config = host.file("/var/lib/prometheus/prometheus.log")
    assert config.exists
    assert config.is_file


def test_version(host):
    """Test version."""
    version = os.getenv('PROMETHEUS', "2.3.2")
    out = host.run("/opt/prometheus/prometheus --version").stderr
    assert "prometheus, version " + version in out
