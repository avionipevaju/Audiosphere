from yahoo_weather.core.api import api

PORT = 8889
HOST = '0.0.0.0'

if __name__ == '__main__':
    api.run(host=HOST, port=PORT)
