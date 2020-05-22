# alertanio

Monitors alerta service and report alerts to Zulip

Next environment variables should be set:
```bash
export DB_HOST='';
export DB_PORT='';
export DB_USER='';
export DB_PASSWORD='';
export ALERTA_API_KEY='';
export ZULIP_EMAIL='';
export ZULIP_API_KEY='';
export ZULIP_TYPE='';
export ZULIP_TO='';
export ZULIP_SUBJECT='';
export ZULIP_SITE=''
```

db_init.yaml - store database structure for client:
`configuration` table store configuration elements for alerta client:
alerta_debug - bool
alerta_endpoint - str
alerta_timeout - int

`templates` table for store templates
template_name - str
template_data - str

`topics` table for store topic and it's connection to template
topic_name - str,
zulip_to - Zulip stream name,
zulip_subject - Zulip subject,
templ_id = templates.template_id