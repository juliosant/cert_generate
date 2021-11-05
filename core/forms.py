from django import forms
from .models import CertificateRevocation

class CertForm(forms.Form):
        country_name = forms.CharField(label='País')
        state = forms.CharField(label='Estado')
        city = forms.CharField(label='Cidade')
        organization_name = forms.CharField(label='Nome da Organização')
        common_name = forms.CharField(label='Nome Fantasia')
        email = forms.EmailField(label='Email')


class CertPrintForm(forms.Form):
        key = forms.CharField(widget=forms.Textarea(attrs={}))
        cert = forms.CharField(widget=forms.Textarea(attrs={}))

class CertificateRevocationForm(forms.ModelForm):
        class Meta:
                model = CertificateRevocation
                fields = '__all__'
                widgets = {
                        'serial_number': forms.TextInput(attrs={'placeholder': 'Digite o "serial number" do certificado'})
                }

