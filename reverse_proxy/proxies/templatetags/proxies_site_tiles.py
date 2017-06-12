from django import template

from proxies.models import ProxySite

register = template.Library()


@register.inclusion_tag('proxies/templatetags/site_tiles.html',
                        takes_context=True)
def site_tiles(context):
    return {
        'proxy_sites_qs': ProxySite.objects.all(),
    }
