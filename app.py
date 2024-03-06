import socket
import re
import urllib.parse
import requests

def site_up(site):
    try:
        sock = socket.create_connection((site, 80))
        sock.close()
        return True
    except OSError:
        return False

def find_links(page):
    links = re.findall('(href=".*?")', page)
    return [link[6:-1] for link in links]

def is_internal_link(site, link):
    if link.startswith('http'):
        return site in link
    else:
        return True

def is_vulnerable_to_sqli(link):
    query = urllib.parse.urlparse(link).query
    if '=' in query and ' OR 1=1' in query or "' OR 1=1" in query:
        return True
    else:
        return False

site = 'example.com' #aqui voçê coloca o site que quer testar !!!
if site_up(site):
    print(f'{site} está online.')
    page = requests.get(site).text
    links = find_links(page)
    print(f'Encontramos {len(links)} links.')
    internal_links = [link for link in links if is_internal_link(site, link)]
    print(f'{len(internal_links)} são internos.')
    vulnerable_links = [link for link in internal_links if is_vulnerable_to_sqli(link)]
    print(f'{len(vulnerable_links)} são vulneráveis a SQL Injection.')
else:
    print(f'{site} está offline.')
