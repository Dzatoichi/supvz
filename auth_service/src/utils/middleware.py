from loguru import logger
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()
        client_ip = request.client.host if request.client else "-"
        client_port = request.client.port if request.client else "-"
        method = request.method
        path = request.url.path
        http_version = request.scope.get("http_version", "1.1")
        response = await call_next(request)
        status_code = response.status_code
        log_type = "access"
        process_time = (time.time() - start_time) * 1000

        logger.bind(
            client_ip=client_ip,
            client_port=client_port,
            method=method,
            path=path,
            http_version=http_version,
            status_code=status_code,
            process_time=f"{process_time:.2f}ms",
            log_type=log_type,
        ).info("HTTP Request")

        return response
