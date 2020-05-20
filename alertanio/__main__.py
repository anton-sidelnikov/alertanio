import logging
import sys

from alertanio.alerta_client import AlertaClient

LOGGER = logging.getLogger('alertanio')


def _main():
    try:
        AlertaClient().start()
    except KeyboardInterrupt:
        LOGGER.info("Alerta fetching stopped")
        sys.exit(0)
    # db = DBHelper(host="80.158.41.159", port="5432", user="postgres", password="qwerty12345!")
    # db.__connect__()
    # if not db.check_database_exist():
    #     db.query(TABLES['config'].params)
    #     db.query(TABLES['templates'].params)
    #     db.query(TABLES['topics'].params)
    # db.__disconnect__()


if __name__ == '__main__':
    _main()
