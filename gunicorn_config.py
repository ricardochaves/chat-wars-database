############
###### http://docs.gunicorn.org/en/stable/settings.html#worker-processes

workers = 2
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2

############
###### http://docs.gunicorn.org/en/stable/settings.html#logging

errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '{"message": "%(r)s", "request_id": "%({HTTP_X_REQUEST_ID}o)s", "http_status": %(s)s, "ip_address": "%(h)s", "response_length": "%(b)s", "referer": "%(f)s", "user_agent": "%(a)s", "request_time": %(L)s, "date": "%(t)s"}'
