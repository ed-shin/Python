# This is default crawler using requests module
# Recommend to use it with bs4 module

import requests


class NetworkCrawler:

    @staticmethod
    def request_get(url, params):
        try:
            response = requests.get(url, params=params)
            return response.text
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            print('Timeout exception')
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print('TooManyRedirects exception')
        except requests.exceptions.RequestException:
            # catastrophic error. bail.
            print('RequestException exception, need to check url')

        return ''

    @staticmethod
    def request_post(url, data):
        try:
            response = requests.post(url, data=data)
            return response.text
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            print('Timeout exception')
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print('TooManyRedirects exception')
        except requests.exceptions.RequestException:
            # catastrophic error. bail.
            print('RequestException exception, need to check url')

        return ''

