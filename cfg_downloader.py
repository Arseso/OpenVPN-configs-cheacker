from dataclasses import dataclass
import os
import subprocess
from bs4 import BeautifulSoup as soup
import requests
import tqdm

URL = 'https://ipspeed.info'
PAGE = 'https://ipspeed.info/freevpn_openvpn.php?language=en'

@dataclass
class _File:
    name: str
    method: str
    url: str
    
    def get_for_save(self):
        return self.name, self.method, requests.get(self.url).content.decode()

def name_gen(country: str) -> str:
    i = 1
    while True:
        yield f"{country}{i}"
        i+=1
        
def _save_file(name: str, method: str, content: str, ping: str | None = None) -> None:
    with open(f'./tmp/{f"{name} [{method}] {ping} ms" if ping else f"{name} [{method}]"}.ovpn', "a") as file:
        file.write(content)

def _get_files_from_page() -> list[_File]:
    page = soup(requests.get(PAGE).content)
    files = []
    countries = {}

    # Поиск всех блоков с информацией о VPN-серверах
    entries = page.find_all("div", {"style": "clear: both;"})

    # Перебор каждой записи
    for entry in entries:
        # Извлекаем страну
        country_div = entry.find_next_sibling("div", class_="list", style="float: left; width: 263px;")
        if not country_div:
            continue
        country = country_div.get_text(strip=True)
        if not countries.get(country):
            countries[country] = name_gen(country)
        file_name = next(countries[country])
        # Извлекаем ссылки (может быть несколько ссылок: UDP и TCP)
        link_div = country_div.find_next_sibling("div", class_="list", style="float: left; width: 373px;")
        links = link_div.find_all("a")
        
        
        for link in links:
            href = link.get('href')
            # Определяем тип соединения (UDP или TCP)
            if "udp" in href:
                protocol = "UDP"
            elif "tcp" in href:
                protocol = "TCP"
            else:
                protocol = "Unknown"

            files.append(_File(file_name, protocol, URL+href))
    return files

def _delete_from_tmp():
        
    subprocess.run(
        ["rm", "-rf", "./tmp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    subprocess.run(
        ["mkdir", "tmp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    

def download():
    _delete_from_tmp()
    files = _get_files_from_page()
    for i in tqdm.trange(len(files), desc='DOWNLOADING'):
        _save_file(*files[i].get_for_save())
    
