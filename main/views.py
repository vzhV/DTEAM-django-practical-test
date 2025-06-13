from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import CV


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
