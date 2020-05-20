import logging
import os
import threading
import time
from datetime import datetime

from alertaclient.api import Client

from alertanio.config.static_config import DATABASE, AlertaConfiguration
from alertanio.database import DBHelper

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

ALERTA_API_KEY = os.environ.get('ALERTA_API_KEY')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


class AlertaClient:
    """Alerta client wrapper"""
    _alerta: Client = None
    _alerta_thread: threading.Thread

    def __init__(self, config=DATABASE['db_config'], environment='prod'):
        self.config = config.params
        self.alerta_api_key = ALERTA_API_KEY
        self.db_password = DB_PASSWORD
        self.environment = environment

        self.load_configuration()

    @property
    def alerta(self):
        """Return alerta instance, create new if missing"""
        if self._alerta is None:
            LOGGER.warning('No alerta exist. Create client.')
            self._alerta = Client(
                endpoint=self.alerta_config.alerta_endpoint,
                debug=self.alerta_config.alerta_debug,
                timeout=self.alerta_config.alerta_timeout,
                key=self.alerta_api_key
            )
        return self._alerta

    def load_configuration(self):
        """Load/Re-Load Alerta configuration and Topics templates"""
        self.db = DBHelper(
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            password=self.db_password
        )
        self.db.__connect__()
        self.alerta_config = AlertaConfiguration(
            *(self.db.get(
                columns='*',
                table='configuration',
                condition=f"config_name='{self.environment}'")[0]))
        self.TEMPLATES = dict(self.db.get(
            columns='topic_name, template_data',
            table='templates',
            custom_clause='INNER JOIN topics ON templates.template_id=topics.templ_id'))
        self.db.__disconnect__()

    def start_fetching(self, auto_refresh=True, interval=5):
        """Start fetching updates from Alerta

            Date format for query: 2020-05-20T11:00:00.000Z
        """

        while auto_refresh:
            alerts = self.alerta.get_alerts(
                query=[('from-date', datetime.utcnow().isoformat().split('.')[0] + '.000Z')])
            for alert in alerts:
                if not alert.repeat and alert.status not in ['ack', 'blackout', 'closed']:
                    print("1")
            time.sleep(interval)
        time.sleep(5)

    def start(self):
        """Start alerta"""

        self._alerta_thread = threading.Thread(
            target=(self.start_fetching()),
            name="Alerta-Thread")
        self._alerta_thread.start()
        self._alerta_thread.join()
