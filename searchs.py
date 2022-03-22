import requests
from bs4 import BeautifulSoup
import lxml
import time
import sys

query = str(sys.argv[1])
print("Query:",query)

header = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36" ,
'referer':'https://www.google.com/'
}

html_doc = requests.get("https://www.google.com/search?q="+query, headers=header)
soup = BeautifulSoup(html_doc.content, 'lxml')

encontrado = False
pagina = None

divs = soup.findAll('div', {'class':'yuRUbf'})
for div in divs:
    urlList = div.find('a').get('href').replace('/url?q=', '').split("&sa")
    url = urlList[0]
    urlLower = urlList[0].lower()
    if 'sinova' in urlLower and ('.co' in urlLower or 'co.linkedin' in urlLower):
        pagina = 1
        print("Página: "+str(pagina),"URL:"+urlList[0])
        encontrado = True
        break

if not encontrado:
    time.sleep(1)
    siguienteURL = "https://www.google.com"+str(soup.find('a', {'id':'pnnext'}).get('href'))
    siguiente = None
    siguienteSoup = None
    
    cont = 2
    while not encontrado:
        time.sleep(1)
        try:
            siguiente = requests.get(siguienteURL)
            siguienteSoup = BeautifulSoup(siguiente.text, 'lxml')
            divs1 = siguienteSoup.findAll('div', {'class':'egMi0'})
            #print(siguienteURL)
            for div1 in divs1:
                urlList1 = div1.find('a').get('href').replace('/url?q=', '').split("&sa")
                url1 = urlList1[0]
                urlLower1 = urlList1[0].lower()
                if 'sinova' in urlLower1 and ('.co' in urlLower1 or 'co.linkedin' in urlLower1):
                    pagina = cont
                    print("Página: "+str(pagina),"URL:"+urlList1[0], "N° Rtas:",len(divs1))
                    encontrado = True
                    break
            if not encontrado:
                cont += 1
                siguienteURL = "https://www.google.com"+str(siguienteSoup.find('a', {'aria-label':'Página siguiente'}).get('href'))
                #print("https://www.google.com"+siguienteSoup.find('a', {'class':'nBDE1b G5eFlf', 'aria-label':'Página siguiente'}).get('href'))
        except:
            print("Palabra no encontrada")    
            break