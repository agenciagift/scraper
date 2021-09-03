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
        body = soup.find('body')
        if body:
            body_text = body.get_text()
        else:
            body_text = ''
        description = smart_truncate(body_text, length=220)

    return description


def get_img_source(image_element):
    if image_element:
        return image_element.get('src')
    else:
        return ''


def get_all_images(soup, base):
    path_list = []
    og_image = get_meta_content(soup, 'og:image')

    if (og_image):
        path_list.append(og_image)

    for element in soup.find_all('img'):
        img_source = get_img_source(element)
        abs_path = absolute_path(img_source, base)
        if (img_source and abs_path not in path_list):
            path_list.append(abs_path)

    return path_list


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
        base = base.replace(parse_result.path, '')

    return base.rstrip('/') + '/' + path.lstrip('/')


def scrape_html(html, base):
    soup = BeautifulSoup(html, 'html.parser')

    return {
        'title': get_title(soup),
        'description': get_description(soup),
        'images': get_all_images(soup, base),
    }
