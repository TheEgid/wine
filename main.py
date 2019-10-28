from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def apply_list_split(lst, delimiter):
    split_points = [i for i, item in enumerate(lst) if delimiter in item]
    split_points.append(len(lst))
    return [lst[i: j] for i, j in zip(split_points, split_points[1:])]


def get_wines_contents(filepath):
    with open(filepath, encoding='utf8') as f:
        lines = [row.replace('\n', '') for row in f]

    raw_data = list()
    for line in lines:
        if ': ' in line:
            line = line.split(': ')
        elif '# ' in line:
            line = ['Категория', line.replace('# ', '')]
        elif 'Выгодное предложение' in line:
            line = ['Акция', line]
        else:
            line = None
        if line:
            raw_data.append(line)

    wines_contents = dict()
    for elem in apply_list_split(raw_data, 'Категория'):
        category = elem[0][1]
        content_items = elem[1:]
        wines_contents[category] = [dict(x) for x in
                                   apply_list_split(content_items, 'Название')]
    return wines_contents


def get_years_after_foundation():
    foundation_year = 1920
    return datetime.now().year - foundation_year


def render():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template_index.html')
    years = get_years_after_foundation()
    wines_contents = get_wines_contents(filepath='products.txt')
    print(wines_contents)

    rendered_page = template.render(years=years, wines_contents=wines_contents)
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


def main():
    render()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
