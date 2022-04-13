from django.db import models


class Log(models.Model):
    operations = (
        ('ssh', 'Open-SSH'),
        ('check', 'Check-me'),
        ('logs', 'client-logs'),
        ('ddos', 'DDOS'),
        ('domain', 'Domain'),
        ('available', 'Check-available')
    )
    ip = models.CharField(max_length=30)
    operation = models.CharField(max_length=9, choices=operations)
    system = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)

