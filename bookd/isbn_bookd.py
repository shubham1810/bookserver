from bs4 import BeautifulSoup as BS
import urllib2, requests, json


def get_data(isbn):
    try:
        page = urllib2.urlopen('http://www.indiabookstore.net/isbn/' + str(isbn))
        soup = BS(page)
        book_name = soup.find('h1', {'class': 'bookMainTitle'})
        rating = soup.find('div', {'class': ' col-sm-4 col-xs-12 userAggregatedRatingBox ratingPositive'})
        image = soup.find('img', {'class': 'bookMainImage'})
        summary = soup.findAll('em')[0].string

        print "Book : " + str(book_name.string.split("\n")[1].split("    ")[5])
        print "ratings : " + str(rating.string.split("\n")[1].split(" ")[22])
        print "Image : " + str(image['src'])
        print summary

    except urllib2.HTTPError:
        pass


def google_books(isbn):
    page = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(isbn))
    data = json.loads(page.text)

    book_data = data['items'][0]['volumeInfo']
    name = book_data['title']
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