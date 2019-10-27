from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_years_after_foundation(foundation_year):
    return datetime.now().year - foundation_year


def render():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template_index.html')
    years = get_years_after_foundation(foundation_year=1920)
    rendered_page = template.render(year=years)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    render()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()