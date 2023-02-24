import socket  # only if you haven't already imported this
from .base import *  # noqa

DEBUG = True

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
