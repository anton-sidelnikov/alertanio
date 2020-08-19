import logging
import threading
import time
from datetime import datetime, timedelta

from alertaclient.api import Client

from alertanio.database import DBHelper
from alertanio.zulip_client import ZulipClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

TIME_FILE = 'alertanio.time'


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
                endpoint='https://alerts.eco.tsi-dev.otc-service.com/',
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

        :param interval: interval between calling Alerta service in seconds
        :return:
        """
        # self.zulip = ZulipClient(self.templates, self.topics)
        body = {
            "alert": {
                "attributes": {},
                "correlate": [],
                "createTime": "2020-08-09T03:23:10.893Z",
                "customer": None,
                "duplicateCount": 81,
                "environment": "prod",
                "event": "Failure",
                "group": "Misc",
                "history": [
                    {"event": "Failure", "href": "/alert/f389b541-9b91-42fa-8251-7dfdf0066c05",
                     "id": "f389b541-9b91-42fa-8251-7dfdf0066c05", "severity": "critical", "status": "open", "text": "",
                     "type": "new", "updateTime": "2020-08-09T03:23:10.893Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/c52c52f5-0d03-429d-8484-1db559ca4dfd",
                     "id": "c52c52f5-0d03-429d-8484-1db559ca4dfd", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-09T21:00:16.832Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/65b6d537-5063-4aa6-b65a-b921781646a4",
                     "id": "65b6d537-5063-4aa6-b65a-b921781646a4", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-10T01:43:00.785Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/138e0b98-ec73-484c-b2f4-1962dedfd61c",
                     "id": "138e0b98-ec73-484c-b2f4-1962dedfd61c", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-10T10:27:46.855Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/b72a85ae-c5a3-4401-b949-c56593d28f86",
                     "id": "b72a85ae-c5a3-4401-b949-c56593d28f86", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-10T10:27:47.860Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/08c9484f-47bf-40a7-95e1-3acfa5bfc9f2",
                     "id": "08c9484f-47bf-40a7-95e1-3acfa5bfc9f2", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-10T16:38:21.304Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/d7814290-7643-4a0f-92ba-d8f22204142d",
                     "id": "d7814290-7643-4a0f-92ba-d8f22204142d", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-10T20:35:45.406Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/504f7df6-bc90-4593-8824-833cd7ddfbdf",
                     "id": "504f7df6-bc90-4593-8824-833cd7ddfbdf", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T03:07:09.878Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/9a6bb698-241e-42dd-be99-ad10bf1e0f2c",
                     "id": "9a6bb698-241e-42dd-be99-ad10bf1e0f2c", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T03:23:02.017Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/8238f895-3fc2-4b9a-8f65-72cec78c2680",
                     "id": "8238f895-3fc2-4b9a-8f65-72cec78c2680", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T08:43:04.975Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/fe46b6f0-4301-4766-ae7a-2ae7fc3da8f4",
                     "id": "fe46b6f0-4301-4766-ae7a-2ae7fc3da8f4", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T09:53:24.743Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/d8fa481b-d673-479e-b3cf-e75bd2085ce0",
                     "id": "d8fa481b-d673-479e-b3cf-e75bd2085ce0", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T10:37:21.207Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/262f7cf6-50a5-4dbd-9653-085eea7af50b",
                     "id": "262f7cf6-50a5-4dbd-9653-085eea7af50b", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T11:00:17.028Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/5fbcf06d-0c93-41f7-9643-5f0f9cc344b0",
                     "id": "5fbcf06d-0c93-41f7-9643-5f0f9cc344b0", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T11:27:45.571Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/7b404310-423b-4f64-a20f-47160718c979",
                     "id": "7b404310-423b-4f64-a20f-47160718c979", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T11:47:45.248Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/24ab60d4-bfe3-4116-8da8-124bae2236ff",
                     "id": "24ab60d4-bfe3-4116-8da8-124bae2236ff", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T13:52:39.573Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/58d399f5-08b5-48cf-a9ac-9ed003ff2803",
                     "id": "58d399f5-08b5-48cf-a9ac-9ed003ff2803", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T17:23:46.683Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/b17dbe39-10b0-48e4-a4b2-1d4f5347be37",
                     "id": "b17dbe39-10b0-48e4-a4b2-1d4f5347be37", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T19:18:08.133Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/9c26109d-4b77-481e-9b9e-8d4c9d9f9f72",
                     "id": "9c26109d-4b77-481e-9b9e-8d4c9d9f9f72", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T19:28:47.447Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/e53dbfbe-8e13-4e55-8e6b-39708f9a0729",
                     "id": "e53dbfbe-8e13-4e55-8e6b-39708f9a0729", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T22:19:07.945Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/a6d61f21-f164-4680-b70e-941df73c947b",
                     "id": "a6d61f21-f164-4680-b70e-941df73c947b", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-11T23:48:57.576Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/c91bc553-926e-4f07-82d4-3f3cdccb5ea3",
                     "id": "c91bc553-926e-4f07-82d4-3f3cdccb5ea3", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-12T00:00:17.591Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/6ef1ff0a-4619-456f-bc01-e8050ab8b2d2",
                     "id": "6ef1ff0a-4619-456f-bc01-e8050ab8b2d2", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-12T00:29:00.234Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/f61acac5-0f47-4f40-91a9-ec254c82a384",
                     "id": "f61acac5-0f47-4f40-91a9-ec254c82a384", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-12T00:43:10.954Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/f48c7327-b9eb-41e5-9d26-cdfc662e2e98",
                     "id": "f48c7327-b9eb-41e5-9d26-cdfc662e2e98", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-12T01:37:09.355Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/62e21e46-c9f4-4fdf-af8f-acd2153e464d",
                     "id": "62e21e46-c9f4-4fdf-af8f-acd2153e464d", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-12T02:20:24.575Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/01aa4fb0-fc55-4c72-9fe0-6ffcf65c2192",
                     "id": "01aa4fb0-fc55-4c72-9fe0-6ffcf65c2192", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-12T02:35:23.297Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/800d321e-19e2-4122-9831-39e0a1155bb8",
                     "id": "800d321e-19e2-4122-9831-39e0a1155bb8", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-12T10:00:14.158Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/4c214c55-5fd9-4d51-b99d-65cad15cb772",
                     "id": "4c214c55-5fd9-4d51-b99d-65cad15cb772", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-13T06:00:15.770Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/alarms -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
                    {"event": "Failure", "href": "/alert/32199711-ae89-4c53-9b32-b859eaf74af4",
                     "id": "32199711-ae89-4c53-9b32-b859eaf74af4", "severity": "critical", "status": "open", "text": "",
                     "type": "value", "updateTime": "2020-08-13T08:00:13.735Z", "user": "apimon_bot",
                     "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"}],
                "href": "/alert/f389b541-9b91-42fa-8251-7dfdf0066c05", "id": "f389b541-9b91-42fa-8251-7dfdf0066c05",
                "lastReceiveId": "32199711-ae89-4c53-9b32-b859eaf74af4", "lastReceiveTime": "2020-08-13T08:00:13.760Z",
                "origin": "uwsgi/a606abc29abd", "previousSeverity": "indeterminate",
                "rawData": "Request to https://ces.eu-de.otc.t-systems.com/V1.0/9c816a66408740db8a4cbd0bed245303/metrics timed out",
                "receiveTime": "2020-08-09T03:23:10.969Z", "repeat": True, "resource": "ces",
                "service": ["apimon", "endpoint_monitor"], "severity": "critical", "status": "open", "tags": [],
                "text": "",
                "timeout": 86400, "trendIndication": "moreSevere", "type": "exceptionAlert",
                "updateTime": "2020-08-09T03:23:10.969Z",
                "value": "curl -g -i -X GET https://ces.eu-de.otc.t-systems.com/V1.0/metrics -H \"X-Auth-Token: ${TOKEN}\" -H \"content-type: application/json\" fails"},
            "status": "ok", "total": 1}
        last_run = self.read_last_run_time()
        while auto_refresh:
            if last_run is not None:
                current_time = last_run
                last_run = None
            else:
                current_time = get_current_time(interval)
            # alerts = self.alerta.get_alerts(query=[('from-date', current_time)])
            alerts = self.alerta.get_alerts(query=body)
            self.write_last_run_time(current_time)
            time.sleep(interval)

    def start(self):
        """Start alerta"""

        self.start_fetching()


def delta_minutes(last_receive_time) -> int:
    if last_receive_time is None:
        return 0
    return (datetime.utcnow().timestamp() - last_receive_time.timestamp()) / 60


def get_current_time(interval):
    return (datetime.utcnow() - timedelta(seconds=interval)).isoformat().split('.')[0] + '.000Z'
