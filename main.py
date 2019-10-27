from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def make_partititon(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def make_split(content, delimiter=": "):
    lst = list()
    for n in content:
        lst.append(n.split(delimiter))
    return lst


def get_card_content(filepath, characteristics_qty=4):
    content_list = list()
    with open(filepath, 'r', encoding='utf8') as file:
        content_list.append(file.read().split('\n'))
    content_list = make_partititon([x for x in content_list[0] if x],
                                   characteristics_qty)
    content_list = list(map(make_split, content_list))
    return [dict(x) for x in content_list]


def get_years_after_foundation(foundation_year):
    return datetime.now().year - foundation_year


def render():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template_index.html')
    years = get_years_after_foundation(foundation_year=1920)
    card_content = get_card_content(filepath='wine.txt')

    rendered_page = template.render(years=years, card_content=card_content)
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


def main():
    render()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
