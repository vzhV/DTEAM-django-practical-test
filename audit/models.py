from django.db import models


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=8)
    path = models.CharField(max_length=512)
    query_string = models.TextField(blank=True)
    remote_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return (f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.method} {self.path}"
                f" ({self.remote_ip or 'Anonymous IP'})")

    class Meta:
        ordering = ["-timestamp"]
