from django.shortcuts import render, HttpResponse
import json
from bookd.isbn_bookd import *
from bookd.models import Book


def apiCall(request):
    val = request.GET.get('isbn')
    try:
        response_value = google_books(val)
    except:
        try:
            response_value = get_data(val)
        except:
            response_value = {"title": 'Error'}

    try:
        saveInParse(response_value)
    except:
        pass

    return HttpResponse(json.dumps(response_value), content_type="application/json")


def saveInParse(response):
    book_data = Book(isbn=response['isbn'], title=response['title'], publisher=response['publisher'], authors=response['authors'], rating=response['rating'], category=response['category'], image=response['image'], summary=response['summary'])
    book_data.save()