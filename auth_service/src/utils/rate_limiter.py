from slowapi import Limiter
from starlette.requests import Request


def get_remote_address(request: Request) -> str:
    """
    Функция получения IP-адреса клиента, сделавшего запрос к приложению.
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    x_real_ip = request.headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip.strip()

    return request.client.host


limiter = Limiter(key_func=get_remote_address, default_limits=["100/minutes; 1000/hour"])
