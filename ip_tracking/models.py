from django.db import models


class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.TextField()

    def __str__(self):
        return f"Request from {self.ip_address} at {self.timestamp} for {self.path}"