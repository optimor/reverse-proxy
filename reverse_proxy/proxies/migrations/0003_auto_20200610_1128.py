# Generated by Django 2.2.13 on 2020-06-10 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("proxies", "0002_auto_20170727_1527"),
    ]

    operations = [
        migrations.RemoveField(model_name="proxysite", name="request_headers",),
        migrations.RemoveField(model_name="proxysite", name="rewrite",),
    ]
