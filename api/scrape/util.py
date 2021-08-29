from bs4 import BeautifulSoup
from urllib.parse import urlparse


def clear_html(html):
    html = html.decode('utf-8')
    return ' '.join(html.split()).replace('> <', '><')


def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def get_meta_content(soup, name):
    content = ''

    for meta in soup.find_all('meta'):
        if meta.get('name') == name or meta.get('property') == name:
            content = meta.get('content')

    return content


def get_title(soup):
    if not soup.title:
        return ''

    return soup.title.string or ''


def get_description(soup):
    description = get_meta_content(soup, 'description')

    if not description:
        body_text = soup.find('body').get_text()
        description = smart_truncate(body_text, length=220)

    return description


def get_img_source(soup):
    image_element = soup.find('img')

    if image_element:
        return image_element.get('src')
    else:
        return ''


def get_image(soup):
    src = get_meta_content(soup, 'og:image')

    if not src:
        return get_img_source(soup)

    if (
        src.startswith('http://') or
        src.startswith('https://') or
        src.startswith('/')
    ):
        return src

    return '/' + src


def absolute_path(path, base):
    if not path:
        return path

    path = str(path)

    if (
        path.startswith('//') or
        path.startswith('http://') or
        path.startswith('https://') or
        path.startswith('data:image/png;base64,') or
        path.startswith('data:text/plain;base64,') or
        path.startswith('data:text/html;charset=US-ASCII,') or
        path.startswith('data:text/html,') or
        path.startswith('data:,')
    ):
        return path

    base = str(base)

    if path.startswith('/'):
        parse_result = urlparse(base)
        print('PARSE RESULT', parse_result)
        base = base.replace(parse_result.path, '')

    return base.rstrip('/') + '/' + path.lstrip('/')


def scrape_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    return {
        'title': get_title(soup),
        'description': get_description(soup),
        'image': get_image(soup),
    }
