# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-27 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("proxies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="proxysite",
            name="subdomain_full_url",
            field=models.URLField(
                blank=True,
                help_text="Full URL this proxy should redirect to.",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="proxysite",
            name="subdomain_name",
            field=models.SlugField(
                blank=True,
                help_text="Subdomain that this proxy depends on.",
                max_length=200,
                null=True,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="proxysite",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                help_text="Proxied site thumbnail to display in dashboard. Thumbnail "
                "should have square dimensions.",
                null=True,
                upload_to="%Y%m%d%H%M",
            ),
        ),
    ]
