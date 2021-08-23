# Generated by Django 3.0.2 on 2020-02-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0004_delete_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('ip', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='ip address')),
                ('user_agent', models.CharField(max_length=100, verbose_name='user agen ')),
            ],
            options={
                'db_table': 'Log',
            },
        ),
    ]