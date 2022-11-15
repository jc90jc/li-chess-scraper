#from xml.dom import minidom
import requests
#import json
from bs4 import BeautifulSoup
import pandas as pd

user_ = XYZ

getheaders={

    "upgrade-insecure-requests": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "cookie": "lila2=57ec0eb32b909e5820f88fcc64aad61d679f95c2-sid=JrI63o7VDgAKSbRSYEgy2r&sessionId=li2OqtjxGrRcQbPfmSduZm; __stripe_mid=a3656481-8a90-434a-9109-00ff5e68dae92e63d7"
    }

for i in range(1,40):
    tagx=''
    if i>1:
        tagx='page=' + str(i) + '&'
    url = 'https://lichess.org/@/' + user_ + '/search?' + tagx + 'players.a=' + user_ + '&sort.order=desc'
    url = requests.get(url, headers = getheaders)
    url1=url.text
    ##print(url)
   # soup = BeautifulSoup(url1)                #make BeautifulSoup
    #prettyHTML = soup.prettify()   #prettify the html
##    print(prettyHTML)
    soup = BeautifulSoup(url.content, 'html.parser')
    s = soup.find('div', {'class': 'search__rows infinite-scroll'})
    ##print (s)
##    print(i)
    if i==1:
        h, [*d]= ['Apertura', 'Tipo', 'B/N','W/L/S','Resultado', 'Link', 'Movimientos'],[[
            b.find('div', {'class': 'opening'}).strong.text,
            b.find('div', {'class': 'header__text'}).strong.text.split(" ", 1)[0],
            b.find('a', {'href': '/@/' + user_}).parent['class'][1],
            b.find('div', {'class': 'result'}).span.attrs,
            b.find('div', {'class': 'result'}).span.text.split(" •", 1)[0],
            '<a href="' + 'http://lichess.org' + b.find('a', {'class': 'game-row__overlay'})['href'][:9] + '">///</a>',
            b.find('div', {'class': 'pgn'}).text
            ]  for b in s.find_all('article')]
##        print(d)
    else:
        [*dx]=[[b.find('div', {'class': 'opening'}).strong.text,
            b.find('div', {'class': 'header__text'}).strong.text.split(" ", 1)[0],
            b.find('a', {'href': '/@/' + user_}).parent['class'][1],
            b.find('div', {'class': 'result'}).span.attrs,
            b.find('div', {'class': 'result'}).span.text.split(" •", 1)[0],
            '<a href="' + 'http://lichess.org' + b.find('a', {'class': 'game-row__overlay'})['href'][:9] + '">///</a>',
            b.find('div', {'class': 'pgn'}).text
            ]  for b in s.find_all('article')]
        d.extend(dx)
##        print (dx)
##        print(d)
    
result = [dict(zip(h, i)) for i in d]
    
result = pd.DataFrame(result).to_html(
    render_links=True,
    escape=False,
)
pre1='<html lang="en">' + \
    '<head>' + \
    '  <title></title>' + \
    '  <meta charset="utf-8">' + \
    '  <meta name="viewport" content="width=1024">' + \
    '  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">' + \
    '  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>' + \
    '  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>' + \
    '</head>' + \
    '<body>' + \
    '<div>' + \
    '<input class="form-control" id="myInput" type="text" placeholder="Search..">' + \
    '  <br>'

post1 = '</div>' + \
    '<script>' + \
    '$(document).ready(function(){' + \
    '  $("#myInput").on("keyup", function() {' + \
    '    var value = $(this).val().toLowerCase();' + \
    '    $("#myTable tr").filter(function() {' + \
    '      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)' + \
    '    });' + \
    '  });' + \
    '});' + \
    '</script>' + \
    '</body>' + \
    '</html>'

result=result.replace("{'class': ['loss']}","loss").replace("{'class': ['win']}","win").replace("{}","stalemate")
result=result.replace('tbody>','tbody id="myTable">')

result1=pre1 + result + post1

##print( result)
with open("/var/www/html/0.html", "w") as file:
    file.write(result1)


