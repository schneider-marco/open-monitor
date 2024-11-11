import argparse
from server_management import *
import json
from Exporter import *
import time
from utils import logger
import threading

def main() -> None:
    parser = argparse.ArgumentParser(description="Open Command & Control")
    parser.add_argument('--monitor', action='store_true', help="Show Monitoring")
    parser.add_argument('--check-hosts', action='store_true', help="Show host connectivity")
    parser.add_argument('--add-server', nargs=2, metavar=('<hostname>', '<ip>'), help="Add new Server")

    args = parser.parse_args()

    if args.add_server:
        hostname, ip = args.add_server
        add_server_to_inventory(hostname, ip)
        exit(0)

    if args.monitor:
        print(json.dumps(run_all_playbooks(), indent=4))
        exit(0)

    if args.check_hosts:
        print(json.dumps(check_reachable_hosts(), indent=4))
        exit(0)


    logger.info("No arguments passed -> starting continuous export...")
    logger.info("Prometheus metrics available at http://localhost:8000/metrics")

    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # Damit der Thread sich beendet, wenn das Hauptprogramm beendet wird
    server_thread.start()

    while True:
        try:
            upstate_data = check_reachable_hosts()
            logger.debug(f"Upstate Data Received: {json.dumps(upstate_data, indent=4)}")
            monitoring_data = run_all_playbooks()
            logger.debug(f"Monitoring Data Received: {json.dumps(monitoring_data, indent=4)}")
            update_metrics(monitoring_data)
            update_upstate_metrics(upstate_data)
            time.sleep(60)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            time.sleep(5)  # Eine kurze Pause, bevor erneut versucht wird


if __name__ == '__main__':
    main()
