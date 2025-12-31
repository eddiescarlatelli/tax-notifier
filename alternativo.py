from selenium import webdriver

#CONFIGURAR O SELENIUM
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
servico = Service(GeckoDriverManager().install())
navegador = webdriver.Firefox(service=servico)

# CONFIGURAR LISTA DE NUMEROS
# arquivo_numeros = open('numeros.txt','r')
numeros = ["24988271842", "24999888855"]

# for linha in arquivo_numeros:
#     linha = linha.strip()
#     numeros.append(linha)
# arquivo_numeros.close()

# # ABRE ARQUIVO DE RESULTADOS
# arquivo_resultado = open('resultado.txt','w')
resultado = []


#VALIDAR SE O LOGIN FOI FEITO
navegador.get('https://web.whatsapp.com/');
navegador.implicitly_wait(3.0)
validador = True

# VALIDAR NUMERO
def isElementPresent(xpath):
        try:
            navegador.find_element(xpath)
            return True
        except:
            return False
            
if validador is True:
    print('-----------------------------------')
    print('ATENCAO: FACA O LOGIN E TECLE ENTER')
    print('-----------------------------------')
    input('...')
    positivo = 0
    negativo = 0
    for numero in numeros:
        navegador.get('https://web.whatsapp.com/send/?phone=55'+ numero +
        '&text&type=phone_number')
        navegador.implicitly_wait(20.0)

        # VERIFICA SE É E SALVA EM NOVO ARQUIVO O RESULTADO
        mensagem_erro = '/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div[1]'
        if isElementPresent(mensagem_erro):
            print("numero invalido")
        else:
            print("numero valido")
        
        try:
            #mensagem_erro = navegador.find_element('xpath','/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div[1]').is_displayed()
            
            print("Resultado: {}... NEGATIVO".format(numero))
            resultado.append("Numero: ")
            resultado.append(numero)
            resultado.append(" - Status: NAO WHATSAPP \n")
            negativo += 1
        except:
            print("Resultado: {}... POSITIVO".format(numero))
            resultado.append("Numero: ")
            resultado.append(numero)
            resultado.append(" - Status: OK \n")
            positivo += 1


print('\n--- RESULTADO ---')
print("TOTAL DE NUMEROS: {}\nPOSITIVO: {}\nNEGATIVO: {}".format((positivo+negativo),positivo,negativo))
print('----------------')
