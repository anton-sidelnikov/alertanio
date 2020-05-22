# Alertanio

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
