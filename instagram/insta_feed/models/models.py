class InstagramResponse:
    """
    Data transfer object representing an instagram response
    """

    def __init__(self, username,  post_image_url, post_caption):
        """
        InstagramResponse assembler
        :param username: Instagram username
        :param post_image_url: Url of the instagram image for a given post
        :param post_caption: Caption corresponding to the image of the given post
        """
        self.username = username
        self.image_url = post_image_url
        self.caption = post_caption
