import ansible_runner
from utils.config import load_config


def run_monitoring_playbook():
    config = load_config()

    runner = ansible_runner.run(inventory=config['inventory_path'],
                                playbook=config['playbook_path'],
                                quiet=True
                                )

    results = []
    for event in runner.events:
        if event['event'] == 'runner_on_ok' and 'task' in event['event_data'] and event['event_data']['task'] == 'Usage Stats':
            # Only gather results for completed tasks
            task_name = event['event_data']['task']
            host = event['event_data']['host']
            result = event['event_data']['res']
            results.append({
                "task": task_name,
                "host": host,
                "result": result
            })

    result_dict = {item['host']: item for item in results}

    return dict(result_dict)