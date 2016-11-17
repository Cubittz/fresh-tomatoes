import webbrowser

class Video():
    """ Virtual class for common properties of all videos """

    def __init__(self, video_title, tagline, image_url, trailer_id):
        self.video_title = video_title
        self.tagline = tagline
        self.image_url = image_url
        self.trailer_id = trailer_id


