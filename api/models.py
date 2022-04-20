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


class WhiteIP(models.Model):
    ip = models.CharField(primary_key=True, max_length=30, unique=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
