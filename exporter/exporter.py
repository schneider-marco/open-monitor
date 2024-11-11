from prometheus_client import Gauge, start_http_server
import re
from utils import logger

gauges = {}

# uptime gauges
upstate_gauge = Gauge('upstate', 'Upstate of all Clients', ['node'])

# Define hardcoded gauges for disk metrics
disk_size_gauge = Gauge('disk_size', 'Disk size in GB', ['node', 'source'])
disk_used_gauge = Gauge('disk_used', 'Disk used in GB', ['node', 'source'])
disk_available_gauge = Gauge('disk_available', 'Disk available in GB', ['node', 'source'])

# Define hardcoded gauges for network usage metrics with source
network_received_packets_gauge = Gauge('network_received_packets', 'Received packets for network interface', ['node', 'source'])
network_sent_packets_gauge = Gauge('network_sent_packets', 'Sent packets for network interface', ['node', 'source'])
network_received_bytes_gauge = Gauge('network_received_bytes', 'Received bytes for network interface', ['node', 'source'])
network_sent_bytes_gauge = Gauge('network_sent_bytes', 'Sent bytes for network interface', ['node', 'source'])

def sanitize_metric_name(name):
    """
    Sanitize the metric name to fit Prometheus naming conventions.
    Replace non-alphanumeric characters with underscores.
    """
    return re.sub(r'\W|^(?=\d)', '_', name)

def create_or_get_gauge(metric_name, description, labels):
    """
    Creates a new Gauge if it doesn't exist or retrieves the existing one.
    """
    if metric_name not in gauges:
        gauges[metric_name] = Gauge(metric_name, description, labels)
    return gauges[metric_name]

def process_disk_data(node_name, disk_info):
    """
    Process disk information in a specific format.
    """
    for disk in disk_info:
        source = disk["source"]
        disk_size_gauge.labels(node=node_name, source=source).set(float(disk["size"]))
        disk_used_gauge.labels(node=node_name, source=source).set(float(disk["used"]))
        disk_available_gauge.labels(node=node_name, source=source).set(float(disk["available"]))

def process_network_data(node_name, network_info):
    """
    Process network usage information in a specific format, adding source for each interface.
    """
    for interface in network_info:
        source = interface["source"]
        network_received_packets_gauge.labels(node=node_name, source=source).set(float(interface["received_packets"]))
        network_sent_packets_gauge.labels(node=node_name, source=source).set(float(interface["sent_packets"]))
        network_received_bytes_gauge.labels(node=node_name, source=source).set(float(interface["received_bytes"]))
        network_sent_bytes_gauge.labels(node=node_name, source=source).set(float(interface["sent_bytes"]))

def process_data(node_name, metric_prefix, data):
    """
    Recursively process JSON data to create and update Prometheus metrics.
    Only numeric values will be converted to Prometheus metrics.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            # Special handling for disk and network information
            if key == "disk_information_in_GB":
                process_disk_data(node_name, value)
            elif key == "network_usage":
                process_network_data(node_name, value)
            else:
                # Create a new metric prefix based on the current key
                new_metric_prefix = sanitize_metric_name(key)
                process_data(node_name, new_metric_prefix, value)
    elif isinstance(data, list):
        for item in data:
            process_data(node_name, metric_prefix, item)
    else:
        # Handle single numeric values (int, float) or numeric strings in the JSON
        try:
            # Attempt to convert value to a float; skip if it raises a ValueError
            value = float(data)
            metric_name = sanitize_metric_name(metric_prefix)
            gauge = create_or_get_gauge(metric_name, f"Dynamic metric for {metric_name}", ['node'])
            gauge.labels(node=node_name).set(value)
        except (ValueError, TypeError):
            # Log skipped non-numeric values
            logger.warn(f"Skipping non-numeric value for metric '{metric_prefix}': {data}")

def update_metrics(data):
    """
    Update all metrics based on the JSON structure provided in `data`.
    """
    for node_name, node_data in data.items():
        process_data(node_name, node_name, node_data)


def update_upstate_metrics(upstate_data):
    """
    Update upstate metrics for each client with a labeled metric.

    Args:
        upstate_data (dict): Dictionary containing upstate information for each client.
    """
    for client_name, is_up in upstate_data.items():
        # Set the labeled upstate gauge for each host (1 if True, 0 if False)
        upstate_gauge.labels(node=client_name).set(1 if is_up else 0)

def start_server():
    # Startet den HTTP-Server auf Port 8000
    start_http_server(8000)