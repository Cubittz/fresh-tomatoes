import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile,
        .tv-show-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover,
        .tv-show-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile, .tv-show-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        
        //popover
        $(document).ready(function () {
                $('[data-toggle="popover"]').popover();
            });
            
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
        // Animate in the tv shows when the page loads
        $(document).ready(function () {
          $('.tv-show-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes What to Watch!</a>
          </div>
        </div>
      </div>
    </div>
    <div>
        <ul class="nav nav-tabs" role="tablist">
            <li role="presentation" class="active"><a href="#movie" aria-controls="movie" role="tab" data-toggle="tab">Movies</a></li>
            <li role="presentation"><a href="#tv_show" aria-controls="tv_show" role="tab" data-toggle="tab">TV Shows</a></li>
        </ul>
    
        <div class="tab-content">
            <div role="tabpanel" class="tab-pane fade in active" id="movie">
                <div class="row">
                    <h2 class="col-sm-12 text-primary">Now Showing in Theatres</h2>
                    {movie_tiles}
                </div>
            </div>
            <div role="tabpanel" class="tab-pane fade" id="tv_show">
                <div class="row">
                    <h2 class="col-sm-12 text-primary">Must Watch TV</h2>
                    {tv_show_tiles}
                </div>
            </div>
        </div>
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-4 col-lg-3 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <span href="#" id="{trailer_youtube_id}" data-toggle="popover"
        data-animation="true"
        data-placement="bottom"
        data-trigger="hover"
        title="{movie_title}"
        data-html="true"
        data-content="{plot}<br/>
                    <b>Certificate: </b>{certificate}<br/>
                    <b>Running Time: </b>{running_time}">
        <img src="{image_url}" width="165" height="257">
    </span>
    <h3>{movie_title}</h3>
</div>
'''

# A single tv show entry html template
tv_show_tile_content = '''
<div class="col-md-4 col-lg-3 tv-show-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <span href="#" id="{trailer_youtube_id}" data-toggle="popover"
        data-animation="true"
        data-placement="bottom"
        data-trigger="hover"
        title="{tv_show_title}"
        data-html="true"
        data-content="{plot}">
        <img src="{image_url}" width="165" height="257">
    </span>
    <h3>{tv_show_title}</h3>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        
        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.video_title,
            plot=movie.plot,
            image_url=movie.image_url,
            certificate=movie.certificate,
            running_time=movie.running_time,
            trailer_youtube_id=movie.trailer_id
        )
    return content

def create_tv_show_tiles_content(tv_shows):
    # The HTML content for this section of the page
    content = ''
    for tv_show in tv_shows:
       
        # Append the tile for the movie with its content filled in
        content += tv_show_tile_content.format(
            tv_show_title=tv_show.video_title,
            plot=tv_show.plot,
            image_url=tv_show.image_url,
            trailer_youtube_id=tv_show.trailer_id
        )
    return content

def open_movies_page(movies, tv_shows):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies)
                                              , tv_show_tiles=create_tv_show_tiles_content(tv_shows))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible
