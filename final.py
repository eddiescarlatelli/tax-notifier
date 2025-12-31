import pandas as pd
import re
import pywhatkit as kit
import time

#planilha = pd.read_csv("D:\Escritorio\planilha_teste.csv",encoding = "ISO-8859-1", sep = ';')

placas = {"0": "21/01/2025", "1" : "22/01/2025","2" : "23/01/2025", "3" : "24/01/2025", "4" : "27/01/2025", "5" : "28/01/2025", "6" : "29/01/2025", "7" : "30/01/2025", "8": "31/01/2025", "9" : "03/02/2025"}

def enviar_mensagem(numero, mensagem):
    try:
        kit.sendwhatmsg_instantly(
            phone_no=f"+55{numero}", 
            message=mensagem,
            tab_close=True,
            close_time=10
        )
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Erro ao enviar para {numero}: {str(e)}")
        return False

envios = pd.read_csv("D:\Escritorio\planilha_update.csv",encoding = "ISO-8859-1", sep = ';')
envios['Fax ou Cel'] = envios['Fax ou Cel'].astype(str).str.replace('\.0', '')

for index, status in enumerate(envios['Status']):
  if status == 'Nao enviado':
    continue
  else:
    if envios['Modelo'][index] < 2010:
      continue
    else:
        nome = envios['Nome'][index].split()
        mensagem = f"Oi, {nome[0]} aqui e o Jorginho Miranda, tudo bem? Seu veiculo {envios['Marca'][index]} com placa {envios['Placa'][index]} tem o IPVA vencendo dia {placas[envios['Placa'][index][-1]]}."
        telefone = envios['Fax ou Cel'][index]
        print(telefone)
        enviar_mensagem(telefone, mensagem)