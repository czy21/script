import jinja2

if __name__ == '__main__':
    a = jinja2.Template("{{ a1 }}").render(**{"a1": "haha"})
    print("a")