#!/bin/bash

# Script to install Open Monitor with default configurations

# Create the application directory
echo "Creating application directory..."
mkdir -p open-monitor && cd open-monitor

# Clone repository
echo "Cloning repository..."
git clone https://github.com/schneider-marco/open-monitor.git

# Create data directories
echo "Creating data directories..."
mkdir -p data/monitoring_prometheus data/monitoring_ansible_exporter data/monitoring_ansible_exporter/ansible/sshkeys

# Copy default configurations
echo "Copying default configurations..."
cp -r open-monitor/example/ansible_exporter/* data/monitoring_ansible_exporter/
cp open-monitor/example/prometheus/prometheus.yml data/monitoring_prometheus/prometheus.yml
cp open-monitor/compose.yaml .

# Remove repository folder
echo "Removing temporary files..."
rm -rf ./open-monitor

# Start Docker Compose in the background
echo "Starting Docker Compose in the background..."
docker compose up -d

# List running Docker containers
echo "Listing running Docker containers..."
docker ps

echo "Installation completed!"
