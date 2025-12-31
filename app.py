import keyboard
import glob
import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import urllib
import pywhatkit as kit
# catches all files in given directory
lista = glob.glob("D:/Escritorio/*.csv")
# user interaction variables
#placa = input("Qual o final da placa para ser enviada a mensagem? ")
mensagem = input("Qual a mensagem deseja enviar? ")
caminho_chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
options = webdriver.ChromeOptions()


# dataframe created given user inputs
planilha = pd.read_csv("D:/Escritorio/FINAL " + placa + ".csv" , encoding = "ISO-8859-1", sep = ';')
#a log to store all phone numbers
agenda = []
# create column planilha['Status'] = "sucesso ou falha"

# loop to catch all phone numbers in spreadsheet to be added to the log
# in the loop all non numeric chars are taken off the string to later it is formatted as a phone number
for index, telefone in enumerate(planilha['Fax ou Cel']):
    telefone = str(telefone)
    telefoneFormat = re.sub('[()-]','',telefone)
    placa = planilha['Placa'][index]
    # checks if the value in the cell is null to be searched in the earlier columnm
    if telefoneFormat == "nan":
        new_telefone = planilha['TelRes'][index]
        new_telefone2 = re.sub('[()-]','',new_telefone)
        agenda.append(new_telefone2)
    # checks if the string is a telephone number, this was implemented due to some cells having the contact name instead of number
    if telefoneFormat.isnumeric():
        agenda.append(telefoneFormat)
    #checks if the telephone number is a landline or cellphone
    if len(telefoneFormat) != 11:
        new_telefone = planilha["TelRes"][index]
        new_telefone2 = re.sub('[()-]','',new_telefone)
        agenda.append(new_telefone2)
    
# transforms the list in a set to avoid sending messages to the same recipient twice
agenda = set(agenda)

#agenda = ["24988271842","22998719290","21994092571","21997922107","21972399452","24999774849","24981508350"," 21997735453","21979760180","21980224364"]
agenda = ["24988271842","24999888855"]
lista = []
# Enter the phone number of the recipient (including country code)
navegador = webdriver.Chrome(service = Service(caminho_chrome))
navegador.get("https://facebook.com")
time.sleep(15)
for telefone in agenda:
    phone_number = "+55" + telefone
    # Enter the message you want to send
    message = mensagem
    # Enter the time at which you want to send the message (24-hour format)
    # The following example sends the message immediately
    
    kit.sendwhatmsg_instantly(phone_number, message, tab_close=True)
    isSucesso = True
    try:
       navegador.find_element(By.XPATH,'//*[@id="side"]/div[1]/div/div/div[2]')
       isSucesso = False
    except:
        pass
        
    lista.append(isSucesso)

print(lista)
 



    # Use the kit.sendwhatmsg() function to send the message




