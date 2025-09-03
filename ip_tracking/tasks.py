import logging
from datetime import datetime, timedelta
from celery import shared_task
from django.db.models import Count
from ip_tracking.models import RequestLog, SuspiciousIP

logger = logging.getLogger(__name__)

@shared_task
def flag_suspicious_ips():
  """
    An hourly Celery task to check for suspicious IP addresses
    based on request volume and access to sensitive paths.
  """
  
  logger.info("Starting hourly suspicious IP detection task...")
  
  one_hour_ago = datetime.now() - timedelta(hours=1)
  
  high_volume_ips = RequestLog.objects.filter(
    timestamp__gte=one_hour_ago
  ).values('ip_address').annotate(
    request_count=Count('ip_address')
  ).filter(
    request_count__gt=100
  ).order_by('-request_count')


  for entry in high_volume_ips:
    ip = entry['ip_address']
    reason = f"High request volume: {entry['request_count']} requests in the last hour."
    SuspiciousIP.objects.get_or_create(ip_address=ip, defaults={'reason': reason})
    logger.warning(f"Flagged suspicious IP '{ip}' for high request volume.")

  sensitive_paths = ['/admin/', '/login/', '/api/']
  
  suspicious_ips = RequestLog.objects.filter(
    timestamp__gte=one_hour_ago,
    path__in=sensitive_paths
  ).values('ip_address').distinct()

  for entry in suspicious_ips:
    ip = entry['ip_address']
    reason = f"Accessed sensitive path: {entry['path']}."
    SuspiciousIP.objects.get_or_create(ip_address=ip, defaults={'reason': reason})
    logger.warning(f"Flagged suspicious IP '{ip}' for accessing sensitive paths.")
    
    
logger.info("Completed suspicious IP detection task.")