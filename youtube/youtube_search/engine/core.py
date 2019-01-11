from youtube_search.engine.api import api

PORT = 8890
HOST = '0.0.0.0'

if __name__ == '__main__':
    api.run(host=HOST, port=PORT)
