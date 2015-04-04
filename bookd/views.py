from django.shortcuts import render, HttpResponse
import json
from bookd.isbn_bookd import *


def apiCall(request):
    val = request.GET.get('isbn')
    try:
        response_value = google_books(val)
    except:
        response_value = {}

    return HttpResponse(json.dumps(response_value), content_type="application/json")