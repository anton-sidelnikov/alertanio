import logging
import threading
import time
from datetime import datetime, timedelta

from alertaclient.api import Client

from alertanio.database import DBHelper
from alertanio.zulip_client import ZulipClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

TIME_FILE = '/tmp/alertanio.time'


class AlertaClient:
    """Alerta client wrapper"""
    _alerta: Client = None
    _alerta_thread: threading.Thread

    def __init__(self, args):
        """

        :param environment: exact environment that stored in db
        """
        self.alerta_api_key = args.alerta_api_key
        self.db_host = args.postgre_host
        self.db_port = args.postgre_port
        self.db_user = args.postgre_user
        self.db_password = args.postgre_password
        self.repeat_interval = args.repeat_interval
        self.environment = args.config_name

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
        self.alerta_config = self.db.get_alerta_configuration(self.environment)
        self.templates = self.db.get_zulip_templates()
        self.topics = self.db.get_topics()
        self.alerta_blackouts = self.db.get_blackouts()
        self.db.__disconnect__()
        self.environments_to_skip = self.alerta_config.skip_environment.split(',')

    def write_last_run_time(self, time):
        with open(TIME_FILE, 'w') as file:
            file.write(time)

    def read_last_run_time(self):
        try:
            with open(TIME_FILE, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def create_blackouts(self):
        if self.alerta_blackouts:
            current_blackouts = self.alerta.get_blackouts()
            for item in self.alerta_blackouts:
                for curr in current_blackouts:
                    if item.environment == curr.environment and item.service == curr.service and curr.status == 'active':
                        self.alerta_blackouts.remove(item)
            for item in self.alerta_blackouts:
                self.alerta.create_blackout(
                    environment=item.environment,
                    service=item.service,
                    resource=item.resource,
                    event=item.event_name,
                    group=item.group_name,
                    tags=item.tags,
                    start=item.start_time,
                    duration=item.duration,
                    text=item.text)

    def start_fetching(self, auto_refresh=True, interval=5):
        """Start fetching updates from Alerta

        Date format for query: 2020-05-20T11:00:00.000Z

        :param interval: interval between calling Alerta service in seconds
        :return:
        """
        self.create_blackouts()
        self.zulip = ZulipClient(self.templates, self.topics)
        last_run = self.read_last_run_time()
        while auto_refresh:
            if last_run is not None:
                current_time = last_run
                last_run = None
            else:
                current_time = get_current_time(interval)
            alerts = self.alerta.get_alerts(query=[('from-date', current_time)])
            for alert in alerts:
                if alert.status not in ['ack', 'blackout', 'closed'] and \
                        alert.environment not in self.environments_to_skip and \
                        delta_minutes(alert.last_receive_time) >= self.repeat_interval:
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


def delta_minutes(last_receive_time) -> int:
    if last_receive_time is None:
        return 0
    return (datetime.utcnow().timestamp() - last_receive_time.timestamp()) / 60


def get_current_time(interval):
    return (datetime.utcnow() - timedelta(seconds=interval)).isoformat().split('.')[0] + '.000Z'
