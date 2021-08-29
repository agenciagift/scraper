from bs4 import BeautifulSoup


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


def get_soup_title(soup):
    if not soup.title:
        return ''

    return soup.title.string or ''


def get_soup_description(soup):
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


def get_soup_image(soup):
    return get_meta_content(soup, 'og:image') or get_img_source(soup)


def scrape_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = get_soup_title(soup)
    description = get_soup_description(soup)
    image = get_soup_image(soup)

    return {
        'title': title,
        'description': description,
        'image': image,
    }
