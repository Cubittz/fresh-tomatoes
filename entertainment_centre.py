import media, fresh_tomatoes
import tmdbsimple as tmdb, requests

# tmdbsimple configuration variables (api for The Movie Database  http://github.com/celiao/tmdbsimple)
tmdb.API_KEY = "d9a3d233a7c254745ebfbba029781234"
tmdb.CONFIG_PATTERN = "http://api.themoviedb.org/3/configuration?api_key={key}"

# set url for all api requests to pass through
url = tmdb.CONFIG_PATTERN.format(key=tmdb.API_KEY)
r = requests.get(url)
config = r.json()

# base_url to conveniently locate images
base_url = config["images"]["base_url"]+'original'

# define movies array
movies = []

# connect to tmdb and retrieve list of movies defined in now_playing() function
in_cinemas = tmdb.Movies()
response = in_cinemas.now_playing()
# iterate through list 
for m in in_cinemas.results:
     # look up individual film info by id
    movie = tmdb.Movies(m['id'])
    response = movie.info()
    # see if info has anything in the videos results list
    if (movie.videos()["results"]):
        trailer_id = movie.videos()["results"][0]["key"]  # if so, grab url for first video
    else:
        trailer_id = ""  # else leave trailer_id blank
    
    # map movie info to an instance of class media.Movie    
    new_item = media.Movie(movie.title.encode('cp1252') ,  # video_title
                           movie.overview.encode('cp1252'), # plot
                           base_url + movie.poster_path,  # image_url 
                           trailer_id,  # trailer_id
                           movie.runtime,  # running_time
                           movie.rating)  # certificate
    # add movie to movies array
    movies.append(new_item)
    
# define tv_shows array
tv_shows = []

# connect to tmdb and retrieve list of tv shows defined in popular() function
top_rated = tmdb.TV()
response = top_rated.popular()
# iterate through list
for t in top_rated.results:
    # look up individual tv show info by id
    tv_show = tmdb.TV(t['id'])
    response = tv_show.info()
    # see if info has anything in the videos results list
    if (tv_show.videos()["results"]):
        trailer_id = tv_show.videos()["results"][0]["key"]  # if so, grab url for first video
    else:
        trailer_id = ""  # else leave trailer_id blank

    # map tv_show info to an instance of class media.Tv_Show
    new_item = media.Tv_Show(tv_show.original_name.encode('cp1252'),  # video_title
                             tv_show.overview.encode('cp1252'),  # plot
                             base_url + tv_show.poster_path,  # image_url 
                             trailer_id)  # trailer_id
    # add tv_show to tv_shows array
    tv_shows.append(new_item)
# pass both arrays to open_movies_page function in fresh_tomatoes
fresh_tomatoes.open_movies_page(movies, tv_shows)
