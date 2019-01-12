import logging
import os

from twitter import (Api, TwitterError)

from moody_py.engine import utils
from moody_py.engine.model import TwitterResponse
from moody_py.storage.storage import Redis


class Moody:
    """
     Enables moody_py Twitter functionality by using python-twitter wrapper for Twitter API.
    """

    def __init__(self):
        """
        Initializes python-twitter wrapper with the Twitter API credentials
        """
        self.api = Api(consumer_key=os.environ["consumer_key"],
                       consumer_secret=os.environ["consumer_secret"],
                       access_token_key=os.environ["access_token_key"],
                       access_token_secret=os.environ["access_token_secret"])
        self.redis_search_engine = Redis()
        logging.info('App name: ' + self.redis_search_engine.get_string('app:name'))

    def verify_credentials(self):
        """
        Verifies if the given tokens are valid
        :return: A boolean value stating if the credentials are valid
        """
        try:
            user = self.api.VerifyCredentials()
            logging.info('Successfully verified ' + user.screen_name)
            return True
        except TwitterError as e:
            logging.error('Error verifying credentials: %s', e.message[0]['message'])
            return False

    def validate_request(self, twitter_request, authorization_header):
        """
        Validates a request by matching the authorization header
        :param twitter_request: Request received on routing endpoints
        :param authorization_header: Header containing the authorization details
        :return: Boolean True if validation is successful False otherwise
        """
        received_passkey = authorization_header.split(" ")[1]
        user_passkey = self.redis_search_engine.get_string('user:' + twitter_request.requested_by)
        if received_passkey == user_passkey:
            return True
        else:
            logging.warn('Error validating request for user %s', twitter_request.requested_by)
            return False

    def tweet(self, twitter_request):
        """
        Posts a tweet to a Twitter account.
        :param twitter_request: TwitterRequest containing necessary tweet information
        :return: TwitterResponse stating if the tweet has been posted
        """
        twitter_content = twitter_request.content
        if twitter_content is None or len(twitter_content) == 0:
            return TwitterResponse(description='Twitter content to post cannot be empty!')
        try:
            status = self.api.PostUpdate(twitter_content)
            logging.info('Posted twit with status: %s', status)
            return TwitterResponse(status)
        except TwitterError as e:
            logging.error('Error posting twit: %s', e.message[0]['message'])
            return TwitterResponse(description='Fatal error while posting tweet. ' + e.message[0]['message'])

    def mood(self, twitter_request):
        """
        Resolves a genre based on the YahooWeather condition code
        :param twitter_request: TwitterRequest containing necessary YahooWeather condition code
        :return: a genre for a given YahooWeather condition code
        """
        genre_list = self.redis_search_engine.get_genre_list(twitter_request.content)
        genre = utils.get_random_from_collection(genre_list)
        logging.info('Resolved genre %s for YahooWeather condition code %s', genre, twitter_request.content)
        return genre
