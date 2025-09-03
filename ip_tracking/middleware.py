import logging
from datetime import datetime, timezone
from ipware import get_client_ip

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response
    
  def __call__(self, request):
    ip_address, is_routable = get_client_ip(request)
    
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    path = request.path
    
    if ip_address is None:
      logger.warning("Unable to get the client's IP address.")
      ip_address = '0.0.0.0'
      is_routable = False
      log_message = f"[{timestamp}] - Incoming request from IP: {ip_address}, Path: {path}"
      logger.info(log_message)
    else:
      if is_routable:
        log_message = f"[{timestamp}] - Incoming request from ROUTABLE IP: {ip_address}, Path: {path}"
      else:
        log_message = f"[{timestamp}] - Incoming request from NON-ROUTABLE IP: {ip_address}, Path: {path}"
      logger.info(log_message)

    response = self.get_response(request)
    return response