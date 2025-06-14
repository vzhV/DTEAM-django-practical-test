from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from xhtml2pdf import pisa

from .models import CV
from .serializers import CVSerializer
from .tasks import send_cv_pdf_email


def cv_list(request):
    cv_queryset = CV.objects.all().order_by('id')
    limit_options = [5, 10, 20, 50]
    try:
        limit = int(request.GET.get('limit', 10))
        if limit <= 0 or limit > 100:
            limit = 10
    except (ValueError, TypeError):
        limit = 10

    paginator = Paginator(cv_queryset, limit)
    page_number = request.GET.get('page', 1)

    try:
        cvs = paginator.page(page_number)
    except PageNotAnInteger:
        cvs = paginator.page(1)
    except EmptyPage:
        cvs = paginator.page(paginator.num_pages)

    return render(request, "main/cv_list.html", {
        "cvs": cvs,
        "limit": limit,
        "limit_options": limit_options
    })


def cv_detail(request, pk):
    cv = get_object_or_404(CV, pk=pk)
    return render(request, "main/cv_detail.html", {"cv": cv})


def cv_pdf(request, pk):
    cv = get_object_or_404(CV, pk=pk)
    template = get_template("main/cv_pdf.html")
    html = template.render({"cv": cv})

    response = HttpResponse(content_type="application/pdf")
    filename = f"{cv.firstname}-{cv.lastname}-cv.pdf".replace(" ", "_")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors with PDF generation <br>" + html)
    return response


def settings_view(request):
    return render(request, "settings.html")


@require_POST
def send_cv_email(request, pk):
    email = request.POST.get("email")
    cv = get_object_or_404(CV, pk=pk)
    if not email:
        messages.error(request, "Mail address is required.")
        return redirect("cv_detail", pk=pk)
    send_cv_pdf_email.delay(pk, email)
    messages.success(request, f"CV has been sent to {email}")
    return redirect("cv_detail", pk=pk)


class CVViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing CVs.
    Provides standard CRUD actions.
    """
    queryset = CV.objects.all().order_by('id')
    serializer_class = CVSerializer
