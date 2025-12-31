
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib

navegador = webdriver.Chrome()
navegador.get("https://web.whatsapp.com/")

while len(navegador.find_elements_by_id("side")) < 1:
    time.sleep(1)

agenda = ["24988271842","22998719290","21994092571","21997922107","21972399452","24999774849","24981508350"," 21997735453","21979760180","21980224364"]

# já estamos com o login feito no whatsapp web
for tel in agenda:
    texto = urllib.parse.quote("Oi, nao precisa responder a mensagem, so estou testando meu codigo de envio automatico.")
    link = f"https://web.whatsapp.com/send?phone={tel}&text={texto}"
    navegador.get(link)
    while len(navegador.find_elements_by_id("side")) < 1:
        time.sleep(1)
    navegador.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').send_keys(Keys.ENTER)
    time.sleep(10)