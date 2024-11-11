# Open-Monitor

**Open-Monitor** is an agentless monitoring program based on [Ansible](https://www.ansible.com/) that enables the collection of system and application metrics. These metrics are forwarded to [Prometheus](https://prometheus.io/) for visualization in [Grafana](https://grafana.com/). This tool provides a simple and effective way to implement a comprehensive monitoring solution without the need to install additional software agents on the monitored systems.

## Features
- **Agentless Monitoring**: Utilizes Ansible to collect metrics without requiring agents.
- **Integration with Prometheus**: Forwards collected data for storage and analysis.
- **Visualization in Grafana**: Seamless integration with Grafana dashboards for real-time visualizations.
- **Flexible and Extensible**: Customizable for different use cases and infrastructure environments.

## Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation
**Create application folder**
   ```bash
    mkdir open-monitor
    cd open-monitor
   ```

**Create data folder**
   ```bash
    mkdir data
    cd data
    mkdir monitoring_prometheus
    mkdir monitoring_ansible_exporter
   ```

**Get compose.yaml**:
   ```bash
    wget https://raw.githubusercontent.com/schneider-marco/open-monitor/compose.yaml
   ```
