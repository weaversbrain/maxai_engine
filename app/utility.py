import jinja2
from prompt_base import templateList

def renderTemplate(module: str, data: dict):
    templateEnvironment = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='./'))
    renderedTemplate = templateEnvironment.get_template(templateList[module]).render(data)

    return renderedTemplate