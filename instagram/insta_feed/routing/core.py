from insta_feed.routing.routing import routing

PORT = 8892
HOST = '0.0.0.0'

if __name__ == '__main__':
    routing.run(host=HOST, port=PORT)
