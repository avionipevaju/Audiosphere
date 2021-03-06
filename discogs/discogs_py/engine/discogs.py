import logging
import os
import urllib2

from bs4 import BeautifulSoup
from discogs_client.client import Client

from discogs_py.engine import utils


class Discogs:
    """
    Enables querying of the Discogs database - The largest music database and marketplace in the world
    """

    DISCOGS_QUERY = 'https://www.discogs.com/search?limit=250&sort=want%2Cdesc&style_exact={}&page={}'

    def __init__(self):
        """
        Initializes Discogs search engine with Discogs API credentials
        """
        self.search_engine = Client('moody_py', user_token=os.environ["discogs_user_token"])

    def get_random_track_by_artist(self, artist_name):
        """
        Returns a random track from a random album of a given artist
        :param artist_name: Artist to search by
        :return: Random track of a given artist, None if an artist doesnt exist
        """
        try:
            artist = self.search_engine.search(artist_name, type='artist')[0]
            random_release = utils.get_random_from_collection(artist.releases)
            logging.info('Found random release %s for artist %s with tracklist %s', random_release.title, artist.name,
                         random_release.tracklist)
            random_track = utils.get_random_from_collection(random_release.tracklist)
            logging.info('Resolved track %s for artist %s', random_track.title, artist.name)
            return "{} {}".format(artist_name, random_track.title)
        except Exception as e:
            logging.error(e.message)
            return None

    def get_random_track_by_genre(self, genre, relevancy=1):
        """
        Returns a random track with the given genre
        :param genre: Genre to search by
        :param relevancy: Indicates the wanted level of relevancy or popularity of the album
        containing the search track
        :return: Random track of a given genre, None if a genre isn't valid
        """
        try:
            url = self.DISCOGS_QUERY.format(genre, relevancy)
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            albums = soup.findAll(attrs={'class': 'card card_large float_fix shortcut_navigable'})
            random_album_id = utils.get_random_from_collection(albums, 'data-object-id')
            album = self.search_engine.release(random_album_id)
            artist = album.artists[0].name
            track_list = album.tracklist
            logging.info('Found album %s - %s with track list %s for genre %s',artist, album.title, album.tracklist, genre)
            track = "{} {}".format(artist, utils.get_random_from_collection(track_list).title)
            logging.info('Resolved track: %s for genre: %s with relevancy: %s', track, genre, relevancy)
            return track
        except Exception as e:
            logging.error('Error resolving track by genre %s', e.message)
