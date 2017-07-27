from django.db import models


class ProxySite(models.Model):
    name = models.SlugField(
        max_length=200, unique=True,
        help_text='Human friendly name to identify proxy settings.')
    subdomain_name = models.SlugField(
        max_length=200, unique=True, blank=True, null=True,
        help_text='Subdomain that this proxy depends on.')
    subdomain_full_url = models.URLField(
        blank=True, null=True,
        help_text='Full URL this proxy should redirect to.')
    thumbnail = models.ImageField(
        upload_to='%Y%m%d%H%M', blank=True, null=True,
        help_text='Proxied site thumbnail to display in dashboard. Thumbnail '
                  'should have square dimensions.')
    upstream = models.CharField(
        max_length=200,
        help_text='The URL of the proxied server. Requests will be made to '
                  'this URL with path appended to it.')
    add_remote_user = models.BooleanField(
        default=False, help_text='Whether to add the REMOTE_USER to the '
                                 'request in case of an authenticated user.')
    default_content_type = models.CharField(
        max_length=200, default='application/octet-stream',
        help_text='The Content-Type that will be added to the response in '
                  'case the upstream server doesn\'t send it and if '
                  'mimetypes.guess_type is not able to guess.')
    retries = models.PositiveIntegerField(
        default=0, help_text='The max number of attempts for a request.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'proxy sites'


class ProxyRewrite(models.Model):
    proxy_site = models.ForeignKey(ProxySite)
    from_regex = models.CharField(max_length=255)
    to_regex = models.CharField(max_length=255)

    def __str__(self):
        return '{}, {}'.format(self.from_regex, self.to_regex)


class ProxyHeader(models.Model):
    proxy_site = models.ForeignKey(ProxySite)
    header_name = models.CharField(max_length=255)
    header_value = models.CharField(max_length=255)

    def __str__(self):
        return '{}, {}'.format(self.header_name, self.header_value)
