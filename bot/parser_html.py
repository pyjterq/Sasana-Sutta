import requests
from bs4 import BeautifulSoup
import re

SUTTA_LINKS = 'http://sasana.pl/alfabetycznie'

TRANSLATORS = {
        'vil': 'Piotr Jagodziński',
        'var': 'Varapanyo Bhikkhu',
        'sir': 'Siristru',
        'agr': 'Agrios',
        'kow': 'Hubert Kowalewski',
        'ltw': "Lo'tsa'wa (Dobromił Dowbór)",
        'krz': 'Janusz Krzyżowski',
    }

COLLECTIONS = {
    'dn': 'Zbiór długich mów',
    'mn': 'Zbiór mów średniej długości',
    'sn': 'Zbiór połączonych mów',
    'an': 'Zbiór mów według wyliczeń',
    'kn': 'Mniejszy zbiór mów',
    'jat': 'Bajki buddyjskie',
    'snp': 'Mowy Zebrane',
    'dhp': 'Dhammapada',
}


def get_link_list(url):  # => [link1, link2]
    """
     (net) pobranie glownej strony (alfabetycznie)
    """
    # 1. pobranie tresci
    # response = requests.get(url)

    # 2. parsowanie tresci (wydobywanie linkow)
    # return []
    suttas_links_list = []
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table_of_contents = soup.find('div', class_='yui-content')
    for a in table_of_contents.findAll('a', href=True):
        suttas_links_list.append(a["href"])
    return suttas_links_list


def get_sutta_data_list(link_list):
    """Returns list of results"""
    sutta_text_list = []
    for link in link_list:
        sutta_text = get_sutta_data(link)
        sutta_text_list.append(sutta_text)
    return sutta_text_list


def get_sutta_data(link):
    """
    Results:
        results: {
            title: str,
            paragraph_list: [str...],
            link: str,
            author: str,
            collection: str,
            sutta_nr: int
        }
    """
    # Korzystamy z metody results.update, poniewaz przepisuje
    #  ona dane z jednego slownika do drugiego
    # a to oznacza, ze kod mozemy podzielic na 2 czesci
    # (jedna dla url, druga dla html) i scalic wynik w jedno.

    data = {}

    # 1. url
    data.update(get_sutta_data_from_url(link))

    # 2. html
    data.update(get_sutta_data_from_html(link))

    # print(data['collection'], len(data['collection']))

    return data


def get_sutta_data_from_url(link):
    """
    Results:
        results: {
            link: str,
            author: str,
            collection: str,
            sutta_nr: int
        }
    """

    results = {'url': f'http://sasana.pl{link}'}

    author = TRANSLATORS.get(parse_author_code(link))
    if author is not None:
        results['author'] = author

    collection = COLLECTIONS.get(parse_collection_code(link))
    # print(collection)
    # if collection is not None:
    results['collection'] = collection

    results['sutta_nr'] = parse_sutta_nr(link)
    return results


# def parse_sutta_nr(link):
#     sutta_code = re.search(r'(?<=-)\d+', link)
#     if sutta_code is None:
#         return link
#     else:
#         return int(sutta_code.group())

def parse_sutta_nr(link):
    url_len = len(link)
    sutta_no = []
    dash_counter = 0
    for letter in link:
        if letter == '-':
            dash_counter += 1
            if dash_counter == 2 and url_len > 12:
                sutta_no.append('.')
            if dash_counter == 3:
                # print(''.join(sutta_no), link)
                return ''.join(sutta_no)
            if dash_counter == 1 and url_len < 10:
                # print(''.join(sutta_no), link)  /jat-159-vil
                return ''.join(sutta_no)
            if dash_counter == 2 and url_len <= 12:
                # print(''.join(sutta_no), link)
                return ''.join(sutta_no)
        if letter in "abcdefghijklmnoprstxyz1234567890":
            sutta_no.append(letter)
    # print(link)
    raise ValueError(link)


def parse_author_code(link):
    match_auth = re.search(r'[a-z]{3}$', link)
    return match_auth.group()


def parse_collection_code(link):
    # print(link)
    match_coll = re.search(r'(?<=/)\w+', link)
    match_coll_code = match_coll.group()
    if check_collcode_in_collections(match_coll_code) is True:
        return match_coll_code
    else:
        print("Add COLLECTION code to COLLECTIONS", match_coll_code)


def check_collcode_in_collections(match_coll):
    if match_coll in ['dn', 'mn', 'sn', 'an', 'kn', 'jat', 'snp', 'dhp']:
        return True


def get_sutta_data_from_html(link):
    """
    Results:
        results: {
            title: str,
            title_pali : str
            paragraph_list: [str...],
        }
    """
    # 1. pobieramy tresc strony
    # 2. parsujemy strone
    # 3. pamietaj zeby przepuszczac tylko polskie paragrafy

    results = {}
    response = requests.get(f'http://sasana.pl{link}')
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    results['title'] = parse_sutta_title(soup)

    results['title_pali'] = parse_sutta_title_pali(soup)

    results['paragraph_list'] = parse_all_paragraphs(soup)

    return results


def parse_sutta_title_pali(html_parser):
    title_content_data = html_parser.find('div', class_='page-title')
    title_content = title_content_data.find('span')
    title_content_string = title_content.string
    title_pali = title_content_string.split(' (')
    return title_pali[0]


def parse_all_paragraphs(html_parser):
    if check_page_kind(html_parser) == 'table':
        return parse_paragraph_table(html_parser)
    else:
        return parse_paragraph_list(html_parser)


def check_page_kind(html_parser):
    if html_parser.find('table') is None:
        return
    else:
        paragraph_data_list = html_parser.select('table p')
        for paragraph in paragraph_data_list:
            if len(str(paragraph)) > 400:
                return 'table'


def parse_paragraph_table(html_parser):
    paragraph_list = []
    sutta_content = html_parser.select('table p')
    for paragraph in sutta_content:
        if len(str(paragraph)) > 200:
            pl_paragraph = chcek_lang(paragraph)
            if pl_paragraph is True:
                paragraph_list.append(paragraph.string)

    return paragraph_list


def parse_paragraph_list(html_parser):
    paragraph_list = []
    sutta_content = html_parser.find('div', class_='drop')
    if sutta_content is not None:
        for paragraph in sutta_content.findAll('p', style=False):
            paragraph_list.append(paragraph.string)
    return paragraph_list


def remove_tags(paragraph):
    # br_re = re.compile(r'</?\s{0,2}br/?\s{0,2}>', flags=re.IGNORECASE)
    sup_re = re.compile(r'<sup.+</sup>')
    return sup_re.sub('', str(paragraph))


def chcek_lang(paragraph):
    special_pl_letters = 'ąężźśćłó'
    paragraph_str = (str(paragraph.string)).lower()
    return bool(set(special_pl_letters) & set(paragraph_str))


def parse_sutta_title(html_parser):
    title_content_data = html_parser.find('div', class_='page-title')
    title_content = title_content_data.find('span')
    title_content_string = title_content.string
    title_match = re.search(r'(?<=-.|–.).+\w', title_content_string)
    if title_match is None:
        # print("remove span tag: ", title_content, title_content.string)
        return title_content.string
    else:
        title = title_match.group()
        # print(title_content)
        return title
