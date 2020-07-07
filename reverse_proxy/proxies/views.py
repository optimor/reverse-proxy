from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from revproxy.views import ProxyView

from .models import ProxySite
from .forms import SelectSiteForm


@method_decorator(login_required, name="dispatch")
class SelectSiteView(View):
    template_name = "proxies/select_site.html"
    form = SelectSiteForm

    def get(self, request, *args, **kwargs):
        ctx = {"form": self.form()}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            proxy_site = form.cleaned_data["proxy_site"]
            request.session["current_site"] = proxy_site.name
            request.session["current_site_full_url"] = proxy_site.subdomain_full_url
            if proxy_site.subdomain_full_url:
                return HttpResponseRedirect(proxy_site.subdomain_full_url)
            return HttpResponseRedirect("/")
        ctx = {"form": form}
        return render(request, self.template_name, ctx)


@method_decorator(login_required, name="dispatch")
class QuickSelectSiteView(View):
    def get(self, request, site_name, *args, **kwargs):
        proxy = get_object_or_404(ProxySite, name=site_name)
        request.session["current_site"] = proxy.name
        request.session["current_site_full_url"] = proxy.subdomain_full_url
        if proxy.subdomain_full_url:
            return HttpResponseRedirect(proxy.subdomain_full_url)
        return HttpResponseRedirect("/")


@method_decorator(login_required, name="dispatch")
class CustomProxyView(ProxyView):
    def get_request_headers(self):
        headers = super(CustomProxyView, self).get_request_headers()
        for proxy_header in self.proxy.proxyheader_set.all():
            headers[proxy_header.header_name] = proxy_header.header_value
        return headers

    def get_request_subdomain(self, request):
        domain = request.META["HTTP_HOST"]
        pieces = domain.split(".")
        try:
            subdomain = pieces[0]
        except IndexError:
            # No subdomain available
            subdomain = None

        return subdomain

    def dispatch(self, request, path, *args, **kwargs):
        proxy_site_qs = ProxySite.objects.all().prefetch_related(
            "proxyrewrite_set", "proxyheader_set"
        )

        proxy_found = False
        subdomain = self.get_request_subdomain(request)
        if subdomain is not None:
            try:
                self.proxy = proxy_site_qs.get(subdomain_name=subdomain)
                proxy_found = True
            except ObjectDoesNotExist:
                # No proxy sites found for this subdomain
                pass

        if not proxy_found:
            if "current_site" not in request.session:
                return HttpResponseRedirect(reverse("select_site"))
            else:
                self.proxy = proxy_site_qs.get(name=request.session["current_site"])

        self.upstream = self.proxy.upstream
        self.add_remote_user = self.proxy.add_remote_user
        self.default_content_type = self.proxy.default_content_type
        self.retries = self.proxy.retries

        self._rewrite = []
        # Take all elements inside tuple, and insert into _rewrite
        for proxy_rewrite in self.proxy.proxyrewrite_set.all():
            from_re = re.compile(proxy_rewrite.from_regex)
            self._rewrite.append((from_re, proxy_rewrite.to_regex))

        response = super(CustomProxyView, self).dispatch(request, path, *args, **kwargs)

        return response
