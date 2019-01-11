import requests
from flask import Flask

from insta_feed import utils
from insta_feed.models.models import InstagramResponse
from insta_feed.scraper.scraper import InstagramScraper

INSTAGRAM_URL = 'https://www.instagram.com/'

routing = Flask(__name__)
scraper = InstagramScraper()


@routing.route('/insta-feed/api/get-post/<instagram_username>')
def get_post(instagram_username):
    """
    Rest endpoint for getting the latest Instagram post for a given account
    :param instagram_username: Instagram account username
    :return: InstagramResponse representing the latest post from the given account
    """
    try:
        results = scraper.profile_page_recent_posts(INSTAGRAM_URL + instagram_username)
    except requests.HTTPError:
        return utils.create_json_error_response('500', 'User ' + instagram_username + ' doesn\'t exist', 500)

    if len(results) == 0:
        return utils.create_json_error_response('500', 'Couldn\'t get posts for username ' + instagram_username, 500)

    latest_post = results[0]
    instagram_image_url = latest_post['display_url']
    captions = latest_post['edge_media_to_caption']['edges']

    if len(captions) == 0:
        instagram_caption = None
    else:
        instagram_caption = captions[0]['node']['text']

    instagram_response = InstagramResponse(instagram_username, instagram_image_url, instagram_caption)
    return utils.create_json_response(instagram_response)

