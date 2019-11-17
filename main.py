from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_file_content(filepath: str) -> list:
    with open(filepath, encoding='utf8') as f:
        return [line.replace('\n', '') for line in f]


def add_to_dict(lst: list) -> dict:
    out_dict = dict()
    for item in lst:
        key, value = item
        out_dict.update({key: value})
    return out_dict


def get_split_points(lst: list, delimiter: str) -> list:
    """
    lst = [['Category', 'High'], ['p1', 1], ['Category', 'Low'], ['p2', 2]]
    list(get_split_points(lst, 'Category')) --> [0, 2, 4]
    """
    for split_point, item in enumerate(lst):
        if delimiter in item:
            yield split_point
        if split_point + 1 == len(lst):
            yield len(lst)


def split_into_blocks_by_delimiter(lst: list, delimiter: str) -> list:
    """
    lst = [['Category', 'High'], ['p1', 1], ['Category', 'Low'], ['p2', 2]]
    list(split_by_delimiter(lst, "Category")) -->
        [[['Category', 'High'], ['p1', 1]], [['Category', 'Low'], ['p2', 2]]]
    """
    split_points = list(get_split_points(lst, delimiter))
    offset_split_points = split_points[1:]
    for cut_start_el, cut_end_el in zip(split_points, offset_split_points):
        yield lst[cut_start_el: cut_end_el]


def parse_wine(file_lines: list) -> dict:
    delimiter = 'Категория'
    preprocessed_lines = list()
    wine = dict()

    for line in file_lines:
        if ': ' in line:
            line = line.split(': ')
        elif '# ' in line:
            line = [delimiter, line.replace('# ', '')]
        elif 'Выгодное предложение' in line:
            line = ['Акция', line]
        else:
            line = None
        if line:
            preprocessed_lines.append(line)

    for category_descr_lines in split_into_blocks_by_delimiter(
            preprocessed_lines, delimiter=delimiter):

        _category_name, *_category_attrs = category_descr_lines
        _, category_name = _category_name
        categories_with_wine_attrs = split_into_blocks_by_delimiter(
            _category_attrs, delimiter='Название')

        wine[category_name] = [add_to_dict(category) for category
                               in categories_with_wine_attrs]
    return wine


def get_years_after_foundation() -> int:
    foundation_year = 1920
    return datetime.now().year - foundation_year


def render():
    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template_index.html')
    years = get_years_after_foundation()
    file_lines = get_file_content(filepath='products.txt')
    wine = parse_wine(file_lines)
    rendered_page = template.render(years=years, wines_content=wine)
    with open('index.html', 'w', encoding='utf8') as f:
        f.write(rendered_page)


def main():
    render()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()