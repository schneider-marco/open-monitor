
# Open-Monitor

**Open-Monitor** is an agentless, Ansible-based monitoring program that collects system and application metrics without needing agents on the monitored systems. The collected data is forwarded to [Prometheus](https://prometheus.io/) for storage and then visualized in real-time with [Grafana](https://grafana.com/), making it a powerful, easy-to-deploy monitoring solution.

## Features
- **Agentless Monitoring**: Uses Ansible to collect metrics without requiring agents on target systems.
- **Prometheus Integration**: Sends all collected metrics to Prometheus for efficient data storage and analysis.
- **Real-Time Visualization**: Integrates seamlessly with Grafana, enabling real-time visualizations through customizable dashboards.
- **Flexible and Extensible**: Easily adaptable for various use cases and infrastructures using Ansible playbooks.

## Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Quick Installation (with Setup Script)
To quickly set up Open-Monitor, use the following command:

```bash
curl -s https://raw.githubusercontent.com/schneider-marco/open-monitor/refs/heads/main/setup.sh | bash
```

This script will create the necessary folder structure and files for Open-Monitor.

---

## Manual Installation
If you prefer a manual setup, follow these steps:

### 1. Create Application Folder
   ```bash
   mkdir open-monitor && cd open-monitor
   ```

### 2. Clone Repository
   ```bash
   git clone https://github.com/schneider-marco/open-monitor.git
   ```

### 3. Create Data Folders
   ```bash
   mkdir -p data/monitoring_prometheus data/monitoring_ansible_exporter data/monitoring_ansible_exporter/ansible/sshkeys
   ```

### 4. Copy Default Configurations and Clean Up
   ```bash
   cp -r open-monitor/example/ansible_exporter/* data/monitoring_ansible_exporter/    && cp open-monitor/example/prometheus/prometheus.yml data/monitoring_prometheus/prometheus.yml    && cp open-monitor/compose.yaml .    && rm -rf ./open-monitor
   ```

### 5. Start Docker Compose in Detached Mode
   ```bash
   docker compose up -d
   ```

### 6. Verify Running Docker Containers
   ```bash
   docker ps
   ```

---

## Adding a New Client

To monitor additional systems, follow these steps:

1. **Add SSH Key**: Place the SSH key for each client in the following directory:
   ```plaintext
   open-monitor/data/monitoring_ansible_exporter/ansible/sshkeys/
   ```

2. **Add Client to Inventory**: Specify the client details in the inventory file:
   ```plaintext
   open-monitor/data/monitoring_ansible_exporter/ansible/inventory/inventory.ini
   ```

3. **Install SSH Key on Client**: Install the SSH key on the client for secure monitoring.


---

Enjoy streamlined, agentless monitoring with Open-Monitor!
