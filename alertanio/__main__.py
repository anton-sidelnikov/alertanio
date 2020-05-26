import logging
import os
import sys

from alertanio.alerta_client import AlertaClient

LOGGER = logging.getLogger('alertanio')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


def _main():
    try:
        AlertaClient(db_host=DB_HOST, db_port=DB_PORT, db_user=DB_USER, db_password=DB_PASSWORD).start()
    except KeyboardInterrupt:
        LOGGER.info("Alerta fetching stopped")
        sys.exit(0)


if __name__ == '__main__':
    _main()
