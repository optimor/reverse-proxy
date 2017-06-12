from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from revproxy.views import ProxyView

from .models import ProxySite
from .forms import SelectSiteForm


@method_decorator(login_required, name='dispatch')
class SelectSiteView(View):
    template_name = 'proxies/select_site.html'
    form = SelectSiteForm

    def get(self, request, *args, **kwargs):
        ctx = {
            'form': self.form()
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            request.session['current_site'] = (
                form.cleaned_data['proxy_site'].name)
            return HttpResponseRedirect('/')
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)


@method_decorator(login_required, name='dispatch')
class QuickSelectSiteView(View):
    def get(self, request, site_name, *args, **kwargs):
        proxy = get_object_or_404(ProxySite, name=site_name)
        request.session['current_site'] = proxy.name
        return HttpResponseRedirect('/')


@method_decorator(login_required, name='dispatch')
class CustomProxyView(ProxyView):
    def get_request_headers(self):
        headers = super(CustomProxyView, self).get_request_headers()
        for proxy_header in self.proxy.proxyheader_set.all():
            headers[proxy_header.header_name] = proxy_header.header_value
        return headers

    def dispatch(self, request, path, *args, **kwargs):
        if 'current_site' not in request.session:
            return HttpResponseRedirect(reverse('select_site'))

        proxy_site_qs = ProxySite.objects.all().prefetch_related(
            'proxyrewrite_set', 'proxyheader_set')
        self.proxy = get_object_or_404(
            proxy_site_qs, name=request.session['current_site'])

        self.upstream = self.proxy.upstream
        self.add_remote_user = self.proxy.add_remote_user
        self.default_content_type = self.proxy.default_content_type
        self.retries = self.proxy.retries

        self._rewrite = []
        # Take all elements inside tuple, and insert into _rewrite
        for proxy_rewrite in self.proxy.proxyrewrite_set.all():
            from_re = re.compile(proxy_rewrite.from_regex)
            self._rewrite.append((from_re, proxy_rewrite.to_regex))

        response = super(CustomProxyView, self).dispatch(
            request, path, *args, **kwargs)

        return response
