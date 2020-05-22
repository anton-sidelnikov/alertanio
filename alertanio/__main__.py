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


if __name__ == '__main__':
    _main()
