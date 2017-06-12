from django import forms

from .models import ProxySite


class SelectSiteForm(forms.Form):
    proxy_site = forms.ModelChoiceField(queryset=ProxySite.objects.all())

    class Meta:
        fields = ['proxy_site']
