import json
import requests
from jinja2 import Environment, FileSystemLoader

# Obtenemos todos los datos
def get_data(url):
    url = url
    try:
        res = requests.get(url)
        return json.loads(res.text)
    except requests.exceptions.HTTPError as e:
        return e.response.text

# Obtenemos el número de la última página
def get_last_page():
    url = "https://catfact.ninja/facts"
    try:
        data_json = get_data(url)
        return data_json.get('last_page')
    except requests.exceptions.HTTPError as e:
        return e.response.text

# Obtenemos los hechos de cada página y los agregamos al arreglo facts
def get_facts():
    facts = []
    for page in range(1, get_last_page() + 1):
        url = f"https://catfact.ninja/facts/?page={page}"
        data_json = get_data(url)
        facts += data_json.get('data')
    return facts

content = get_facts()

# Configuramos la carpeta donde buscará los templates
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# Indicamos el archivo html donde se renderizará el listado
template = env.get_template('lista.html')

output = template.render(content = content)
print(output)

