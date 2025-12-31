import pywhatkit as kit
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=options)

def verificar_numero(numero):
    try:
        driver.get(f'https://web.whatsapp.com/send/?phone=55{numero}&text&type=phone_number')
        
        try:
            # Espera até 20 segundos pela mensagem de erro
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, 
                '/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div'))
            )
            return False  # Número inválido
        except TimeoutException:
            return True  # Número válido
            
    except Exception as e:
        print(f"Erro ao verificar numero {numero}: {str(e)}")
        return False

def enviar_mensagem(numero, mensagem):
    try:
        if not verificar_numero(numero):
            print(f"Numero {numero} invalido ou nao possui WhatsApp")
            return False
            
        kit.sendwhatmsg_instantly(
            phone_no=f"+55{numero}",
            message=mensagem,
            tab_close=True,
            close_time=2
        )
        time.sleep(10)
        return True
        
    except Exception as e:
        print(f"Erro ao enviar para {numero}: {str(e)}")
        return False

if __name__ == "__main__":
    numeros = ["24988271842", "24999888855"]
    mensagem = input("Digite a mensagem a ser enviada: ")
    
    resultados = []
    for numero in numeros:
        print(f"\nTentando enviar para {numero}...")
        sucesso = enviar_mensagem(numero, mensagem)
        resultados.append(sucesso)
        time.sleep(2)
    
    print(f"\nResultados dos envios:")
    for i, resultado in enumerate(resultados):
        print(f"Numero {numeros[i]}: {'Sucesso' if resultado else 'Falha'}")