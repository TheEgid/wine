from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def apply_list_split(lst: list, delimiter: str) -> list:
    split_points = [index for index, item in enumerate(lst)
                    if delimiter in item]
    split_points.append(len(lst))
    return [lst[j: i] for j, i in zip(split_points, split_points[1:])]


def parse_vines_content(filepath: str) -> dict:
    with open(filepath, encoding='utf8') as f:
        lines = [row.replace('\n', '') for row in f]

    delimiter = 'Категория'
    raw_data_list = list()
    for line in lines:
        if ': ' in line:
            line = line.split(': ')
        elif '# ' in line:
            line = [delimiter, line.replace('# ','')]
        elif 'Выгодное предложение' in line:
            line = ['Акция', line]
        else:
            line = None
        if line:
            raw_data_list.append(line)

    vines_content = dict()
    for data in apply_list_split(raw_data_list, delimiter=delimiter):
        _category_name, *_category_content = data
        _, category_name = _category_name
        splitted_content_list = apply_list_split(_category_content,
                                                 delimiter='Название')
        vines_content[category_name] = [dict(content) for content in
                                        splitted_content_list]
    return vines_content


def get_years_after_foundation() -> int:
    foundation_year = 1920
    return datetime.now().year - foundation_year


def render():
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template_index.html')
    years = get_years_after_foundation()
    wines_content = parse_vines_content(filepath='products.txt')

    rendered_page = template.render(years=years, wines_content=wines_content)
    with open('index.html', 'w', encoding='utf8') as f:
        f.write(rendered_page)


def main():
    render()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
