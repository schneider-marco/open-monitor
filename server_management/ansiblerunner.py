import ansible_runner
from utils.config import load_config
import os
import json
from utils.logger import logger

def format_json(data):
    formatted_data = {}

    for entry in data:
        for host, details in entry.items():
            task = details.get("task")
            msg = details.get("result", {}).get("msg")

            # Initialize host entry in formatted_data if it doesn't exist
            if host not in formatted_data:
                formatted_data[host] = {}

            # Assign the msg block under the respective task for the host
            if task and msg is not None:
                formatted_data[host][task] = msg

    return formatted_data


def run_all_playbooks():

    data = []
    config = load_config()

    playbook_path = os.path.abspath(config['playbook_path'])
    inventory = os.path.abspath(config['inventory_path'])

    counter = 0

    for file_name in os.listdir(playbook_path):
        file_path = os.path.abspath(os.path.join(playbook_path, file_name))

        if not (file_name.endswith('.yml') or file_name.endswith('.yaml')):
            logger.debug(f"Skipping non-YAML file: {file_name}")
            continue

        logger.debug(f"Starting Playbook: {file_path}")

        runner = ansible_runner.run(inventory=inventory,
                                    playbook=file_path,
                                    quiet=True
                                    )

        results = []
        for event in runner.events:
            if event['event'] == 'runner_on_ok':
                task_name = event['event_data']['task']
                host = event['event_data']['host']
                result = event['event_data']['res']
                results.append({
                    "task": task_name,
                    "host": host,
                    "result": result
                })

        result_dict = {item['host']: item for item in results}
        data.append(result_dict)
        counter += 1

    return format_json(data)
