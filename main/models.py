from django.db import models

# Create your models here.
class Log (models.Model):
    ip=models.CharField("ip address" ,max_length=30 ,primary_key=True)
    user_agent=models.CharField("user agen ",max_length=100)
    FinishTime = models.DateTimeField(db_column="finish_time", auto_now=True)

    class Meta:
        db_table="Log"
