from prometheus_client import Gauge, CollectorRegistry, start_http_server
import threading

registry = CollectorRegistry()
cpu_usage_gauge = Gauge('cpu_usage', 'CPU Usage percentage', ['host'], registry=registry)
ram_usage_gauge = Gauge('ram_usage', 'RAM Usage percentage', ['host'], registry=registry)
disk_usage_gauge = Gauge('disk_usage', 'Disk Usage percentage', ['host'], registry=registry)
network_received_gauge = Gauge('network_received_bytes', 'Network Received Bytes', ['host'], registry=registry)
network_sent_gauge = Gauge('network_sent_bytes', 'Network Sent Bytes', ['host'], registry=registry)
running_processes_gauge = Gauge('running_processes', 'Number of running processes', ['host'], registry=registry)
upstate_gauge = Gauge('upstate', 'Upstate of all Clients', ['host'], registry=registry)
cpu_load_1m_gauge = Gauge('cpu_load_1m', 'Average CPU Load (1 minute)', ['host'], registry=registry)
cpu_load_5m_gauge = Gauge('cpu_load_5m', 'Average CPU Load (5 minutes)', ['host'], registry=registry)
cpu_load_15m_gauge = Gauge('cpu_load_15m', 'Average CPU Load (15 minutes)', ['host'], registry=registry)
free_disk_space_gauge = Gauge('free_disk_space', 'Free Disk Space in GB', ['host'], registry=registry)
system_uptime_gauge = Gauge('system_uptime_minutes', 'System Uptime in Minutes', ['host'], registry=registry)


def start_prometheus_server(port=8000):
    """Start the Prometheus HTTP server on a separate thread."""
    thread = threading.Thread(target=start_http_server, args=(port,), kwargs={'registry': registry})
    thread.daemon = True  # Daemonize the thread to allow program to exit
    thread.start()
    print(f"Prometheus metrics server started on port {port}")


def update_metrics(data):
    """
    Update the metrics with new data.

    Args:
        data (dict): Dictionary containing metrics for multiple hosts.
    """

    host_metrics = data[1]
    for host, host_data in host_metrics.items():
        result = host_data['result']['msg']

        # Parse values and update the corresponding gauges
        for item in result:
            if "CPU Usage" in item:
                cpu_usage = float(item.split(": ")[1].strip('%'))
                cpu_usage_gauge.labels(host=host).set(cpu_usage)
            elif "RAM Usage" in item:
                ram_usage = float(item.split(": ")[1].strip('%'))
                ram_usage_gauge.labels(host=host).set(ram_usage)
            elif "Disk Space Used" in item:
                disk_usage = float(item.split(": ")[1].strip('%'))
                disk_usage_gauge.labels(host=host).set(disk_usage)
            elif "Network Received Bytes" in item:
                network_received = int(item.split(": ")[1])
                network_received_gauge.labels(host=host).set(network_received)
            elif "Network Sent Bytes" in item:
                network_sent = int(item.split(": ")[1])
                network_sent_gauge.labels(host=host).set(network_sent)
            elif "Running Processes" in item:
                running_processes = int(item.split(": ")[1])
                running_processes_gauge.labels(host=host).set(running_processes)
            elif "Average CPU Load" in item:
                load_values = item.split(": ")[1].strip().split(" ")
                cpu_load_1m = float(load_values[0])
                cpu_load_5m = float(load_values[1])
                cpu_load_15m = float(load_values[2])
                cpu_load_1m_gauge.labels(host=host).set(cpu_load_1m)
                cpu_load_5m_gauge.labels(host=host).set(cpu_load_5m)
                cpu_load_15m_gauge.labels(host=host).set(cpu_load_15m)
            elif "Free Disk Space" in item:
                # Convert free disk space to GB by removing the 'G' and casting to float
                free_disk_space = float(item.split(": ")[1].strip('G'))
                free_disk_space_gauge.labels(host=host).set(free_disk_space)
            elif "System Uptime" in item:
                # Convert uptime from "Hours:Minutes" to total minutes
                hours, minutes = map(int, item.split(": ")[1].split(":"))
                uptime_minutes = hours * 60 + minutes
                system_uptime_gauge.labels(host=host).set(uptime_minutes)


def update_upstate_metrics(upstate_data):
    """
    Update upstate metrics for each client with a labeled metric.

    Args:
        upstate_data (dict): Dictionary containing upstate information for each client.
    """
    for client_name, is_up in upstate_data[0]["upstate"].items():
        # Set the labeled upstate gauge for each host (1 if True, 0 if False)
        upstate_gauge.labels(host=client_name).set(1 if is_up else 0)