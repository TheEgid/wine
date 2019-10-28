from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def apply_list_split(lst, delimiter):
    split_points = [i for i, item in enumerate(lst) if delimiter in item]
    split_points.append(len(lst))
    return [lst[i: j] for i, j in zip(split_points, split_points[1:])]


def parse_wines_contents(filepath):
    with open(filepath, encoding='utf8') as f:
        lines = [row.replace('\n', '') for row in f]

    temp_data = list()
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
            temp_data.append(line)

    wines_contents = dict()
    for elem in apply_list_split(temp_data, 'Категория'):
        category = elem[0][1]
        contents = elem[1:]
        wines_contents[category] = [dict(row) for row in
                                    apply_list_split(contents, 'Название')]

    return wines_contents


def get_years_after_foundation():
    foundation_year = 1920
    return datetime.now().year - foundation_year


def render():
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template_index.html')

    years = get_years_after_foundation()
    wines_contents = parse_wines_contents(filepath='products.txt')

    rendered_page = template.render(years=years, wines_contents=wines_contents)
    with open('index.html', 'w', encoding='utf8') as f:
        f.write(rendered_page)


def main():
    render()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
