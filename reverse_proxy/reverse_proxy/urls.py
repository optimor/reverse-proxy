"""reverse_proxy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import jet

from proxies import views as proxy_views

from django_otp.admin import OTPAdminSite

admin.site.__class__ = OTPAdminSite


# Text to put at the end of each page's <title>.
admin.site.site_header = "Monitoring proxy"
# Text to put in each page's <h1> (and above login form).
admin.site.site_title = "Monitoring proxy"
# Text to put at the top of the admin index page.
admin.site.index_title = "Monitoring proxy"
# There is no other site than the admin iterface, so we disable links realated
# to custom site functionality
admin.site.site_url = None
# Disable bulk delete functionality
admin.site.disable_action("delete_selected")

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(
        r"^proxy-dashboard/select-site$",
        proxy_views.SelectSiteView.as_view(),
        name="select_site",
    ),
    url(
        r"^proxy-dashboard/quick-select-site/(?P<site_name>[\w-]+)$",
        proxy_views.QuickSelectSiteView.as_view(),
        name="quick_select_site",
    ),
    url(r"^proxy-jet/", include("jet.urls", "jet")),
    url(r"^proxy-dashboard/", admin.site.urls),
    url(r"^(?P<path>.*)$", proxy_views.CustomProxyView.as_view()),
]
