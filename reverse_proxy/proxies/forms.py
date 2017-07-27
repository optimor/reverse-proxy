from django import forms

from .models import ProxySite


class SelectSiteForm(forms.Form):
    proxy_site = forms.ModelChoiceField(queryset=ProxySite.objects.all())

    class Meta:
        fields = ['proxy_site']


class ProxySiteForm(forms.ModelForm):
    class Meta:
        model = ProxySite
        exclude = []

    def clean(self):
        cleaned_data = super(ProxySiteForm, self).clean()
        subdomain_name = cleaned_data.get('subdomain_name')
        subdomain_full_url = cleaned_data.get('subdomain_full_url')

        if (any([subdomain_name, subdomain_full_url]) and
                not all([subdomain_name, subdomain_full_url])):
            self.add_error('subdomain_name', 'Both fields must be filled in.')
            self.add_error(
                'subdomain_full_url', 'Both fields must be filled in.')
