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


def apply_octothorpe_split(lst):
    split_points = [i for i, item in enumerate(lst) if '#' in item]
    split_points.append(len(lst))
    return [lst[i: j] for i, j in zip(split_points, split_points[1:])]


def get_card_content(filepath, characteristics_qty=4):
    global content_list
    raw_content_list = list()
    with open(filepath, 'r', encoding='utf8') as file:
        for line in file.readlines():
            _line = line.split('\n')[0]
            if _line:
                raw_content_list.append(_line)

    raw_content_list = apply_octothorpe_split(raw_content_list)


    raw_content_list = [x[0].replace('# ', 'Категория: ') for x in raw_content_list])
    for x in raw_content_list:
        print(x)

    print(raw_content_list)
    #
    # breakpoint()
    # fn_list = []
    # # dictionary = dict()
    # for x in raw_content_list:
    #     category = x[0].replace('# ', '')
    #     content_list = x[1:]
    #     #content_list.append([f'Категория: {category}'])
    #
    #     content_list = make_partititon([x for x in content_list if x],
    #                                     characteristics_qty)
    #
    #     content_list = [x.append([f'Категория: {category}']) for x in content_list]
    # # fn_list.append(content_list)
    #     print(content_list)
    # breakpoint()
    # content_list = list(map(make_split, content_list))
    #
    # #return content_list

    #content_list = list(map(make_split, content_list))
    # print(content_list)
    return raw_content_list
    #return [dict(x) for x in raw_content_list if x]


def get_years_after_foundation(foundation_year):
    return datetime.now().year - foundation_year


def render():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template_index.html')
    years = get_years_after_foundation(foundation_year=1920)
    card_content = get_card_content(filepath='products.txt')
    #print(card_content)

    rendered_page = template.render(years=years, card_content=card_content)
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


def main():
    render()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
