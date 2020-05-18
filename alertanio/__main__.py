import logging

from alertanio.config.static_config import TABLES
from alertanio.database import DBHelper

LOG = logging.getLogger('alertanio')

DEFAULT_TMPL = """
{% if customer %}Customer: `{{customer}}` {% endif %}
*[{{ status.capitalize() }}] {{ environment }} {{ severity.capitalize() }}*
{{ event }} {{ resource.capitalize() }}
```
{{ text }}
```
"""


def _main():
    db = DBHelper(host="80.158.41.159", port="5432", user="postgres", password="qwerty12345!")
    db.__connect__()
    if not db.check_database_exist():
        db.query(TABLES['config'].params)
        db.query(TABLES['templates'].params)
        db.query(TABLES['topics'].params)
    db.__disconnect__()


if __name__ == '__main__':
    _main()
