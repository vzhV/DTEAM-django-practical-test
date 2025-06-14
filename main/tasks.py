import tempfile

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import CV
from xhtml2pdf import pisa


@shared_task
def send_cv_pdf_email(cv_id, to_email):
    cv = CV.objects.get(pk=cv_id)
    html = render_to_string("main/cv_pdf.html", {"cv": cv})
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=True) as temp_file:
        pisa_status = pisa.CreatePDF(html, dest=temp_file)
        if pisa_status.err:
            return False

        temp_file.flush()
        temp_file.seek(0)

        filename = f"{cv.firstname}-{cv.lastname}-cv.pdf".replace(" ", "_")
        email = EmailMessage(
            subject=f"{cv.firstname} {cv.lastname} CV",
            body="CV is attached as PDF file",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach(filename, temp_file.read(), "application/pdf")
        email.send()
    return True
