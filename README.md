# Alertanio

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
```bash
export DB_HOST='';
export DB_PORT='';
export DB_USER='';
export DB_PASSWORD='';
export ALERTA_API_KEY='';
```
Or by passing arguments to module:
`python3 -m alertanio --postgre_host=hostname --postgre_port=port --postgre_user=username --postgre_password=password --repeat_interval=5 --config_name=prod --alerta_api_key=apikey`

--repeat_interval=5 --config_name=prod - can de set only in module parameters

### **db_init.yaml** - store database structure for client:

`configuration` table store configuration elements for alerta client:
1. alerta_debug - bool
2. alerta_endpoint - str
3. alerta_timeout - int

`templates` table for store templates
1. template_name - str
2. template_data - str

`topics` table for store topic and it's connection to template
1. topic_name - str,
2. zulip_to - Zulip stream name,
3. zulip_subject - Zulip subject,
4. templ_id = templates.template_id

`blackouts`
1. blackout_id
2. environment - environment name
3. resource
4. service - list of services to blackout, divided by comma
5. event_name 
6. group_name
7. tags
8. startTime - when blackout starts (timestamp)
9. duration - in seconds
10. reason - reason of blackout
