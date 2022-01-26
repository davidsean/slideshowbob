
# Don't configure SSL with gunicorn, use HAProxy instead
bind = '0.0.0.0:80'

wsgi_app = '/app/main.py'
workers = 8


# pidfile = 'pidfile'
# errorlog = 'errorlog'
loglevel = 'debug'
# accesslog = 'accesslog'