import logging
import os
import sys
from argparse import ArgumentParser

from alertanio.alerta_client import AlertaClient

LOGGER = logging.getLogger('alertanio')


def _config():
    arg_p = ArgumentParser(description='Alerta client for fetching new alerts and send it to Zulip')
    arg_p.add_argument('--postgre_host', default=os.environ.get('DB_HOST'), help='postgres host')
    arg_p.add_argument('--postgre_port', default=os.environ.get('DB_PORT'), help='postgres port')
    arg_p.add_argument('--postgre_user', default=os.environ.get('DB_USER'), help='postgres user')
    arg_p.add_argument('--postgre_password', default=os.environ.get('DB_PASSWORD'), help='postgres password')
    arg_p.add_argument('--repeat_interval', default=5, help='interval for repeat alerts in minutes')
    arg_p.add_argument('--config_name', default='prod', help='name of calerta config stored in database')
    arg_p.add_argument('--alerta_api_key', default=os.environ.get('ALERTA_API_KEY'), help='api key for alerta')

    args = arg_p.parse_args()
    return args


def _main():
    args = _config()
    try:
        AlertaClient(args).start()
    except KeyboardInterrupt:
        LOGGER.info("Alerta fetching stopped")
        sys.exit(0)


if __name__ == '__main__':
    _main()
