import media, fresh_tomatoes
import tmdbsimple as tmdb, requests

tmdb.API_KEY = "d9a3d233a7c254745ebfbba029781234"
tmdb.CONFIG_PATTERN = "http://api.themoviedb.org/3/configuration?api_key={key}"

url = tmdb.CONFIG_PATTERN.format(key=tmdb.API_KEY)
r = requests.get(url)
config = r.json()

base_url = config["images"]["base_url"]+'original'

movies = []

in_cinemas = tmdb.Movies()
response = in_cinemas.now_playing()
for m in in_cinemas.results:
    movie = tmdb.Movies(m['id'])
    response = movie.info()
    if (movie.videos()["results"]):
        trailer_id = movie.videos()["results"][0]["key"]
    else:
        trailer_id = ""
        
    new_item = media.Movie(movie.title.encode('cp1252') ,
                           movie.overview.encode('cp1252'),
                           base_url + movie.poster_path,
                           trailer_id,
                           movie.runtime,
                           movie.rating)
    movies.append(new_item)
    

tv_shows = []
top_rated = tmdb.TV()
response = top_rated.popular()
for t in top_rated.results:
    tv_show = tmdb.TV(t['id'])
    response = tv_show.info()
    if (tv_show.videos()["results"]):
        trailer_id = tv_show.videos()["results"][0]["key"]
    else:
        trailer_id = ""

    new_item = media.Tv_Show(tv_show.original_name.encode('cp1252'),
                             tv_show.overview.encode('cp1252'),
                             base_url + tv_show.poster_path,
                             trailer_id)
    tv_shows.append(new_item)

fresh_tomatoes.open_movies_page(movies, tv_shows)
