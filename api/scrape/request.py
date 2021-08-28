from api.scrape.util import clear_html, scrape_html
from urllib.request import Request, urlopen
from urllib.error import ContentTooShortError, HTTPError, URLError

import ssl
import certifi


def get_page_data(url):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36' }

    if not url:
        return {
            'status': 204,
            'error': 'Url not defined.'
        }

    try:
        req = Request(url, headers = headers)
        response = urlopen(req, context = ssl_context)
        html = clear_html(response.read())
        return {
            'status': 200,
            'data': scrape_html(html),
            'error': None,
        }

    except ContentTooShortError as e:
        return {
            'status': 400,
            'error': str(e)
        }

    except HTTPError as e:
        return {
            'status': e.status,
            'error': str(e.reason),
        }

    except URLError as e:
        return {
            'status': 400,
            'error': str(e.reason),
        }

    except ValueError as e:
        return {
            'status': 400,
            'error': str(e),
        }
