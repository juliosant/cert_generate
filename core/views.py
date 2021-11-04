# Create your views here.
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CertForm, CertificateRevocationForm
from .models import CertificateRevocation


def homepage(request):
    return render(request, 'home.html')


# Gerar chave
def gen_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    # Write our key to disk for safe keeping
    with open("key.pem", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
        ))
    
    return key


# Gerar certificado
def gen_certificate(key, post):
    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, post['country_name']),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, post['state']),
        x509.NameAttribute(NameOID.LOCALITY_NAME, post['city']),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, post['organization_name']),
        x509.NameAttribute(NameOID.COMMON_NAME, post['common_name']),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, post['email']),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Our certificate will be valid for 10 days
        datetime.datetime.utcnow() + datetime.timedelta(days=10)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    # Sign our certificate with our private key
    ).sign(key, hashes.SHA256())
    # Write our certificate out to disk.
    with open("certificate.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


# Mostrar certificado e chave gerada
def certificate(request):
    privateKeySTR = open('key.pem').read()
    certificateSTR = open('certificate.pem').read()
    #certSTR = x509.load_pem_x509_certificate(str.encode(certificateSTR), default_backend())
    content = {
            'cert': certificateSTR,
            'privateKey': privateKeySTR,
            #'certSTR': certSTR
    }
    print(privateKeySTR)
    return render(request, 'certificate.html', content)


# Gerar formulário de dados para certificado
def create_certificate(request):
    if request.POST:
        keyPEM = gen_key()
        certPEM = gen_certificate(keyPEM, request.POST.copy())

        #print(certificateSTR)
        #print(certSTR.serial_number)
        #print(certSTR.issuer.rfc4514_string())

        return redirect('certificate')

    certificate_form = CertForm()
    content = {
        'certificate_form': certificate_form
    }
    return render(request, 'create_certificate.html', content)


# Adicionar certificados para crl
def add_cert_revocation(request):
    cert_revocation_form = CertificateRevocationForm()
    content = {
        'cert_revocation_form': cert_revocation_form,
        'exists': False
    }

    if request.POST:
        certificates_number = CertificateRevocation.objects.filter(serial_number=request.POST['serial_number']).count()
        if certificates_number > 0:
            messages.info(request, "Certificado já tinha sido revogado revogado")
            content['exists'] = True
            return render(request, 'add_cert_revocation.html', content)
        cert_revocation_form = CertificateRevocationForm(request.POST)
        if cert_revocation_form.is_valid():
            cert_revocation_form.save()
            return redirect('homepage')
    
    return render(request, 'add_cert_revocation.html', content)


# listar Certificdos Revogados
def cert_revocation_list(request):
    crl = CertificateRevocation.objects.all()
    content = {
        'crl' :crl
    }
    return render(request, 'cetificate_revocation_list.html', content)
#https://understandingwebpki.com/