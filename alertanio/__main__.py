import logging

from alertanio.alerta_client import AlertaClient

LOG = logging.getLogger('alertanio')


def _main():
    client = AlertaClient()
    client.start()
    # db = DBHelper(host="80.158.41.159", port="5432", user="postgres", password="qwerty12345!")
    # db.__connect__()
    # if not db.check_database_exist():
    #     db.query(TABLES['config'].params)
    #     db.query(TABLES['templates'].params)
    #     db.query(TABLES['topics'].params)
    # db.__disconnect__()


if __name__ == '__main__':
    _main()
