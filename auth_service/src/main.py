from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .routers import api_router
from .utils.exceptions import setup_exception_handlers
from .utils.middleware import LoggingMiddleware
from .utils.rate_limiter import limiter

# xyecoc
app = FastAPI()
setup_exception_handlers(app)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(LoggingMiddleware)
app.include_router(api_router)
