#!/bin/bash

# Script to install Open Monitor with default configurations

# Create the application directory
echo "Creating application directory..."
mkdir -p open-monitor && cd open-monitor

# Clone repository
echo "Cloning repository..."
if [ ! -d "open-monitor" ]; then
  git clone https://github.com/schneider-marco/open-monitor.git
else
  echo "Repository already exists, skipping clone..."
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/monitoring_prometheus data/monitoring_ansible_exporter data/monitoring_ansible_exporter/ansible/sshkeys

# Copy default configurations
echo "Copying default configurations..."
for file in open-monitor/example/ansible_exporter/*; do
  if [ -e "data/monitoring_ansible_exporter/$(basename "$file")" ]; then
    echo "File $(basename "$file") already exists, skipping..."
  else
    cp -r "$file" data/monitoring_ansible_exporter/
  fi
done

if [ ! -f "data/monitoring_prometheus/prometheus.yml" ]; then
  cp open-monitor/example/prometheus/prometheus.yml data/monitoring_prometheus/prometheus.yml
else
  echo "File prometheus.yml already exists, skipping..."
fi

if [ ! -f "compose.yaml" ]; then
  cp open-monitor/compose.yaml .
else
  echo "File compose.yaml already exists, skipping..."
fi

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
