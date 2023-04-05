import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import re
from string import ascii_uppercase
import csv
import time

base_url = "https://www3.gogoanimes.fi/"
url_lista_animes = "https://www3.gogoanimes.fi/anime-list.html" #Lista de animes em ordem alfabetica
url = base_url

ascii_uppercase

Anime = []
anime_info={}

#lista de caracteres
charecters = list(ascii_uppercase)
charecters.insert(0,"special")

main_start = time.time()

for trat_caracter in charecters[:]:

    print("\rProcessing {}.".format(trat_caracter),end='')
    #url = re.legendado('special',trat_caracter,url_lista_animes)
    
    # solicitando o código-fonte html do site através da função Request do módulo urllib e lendo-o usando a função urlopen

    #Requisitando a url com Request
    url_link = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    url_page = urlopen(url_link).read()
    url_html = bs(url_page, 'html.parser')
    
    #Pegando todas as divs com conteudo de animes hospedados
    containers = url_html.find_all('div',class_='content_episode revent datagrild')
    
    print("\rProcessing {}..".format(trat_caracter),end='')
    
    #Looping para pegar as informacoes dos animes
    for itens in containers[:]:
        
        animes = itens.find_all('div',class_ = "nome")
        html_links = itens.find_all('a') #getting url of anime
        
        for i,anime in enumerate(animes[:]):
            nome=''
            descricao=''
            temporada=''
            genero=''
            url_do_anime=''
            status=''
            episodes=''
            status
            lancamento=''
            movie=''
            legendado=''
            
            
            try:
                titulo = anime.text#nome do anime
                html_link = html_links[i].get('href') #url do anime

                #pega o nome junto a temporada no nome
                #usando  regex search function para pegar o titulo e temporada
                if re.search(r"temporada [0-9]?",titulo):
                    nome,temporada = re.split(r"temporada [0-9]?",titulo) #separando o conteúdo por temporada
                elif re.search(r"[0-9][a-z]+? temporada",titulo):
                    nome,temporada = re.split(r"[0-9][a-z]+? temporada",titulo)
                elif re.search(r"[0-9][a-z][a-z]",titulo):
                    try:
                        nome,temporada = re.split(r"[0-9]['nd','rd','th']+",titulo) #separando os titulos por temporada
                    except:
                        nome = re.split(r"[0-9]['nd','rd','th']+",titulo)[0] 
                else:
                    nome = titulo #caso não tenha temporada

                #iniciando um padrão para procurar por " temporada " no título do Anime usando regex
                pattern = r"^([0-9][a-z]+? temporada | temporada [0-9][a-z]+?\s )$"
                temporada = re.search(pattern,titulo)

                if not temporada:
                    pattern = r"[0-9]['nd','rd','th']+"
                    temporada = re.search(pattern,titulo)

                if temporada:
                    pass #caso encontre temporada
                else:
                    temporada = ["temporada 1"] #caso ainda não tenha achado temporada
                
                #Lógica para alterar para dublado baseado no titulo do anime
                if 'Dub' in titulo or 'dub' in titulo:
                    legendado = 'Dub'
                else:
                    legendado = 'legendado'
                

                #url_do_anime para redirecionar para a página principal do anime para extrair informações mais detalhadas, como:
                #1. descricao
                #2. status
                #3. lançamento
                #4. genero
                #5. total de epsodios
                url_do_anime = main_url+html_link
                url_do_anime = url_do_anime.replace('watch','anime')
                
                url_link = Request(url_do_anime, headers={'User-Agent': 'Mozilla/5.0'})
                url_page = urlopen(url_link).read()
                url_html = bs(url_page, 'html.parser')

                containers = url_html.find_all('div',class_="main_body")
                contents = containers[0].find_all('div',class_='right')


                #descrição
                descricao = contents[0].find_all('p')[0].text 
                #status, data de lançamento , genero e número total de episódios do anime
                temp=[]
                genero=[]
                for i in contents[0].find_all('a')[2:]:
                    temp.append(i.text)

                status,lancamento = temp[:2]
                genero = temp[2:]
                genero = ', '.join(genero)

                containers = containers[0].find_all('div',class_='list_episode')
                try:
                    text = containers[0].find('span',class_='nome').text
                    text = re.search('Episode [0-9]+',text)
                    episodes = re.search('[0-9]+',text[0])[0]
                    if int(episodes) > 0 and int(episodes) < 2:
                        movie = 'Movie'
                    else:
                        movie = 'Series'
                except:
                    episodes = 'None'
                    movie = 'None'


                print("\rProcessing {}...".format(trat_caracter),end='')

                #pegando as informações na pagina principal do anime
                anime_info['Anime titulo'] = nome
                anime_info['descricao'] = descricao
                anime_info['Current/Latest temporada'] = temporada[0]
                anime_info['URL'] = url_do_anime
                anime_info['Status'] = status
                anime_info['Initial Air Date'] = lancamento
                anime_info['genero'] = genero
                anime_info['Episodes Aired'] = episodes
                anime_info['Series/Movie'] = movie
                anime_info['legendado/Dub'] = legendado

                armaz_info = anime_info.copy()

                Anime.append(armaz_info)
                
            except:

                print("\rProcessing {}...".format(trat_caracter),end='')
                
                try:
                 #Reunir todos os dados coletados até agora em um dicionário para estruturá-lo com base no título do anime
#                   adicionando todas as informações extraídas do Anime       
                    anime_info['Titulo do Anime'] = nome
                    anime_info['Descrição'] = descricao
                    anime_info['Temporada'] = temporada[0]
                    anime_info['URL'] = url_do_anime
                    anime_info['Status'] = status
                    anime_info['Lançamento'] = lancamento
                    anime_info['Gênero'] = genero
                    anime_info['Episodios'] = episodes
                    anime_info['Serie/Filme'] = movie
                    anime_info['legendado/Dub'] = legendado
                except:
                    pass

                #Após cada loop armazena as info dos animes na variavel armaz_info
                armaz_info = anime_info.copy()

                Anime.append(armaz_info)
                
#                 break
    
    print("\rProcessed {}     ".format(trat_caracter))
    
main_end = time.time() - main_start
print('\rTermino')
print("Tempo: {}s".format(main_end))

print("Total de animes:",len(Anime))

#Gravar os dados não estruturados coletados até agora em um formato estruturado (.csv)

#Colunas de titulo
header = ['Titulo do Anime', 'Descricao', 'Temporada', 'Episodios', 'Status', 'Lançamento', 'Genero', 'legendado/Dub', 'Serie/Filme', 'URL']

#grava os dado em arquivo .csv
with open(r'C:\Users\hugohsk\Documentos\trabp1AnimeWebScraping\AnimeWebScrapingTrab.csv', 'w+', newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnomes=header)

    writer.writeheader()
    writer.writerows(Anime)
    
print("Dados salvos em: ",r'C:\Users\hugohsk\Documentos\trabp1AnimeWebScraping\AnimeWebScrapingTrab.csv')

