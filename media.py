import video

class Movie(video.Video):
    """ This class provides a way to store movie related information """
    
    def __init__(self, video_title, plot, image_url, trailer_id, 
                 running_time, certificate):
        video.Video.__init__(self, video_title, plot, image_url, trailer_id)
        self.running_time = running_time
        self.certificate = certificate


class Tv_Show(video.Video):
    """ This class provides a way to store TV Show information """
    # no additional fields have been added to Tv_Show, but wanted it in
    # it's own class so that option was readily available without impacting
    # the movie or the video virtual class
    def __init__(self, video_title, plot, image_url, trailer_id):
        video.Video.__init__(self, video_title, plot, image_url, trailer_id)

        

        
