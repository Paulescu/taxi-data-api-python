import time
from datetime import datetime

from elasticsearch import Elasticsearch
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import elasticsearch_config

# Initialize Elasticsearch client
es = Elasticsearch([elasticsearch_config.host])

class TimingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/trips":
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log to Elasticsearch
            es.index(
                index=elasticsearch_config.index,
                body={
                    "endpoint": "/trips",
                    "method": request.method,
                    "process_time": process_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
            return response
        return await call_next(request)
