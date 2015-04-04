from bs4 import BeautifulSoup as BS
import urllib2, requests, json


def get_data(isbn):
    try:
        page = urllib2.urlopen('http://www.indiabookstore.net/isbn/' + str(isbn))
        soup = BS(page)
        book_name = soup.find('h1', {'class': 'bookMainTitle'})
        print book_name.string.strip()
        rating = soup.find('div', {'class': ' col-sm-4 col-xs-12 userAggregatedRatingBox ratingPositive'})
        image = soup.find('img', {'class': 'bookMainImage'})
        summary = soup.findAll('em')[0].string
        authors = soup.findAll('div')
        category = "Uncategorized"

        author = ""
        for i in authors:
            if i.string is not None and 'Author' in i.string:
                author = i.string[9:]
                break
            else:
                author = ""
        publisher = ""
        for i in authors:
            if i.string is not None and 'Publisher' in i.string:
                publisher = i.string[12:]
                break
            else:
                publisher = ""

        response = {}
        response['publisher'] = str(publisher)
        response['isbn'] = str(isbn)
        response['title'] = str(book_name.string.strip())
        response['authors'] = author
        response['summary'] = summary
        response['image'] = str(image['src'])
        response['rating'] = str(rating.string.strip())
        response['category'] = category

        return response

    except urllib2.HTTPError:
        return {}


def google_books(isbn):
    page = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(isbn))
    data = json.loads(page.text)

    book_data = data['items'][0]['volumeInfo']
    name = book_data['title']
    publisher = book_data['publisher']
    authors = ""
    for i in book_data['authors']:
        if len(book_data['authors']) is not 1:
            authors = authors.join(", " + str(i))
        else:
            authors = book_data['authors'][0]

    page = urllib2.urlopen('http://www.indiabookstore.net/isbn/' + str(isbn))
    soup = BS(page)

    image = book_data['imageLinks']['thumbnail']
    rating = book_data['averageRating']
    category = "Uncategorized"

    summary = soup.findAll('em')[0].string
    '''print name
    print authors
    print summary
    print image
    print rating
    print category'''

    response = {}
    response['publisher'] = publisher
    response['isbn'] = str(isbn)
    response['title'] = name
    response['authors'] = authors
    response['summary'] = summary
    response['image'] = image
    response['rating'] = rating
    response['category'] = category

    return response

if __name__ == '__main__':
    get_data(9788131710265)
    #google_books(9788131710265)