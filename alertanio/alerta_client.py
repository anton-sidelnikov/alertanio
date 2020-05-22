import logging
import os
import threading
import time
from datetime import datetime, timedelta

from alertaclient.api import Client

from alertanio.config.static_config import AlertaConfiguration, topic_map
from alertanio.database import DBHelper
from alertanio.zulip_client import ZulipClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

ALERTA_API_KEY = os.environ.get('ALERTA_API_KEY')
TIME_FILE = '/tmp/alertanio.time'


class AlertaClient:
    """Alerta client wrapper"""
    _alerta: Client = None
    _alerta_thread: threading.Thread

    def __init__(self, db_host, db_port, db_user, db_password, environment='prod'):
        self.alerta_api_key = ALERTA_API_KEY
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
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
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password
        )
        self.db.__connect__()
        self.alerta_config = AlertaConfiguration(
            *self.db.get(
                columns='*',
                table='configuration',
                condition=f"config_name='{self.environment}'")[0])
        self.templates = dict(self.db.get(
            columns='topic_name, template_data',
            table='templates',
            custom_clause='INNER JOIN topics ON templates.template_id=topics.templ_id'))
        self.topics = topic_map(self.db.get(table='topics', columns='topic_name, zulip_to, zulip_subject'))
        self.db.__disconnect__()

        self.zulip = ZulipClient(self.templates, self.topics)

    def write_last_run_time(self, time):
        with open(TIME_FILE, 'w') as file:
            file.write(time)

    def read_last_run_time(self):
        try:
            with open(TIME_FILE, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def start_fetching(self, auto_refresh=True, interval=5):
        """Start fetching updates from Alerta

            Date format for query: 2020-05-20T11:00:00.000Z
        """
        last_run = self.read_last_run_time()
        while auto_refresh:
            if last_run is not None:
                current_time = last_run
                last_run = None
            else:
                current_time = (datetime.utcnow() - timedelta(seconds=interval)).isoformat().split('.')[0] + '.000Z'
            alerts = self.alerta.get_alerts(query=[('from-date', current_time)])
            for alert in alerts:
                if not alert.repeat and alert.status not in ['ack', 'blackout', 'closed']:
                    self.zulip.post_receive(alert)
            self.write_last_run_time(current_time)
            time.sleep(interval)

    def start(self):
        """Start alerta"""

        self._alerta_thread = threading.Thread(
            target=(self.start_fetching()),
            name="Alerta-Thread")
        self._alerta_thread.start()
        self._alerta_thread.join()
