import logging
import os

import zulip
from jinja2 import Template, UndefinedError

LOGGER = logging.getLogger('zulip')

ZULIP_API_KEY = os.environ.get('ZULIP_API_KEY')
ZULIP_EMAIL = os.environ.get('ZULIP_EMAIL')
ZULIP_SITE = os.environ.get('ZULIP_SITE')
ZULIP_TYPE = os.environ.get('ZULIP_TYPE', 'stream')
ZULIP_TO = os.environ.get('ZULIP_TO')
ZULIP_SUBJECT = os.environ.get('ZULIP_SUBJECT', 'Alert')
ZULIP_ALLOW_UNSECURE = os.environ.get('ZULIP_ALLOW_UNSECURE')


class ZulipClient():

    def __init__(self, template_map, topic_map):
        zulip_args = {
            'site': ZULIP_SITE,
            'email': ZULIP_EMAIL,
            'api_key': ZULIP_API_KEY
        }
        if ZULIP_ALLOW_UNSECURE is not None:
            zulip_args['insecure'] = ZULIP_ALLOW_UNSECURE
        self.bot = zulip.Client(**zulip_args)

        self.ZULIP_TEMPLATES = template_map
        self.ZULIP_SERVICE_TOPIC_MAP = topic_map
        """
            {
                'service1': {
                    'to': 'stream_name',
                    'subject': 'topic_name'
                }
            }
        """

        # self.template = Template(DEFAULT_TMPL)

    def post_receive(self, alert):
        self.template = Template(self.ZULIP_TEMPLATES['DEFAULT_TMPL'])

        try:
            text = self.template.render(alert.__dict__)
        except UndefinedError:
            text = "Can't render zulip template message."

        try:
            message_to = None
            message_subject = None
            if (self.ZULIP_SERVICE_TOPIC_MAP
                    and isinstance(self.ZULIP_SERVICE_TOPIC_MAP, dict)):
                # ZULIP_SERVICE_TOPIC_MAP is a dict in the form
                # {'service1':
                #    {'to': 'stream_name', 'subject': 'topic_name'}
                # }
                for srv in alert.service:
                    if srv in self.ZULIP_SERVICE_TOPIC_MAP:
                        val = self.ZULIP_SERVICE_TOPIC_MAP[srv]
                        if 'subject' in val:
                            message_subject = val['subject']
                        if 'to' in val:
                            message_to = val['to']
                        break

            if not message_to:
                message_to = ZULIP_TO
            if not message_subject:
                message_subject = '_'.join(alert.service)

            request = {
                'type': ZULIP_TYPE.strip(),
                'to': message_to.strip(),
                'subject': message_subject.strip(),
                'content': text
            }
            LOGGER.debug('Zulip: message=%s', text)

            # response = self.bot.send_message(request)

        #     if response['result'] != 'success':
        #         LOGGER.warn('Error sending alert message to Zulip %s' %
        #                  response['msg'])
        except Exception as e:
            raise RuntimeError("Zulip: ERROR - %s", e)

        # LOGGER.debug('Zulip: %s', response)

        return

    def status_change(self, alert, status, text):
        return
