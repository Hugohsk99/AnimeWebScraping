import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent

ua = UserAgent()

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
}

def raspar_dados_animes(url):
    time.sleep(2)  # Aguarde 2 segundos entre as solicitações
    response = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    animes = []
    
    table = soup.find("table", {"class": "top-ranking-table"})
    rows = table.find_all("tr", {"class": "ranking-list"})
    
    for row in rows:
        print(row)  # Diagnóstico: imprimir a linha atual
        title_tag = row.find("div", {"class": "di-ib clearfix"}).find("a")
        title = title_tag.text if title_tag else None
        url = title_tag["href"] if title_tag else None
        score_tag = row.find("td", {"class": "score ac fs14"}).find("span")
        score = score_tag.text if score_tag else None
        rank_tag = row.find("span", {"class": "rank"})
        rank = rank_tag.text.strip() if rank_tag else None
        
        animes.append({"Título": title, "URL": url, "Pontuação": score, "Ranking": rank})
    
    return animes

url = "https://myanimelist.net/topanime.php"
dados_animes = raspar_dados_animes(url)

df_animes = pd.DataFrame(dados_animes)
df_animes.to_excel("animes.xlsx", index=False)

print(df_animes)
