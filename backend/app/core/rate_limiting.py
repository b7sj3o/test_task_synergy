from slowapi import Limiter
from slowapi.util import get_remote_address


# limiting based on the IP address
limiter = Limiter(key_func=get_remote_address)