# alertanio

Monitors alerta service and report alerts to Zulip

Next environment variables should be set:
```bash
export ZULIP_EMAIL='';
export ZULIP_API_KEY='';
export ZULIP_TYPE='';
export ZULIP_TO='';
export ZULIP_SUBJECT='';
export ZULIP_SITE=''
```
Next variable can be set using environment variables:
```
export DB_HOST='';
export DB_PORT='';
export DB_USER='';
export DB_PASSWORD='';
export ALERTA_API_KEY='';
```
Or by passing arguments to module:
`python3 -m alertanio --postgre_host=hostname --postgre_port=port --postgre_user=username --postgre_password=password --repeat_interval=5 --config_name=prod --alerta_api_key=apikey`

`--repeat_interval=5 --config_name=prod - can de set only in module parameters`

db_init.yaml - store database structure for client:
`configuration` table store configuration elements for alerta client:
alerta_debug - bool
alerta_endpoint - str
alerta_timeout - int

`templates` table for store templates
template_name - str
template_data - str

`topics` table for store topic and it's connection to template
topic_name - str
zulip_to - Zulip stream name
zulip_subject - Zulip subject
templ_id = templates.template_id

`blackouts`
blackout_id
environment - environment name
resource
service - list of services to blackout, divided by comma
event_name 
group_name
tags
startTime - when blackout starts (timestamp)
duration - in seconds
reason - reason of blackout
