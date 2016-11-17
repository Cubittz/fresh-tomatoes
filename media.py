import video

class Movie(video.Video):
    """ This class provides a way to store movie related information """
    
    def __init__(self, video_title, tagline, image_url, trailer_id, running_time, certificate):
        video.Video.__init__(self, video_title, tagline, image_url, trailer_id)
        self.running_time = running_time
        self.certificate = certificate


class Tv_Show(video.Video):
    """ This class provides a way to store TV Show information """

    def __init__(self, video_title, tagline, image_url, trailer_id):
        video.Video.__init__(self, video_title, tagline, image_url, trailer_id)

        

        
