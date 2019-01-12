class Instruction:
    """
    Value object representing instruction that the engine should perform
    """

    PROCESS_WEATHER_DATA = "PROCESS_WEATHER_DATA"
    PROCESS_ARTIST = "PROCESS_ARTIST"
    PROCESS_INSTAGRAM_POST = "PROCESS_INSTAGRAM_POST"

    def __init__(self):
        pass


class TwitterRequest:
    """
    Data transfer object representing a received request
    """

    def __init__(self, json_request=None):
        """
        ExecutionRequest assembler
        :param json_request: JSON represented execution request
        """
        self.content = json_request['content']
        self.requested_by = json_request['requestedBy']


class TwitterResponse:
    """
    Data transfer object representing a twitter response
    """

    _to_string = 'Status {}, Description {}, Post_Id {}, Timestamp {}, Content {}'

    def __init__(self, twitter_status=None, description=None):
        """
        TwitterResponse assembler
        :param twitter_status: twitter.Status object
        """
        if twitter_status is None:
            self.status = -1
            self.description = description
        else:
            self.status = 0
            self.description = 'Successfully posted tweet'
            self.post_id = twitter_status.id
            self.timestamp = twitter_status.created_at
            self.content = twitter_status.text

    def __str__(self):
        return self._to_string.format(self.status, self.description, self.post_id, self.timestamp, self.content)

