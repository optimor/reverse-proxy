from django.contrib import admin
from jet.admin import CompactInline

from .models import ProxySite, ProxyRewrite, ProxyHeader
from .forms import ProxySiteForm


class ProxyRewriteInline(CompactInline):
    model = ProxyRewrite
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('from_regex', 'to_regex'),
            'description':
                'A list of tuples in the style (from, to) where from must by '
                'a valid regex expression and to a valid URL. If '
                'request.get_full_path matches the from expression the '
                'request will be redirected to to with an status code 302. '
                'Matches groups can be used to pass parts from the from '
                'URL to the to URL using numbered groups.'
        }),
    )


class ProxyHeaderInline(CompactInline):
    model = ProxyHeader
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('header_name', 'header_value'),
            'description':
                'A list of tuples in the style (key, value) where key must '
                'by a valid HEADER and key a valid header value.'
        }),
    )


@admin.register(ProxySite)
class ProxySiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'upstream', 'subdomain_name', 'subdomain_full_url',
                    'add_remote_user', 'default_content_type', 'retries')
    fieldsets = (
        (None, {
            'fields': ('name', 'upstream', 'thumbnail'),
        }),
        ('Subdomain', {
            'fields': ('subdomain_name', 'subdomain_full_url'),
            'description':
                'Specify those to setup proxy that redirects based on the '
                'subdomain of the current URL'
        }),
        ('Extra', {
            'fields': ('add_remote_user', 'default_content_type', 'retries')
        }),
    )
    form = ProxySiteForm
    inlines = (ProxyRewriteInline, ProxyHeaderInline)
