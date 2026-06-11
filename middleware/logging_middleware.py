import time

from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware

from core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    
	async def dispatch(self, request: Request, call_next):
     
		start_time = time.perf_counter()
  
		method = request.method
  
		path = request.url.path

  
		client_ip = request.client.host
  
		logger.info(
			f"Incoming request | method={method} | path={path} | client_ip={client_ip}"
		)
		try:
			response = await call_next(request)
   
			process_time = round(time.perf_counter() - start_time, 4)
   
			logger.info(
				f"Request completed | method={method} | path={path} | status_code={response.status_code} | duration={process_time}s"
			)
   
			return response

		except Exception as e:
      
			process_time = round(time.perf_counter() - start_time, 4)
   
			logger.error(
				f"Request failed |method={method} |path={path} | duration={process_time}s |error={str(e)}"
			)
   
			raise
