import webbrowser

class Video():
    """ Virtual class for common properties of all videos """

    def __init__(self, video_title, plot, image_url, trailer_id):
        self.video_title = video_title
        self.plot = plot
        self.image_url = image_url
        self.trailer_id = trailer_id


