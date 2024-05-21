import requests
from bs4 import BeautifulSoup
from datetime import date
from urllib.parse import urlparse  # Añade esta línea para importar urlparse

# Lista de URLs de búsqueda de empleo
urls = [
    'https://www.linkedin.com/jobs/search?keywords=Hardware&location=Gerona%20y%20alrededores&geoId=90009777&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
    'https://www.linkedin.com/jobs/search?keywords=Hardware%20Engineer&location=Gerona%20y%20alrededores&geoId=90009777&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
    'https://www.linkedin.com/jobs/search?keywords=Ingeniero+electr%C3%B3nico&location=Gerona+y+alrededores&geoId=90009777&trk=public_jobs_jobs-search-bar_search-submit',
    'https://www.linkedin.com/jobs/search?keywords=T%C3%A9cnico%20electr%C3%B3nico&location=Gerona%20y%20alrededores&geoId=90009777&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
    'https://www.linkedin.com/jobs/search?keywords=Dise%C3%B1o%20de%20hardware%20electr%C3%B3nico&location=Gerona%20y%20alrededores&geoId=90009777&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    # Añade más URLs aquí
]

def get_base_link(url):
    # Utiliza urlparse para dividir el enlace en sus componentes
    parsed_url = urlparse(url)
    # Reensambla el enlace utilizando solo el esquema, la red y la ruta (sin los parámetros de la consulta)
    base_link = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    return base_link

# Nombre del archivo .md
filename = "tabla.md"

# Lee el contenido del archivo existente si existe
try:
    with open(filename, "r") as file:
        existing_data = file.readlines()
except FileNotFoundError:
    existing_data = []

# Guarda los enlaces base de las filas existentes en un conjunto
existing_base_links = set()
row_count = 1  # Inicializa el contador de filas
for line in existing_data[2:]:  # Ignora las primeras dos líneas que son el encabezado de la tabla
    parts = line.split("|")
    if len(parts) >= 6:
        link_part = parts[2].strip()
        href_start = link_part.find("(")
        href_end = link_part.find(")")
        if href_start != -1 and href_end != -1:
            href_link = link_part[href_start + 1:href_end]
            existing_base_links.add(get_base_link(href_link))
            row_count += 1  # Incrementa el contador de filas por cada fila existente

# Itera sobre la lista de URLs
for url in urls:
    response = requests.get(url)

    # Verifica que la respuesta sea exitosa
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('div', {'class': 'job-search-card'})

        # Lista para almacenar los nuevos datos
        new_data = []

        for job in job_listings:
            title = job.find('h3', {'class': 'base-search-card__title'}).text.strip().replace('(', '-').replace(')', '-')
            company = job.find('a', {'class': 'hidden-nested-link'}).text.strip()
            location = job.find('span', {'class': 'job-search-card__location'}).text.strip()
            anchor_tag = job.find('a', class_='base-card__full-link')
            href_link = anchor_tag['href']
            date_added = date.today().strftime("%Y-%m-%d")  # Obtiene la fecha actual

            # Obtén la parte relevante del enlace
            base_href_link = get_base_link(href_link)

            # Agrega los datos a la lista de nuevos datos
            new_data.append((title, company, location, href_link, base_href_link, date_added))

        # Escribe los nuevos datos en el archivo .md sin duplicar las filas existentes
        with open(filename, "a") as file:
            for title, company, location, href_link, base_href_link, date_added in new_data:
                if base_href_link not in existing_base_links:
                    # Agrega la fila con el número de fila, el checkbox [ ] y el enlace en la primera columna
                    file.write(f"| {row_count} | [{title}]({href_link}) | {company} | {location} | [ ] | {date_added} |\n")
                    row_count += 1  # Incrementa el contador de filas por cada nueva fila añadida

    else:
        print(f"Failed to fetch job listings from {url}.")

print(f"Nuevos datos agregados al archivo {filename}.")
