
# Don't configure SSL with gunicorn, use HAProxy instead
# bind = '0.0.0.0:443'
# certfile = '/instance/certs/certificate.pem'
# ca_certs = '/instance/certs/dv-ssl-chain.pem'
# keyfile = '/instance/certs/privatekey.key'

# wsgi_app = '/instance/app/main.py'

# workers = 4
# ssl_version = 'TLS'

# pidfile = 'pidfile'
# errorlog = 'errorlog'
loglevel = 'debug'
# accesslog = 'accesslog'