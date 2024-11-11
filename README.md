# Open-Monitor

**Open-Monitor** is an agentless monitoring program based on [Ansible](https://www.ansible.com/) that enables the collection of system and application metrics. These metrics are forwarded to [Prometheus](https://prometheus.io/) for visualization in [Grafana](https://grafana.com/). This tool provides a simple and effective way to implement a comprehensive monitoring solution without the need to install additional software agents on the monitored systems.

## Features
- **Agentless Monitoring**: Utilizes Ansible to collect metrics without requiring agents.
- **Integration with Prometheus**: Forwards collected data for storage and analysis.
- **Visualization in Grafana**: Seamless integration with Grafana dashboards for real-time visualizations.
- **Flexible and Extensible**: Customizable for different use cases and infrastructure environments via ansible playbooks

## Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation (with default configs)
**Create application folder**
   ```bash
    mkdir open-monitor && cd open-monitor
   ```
**Get Files**:
   ```bash
    git clone https://github.com/schneider-marco/open-monitor.git
   ```

**Create data folder**
   ```bash
  mkdir -p data/monitoring_prometheus data/monitoring_ansible_exporter data/monitoring_ansible_exporter/ansible/sshkeys

   ```

**Copy default configs**
   ```bash
cp -r open-monitor/example/ansible_exporter/* data/monitoring_ansible_exporter/ && cp open-monitor/example/prometheus/prometheus.yml data/monitoring_prometheus/prometheus.yml && cp open-monitor/compose.yaml . && rm -rf ./open-monitor
   ```

**Run compose in background**:
   ```bash
    docker compose up -d
   ```

**List running docker**:
   ```bash
    docker ps
   ```

## Advanced Installation (without default config)


## Update
**Upgrade to latest version**
   ```bash
    docker compose pull && docker compose up -d --force-recreate
   ```