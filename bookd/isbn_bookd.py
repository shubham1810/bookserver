from bs4 import BeautifulSoup as BS
import urllib2, requests, json


def get_data(isbn):
    try:
        page = urllib2.urlopen('http://www.indiabookstore.net/isbn/' + str(isbn))
        soup = BS(page)
        book_name = soup.find('h1', {'class': 'bookMainTitle'})
        rating = soup.find('div', {'class': ' col-sm-4 col-xs-12 userAggregatedRatingBox ratingPositive'})
        image = soup.find('img', {'class': 'bookMainImage'})
        summary = soup.findAll('em')

        print "Book : " + str(book_name.string.split("\n")[1].split("    ")[5])
        print "ratings : " + str(rating.string.split("\n")[1].split(" ")[22])
        print "Image : " + str(image['src'])

    except urllib2.HTTPError:
        pass


def google_books(isbn):
    try:
        page = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(isbn))
    except:
        pass
    data = json.loads(page.text)

    try:
        book_data = data['items'][0]['volumeInfo']
        name = book_data['name']

        page = urllib2.urlopen('http://www.indiabookstore.net/isbn/' + str(isbn))
        soup = BS(page)

        summary = soup.findAll('em')[0].string
        print summary
    except:
        pass

if __name__ == '__main__':
    #get_data(9788131710265)
    google_books(9788131710265)