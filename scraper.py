from bs4 import BeautifulSoup
import requests
 
# sample web page
sample_web_page = 'https://web.whatsapp.com/'
 
# call get method to request that page
page = requests.get(sample_web_page).read().decode('utf-8')
 
# with the help of beautifulSoup and html parser create soup
soup = BeautifulSoup(page.content, "html.parser")
 
child_soup = soup.find_all('div')
 
text = 'O número de telefone compartilhado por url é inválido'
 
# we will search the tag with in which text is same as given text
for i in child_soup:
    print(i.string)
