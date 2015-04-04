from django.shortcuts import render, HttpResponse
import json
from bookd.isbn_bookd import *
from bookd.models import Book


def apiCall(request):
    val = request.GET.get('isbn')


    bookVals = Book.Query.filter(isbn=str(val))

    print len(bookVals), "SHUBHAM"
    if len(bookVals) is not 0:
        response = {}
        for existing in bookVals:
            response['publisher'] = existing.publisher
            response['isbn'] = existing.isbn
            response['title'] = existing.title
            response['authors'] = existing.authors
            response['summary'] = existing.summary
            response['image'] = existing.image
            response['rating'] = existing.rating
            response['category'] = existing.category

        print response

        return HttpResponse(json.dumps(response), content_type="application/json")

    else:
        print "YAY"
        try:
            response_value = google_books(val)
        except:
            try:
                response_value = get_data(val)
            except:
                response_value = {"title": 'Error'}

        saveInParse(response_value)

        return HttpResponse(json.dumps(response_value), content_type="application/json")


def saveInParse(response):
    book_data = Book(isbn=response['isbn'], title=response['title'], publisher=response['publisher'], authors=response['authors'], rating=float(str(response['rating'])), category=response['category'], image=response['image'], summary=response['summary'])
    book_data.save()