from application.models import Movie, Rating
from urllib import quote
import requests
import json
import time
import codecs

#tmdb username: softwareengineering14
#tmdb pass: PEQybzeR
api_key = 'a911827b62ca2bd0cb692a422e4f7045'

def getJson(url,args):
    r = requests.get(url.format(*args)).content.decode('utf-8')
    try:
        j = json.loads(r)
        return j
    except:
        return {'total_results':0}

loadItems = raw_input("Load Items? [y,N]> ")
if('y' in loadItems.lower()):
    movs = []
    image_url = 'http://image.tmdb.org/t/p/w500'
    search_url = 'http://api.themoviedb.org/3/search/movie?api_key={}&query={}'
    data_url = 'http://api.themoviedb.org/3/movie/{}?api_key={}&append_to_response=credits'

    with codecs.open("datasets/movielens/ml-100k/u.item", encoding = "ISO-8859-1") as f:
      for line in f:
        item = line.strip().split('|')
        db_id = item[0]
        title = item[1]
        link = item[4]

        print(title)
        t = " ".join(title.strip().split()[:-1])
        j = getJson(search_url, (api_key, quote(t)))
        while t!="" and j['total_results'] == 0:
            print("lookup ",t)
            t = " ".join(t.strip().split()[:-1])
            j = getJson(search_url, (api_key, quote(t)))
            time.sleep(1)

        try:
            r = j['results'][0]
            api_id = r['id']
            image = image_url+r['poster_path']

            j = getJson(data_url, (api_id, api_key))
            actor    = ", ".join(person['name'] for person in j['credits']['cast'][:2])
            director = ", ".join(person['name'] for person in j['credits']['crew'] if person['job'] == "Director") 
            description = j['overview'] or "N/A"
        except:
            image = " "
            actor = " "
            director = " "
            description = "N\A"
        

        mov = Movie()
        mov.id = db_id
        mov.title = title
        mov.link = link
        mov.image = image
        mov.director = director 
        mov.actor = actor
        mov.description = description
        #mov.save()
        movs.append(mov)
    Movie.objects.bulk_create(movs)

loadRatings = raw_input("Load Ratings? [y,N]> ")
if('y' in loadRatings.lower()):
    rats = []
    with codecs.open("datasets/movielens/ml-100k/u.data") as f:
      for line in f:
        item = line.strip().split()

        rat = Rating()
        rat.user = item[0]
        rat.movie = Movie.objects.get( id=item[1] ) 
        rat.rating = item[2]
        rats.append( rat )
        #rat.save()
    Rating.objects.bulk_create(rats)

print("success")
