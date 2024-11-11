import ansible_runner
from utils.config import load_config
import os

def check_reachable_hosts() -> dict[str, bool]:
    config = load_config()

    inventory = os.path.abspath(config['inventory_path'])

    runner = ansible_runner.run(
        private_data_dir='.',
        inventory=inventory,
        module='ping',
        host_pattern='all',
        quiet=True
    )

    ping_results = {}

    for event in runner.events:
        event_data = event.get('event_data', {})
        hostname = event_data.get('host')

        if event.get('event') == 'runner_on_ok':  # Ping successful
            ping_results[hostname] = True
        elif event.get('event') == 'runner_on_unreachable':  # Host unreachable
            ping_results[hostname] = False
        elif event.get('event') == 'runner_on_failed':
            ping_results[hostname] = False


    return ping_results
