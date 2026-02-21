import requests
import pandas as pd
from datetime import datetime
import time
import pytz
import random

#initial configs
LOCAL_SERVER = "http://127.0.0.1:3333"
API_TOKEN = "your_api_token"
SESSION = "your_session"
SESSION_KEY = "your_session_key"
#setting up a daily load so Meta doesnt block the number
MAX_DAILY_LOAD = 100
#phone number to send reports
ADMIN = "your_number"

#dictionary containing the dates the client has to be notified about
placas = {"0": "21/01/2026", "1" : "22/01/2026","2" : "23/01/2026", "3" : "26/01/2026", "4" : "27/01/2026", "5" : "28/01/2026", "6" : "29/01/2026", "7" : "30/01/2026", "8": "02/02/2026", "9" : "03/02/2026"}


def send_message(number, message):
    url = f"{LOCAL_SERVER}/sendText"

    #headers the myzap api sentText function requires
    headers = {
        "Content-Type": "application/json",
        "apitoken": API_TOKEN,
        "sessionkey": SESSION_KEY
    }

    #sets up the payload to be put in the json
    payload = {
        "session": SESSION,
        "number": number,
        "text": message
    }

    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        data = response.json()

        print("Resposta da API:")
        print(f"Status HTTP: {response.status_code}")
        
        #checks if the message was sent
        if data.get("result") == 200:
            #if sent it loads the timestamp from the json to the variable so it can be saved later on and returns True
            timestamp = data.get("data",{}).get("timestamp","")
            return True, timestamp
        elif data.get("response") == False:
            profile = data.get("profile",{})
            #the json is different if the message is not sent, so it checks that value and returns False
            if not profile.get("numberExists", True):
                return False, None
            
        return False, None

    except Exception as e:
        #checks for other kinds of errors
        print(f"Erro : {e}")
        return False, None

def result_datasheet():

    #reads the file to check phone numbers
    file = "D:\\Escritorio\\IPVA_2026_filtered.csv"
    df = pd.read_csv(file,encoding = "ISO-8859-1", sep = ';')
    
    #fills the empty cells with empty string to avoid errors in the loop ahead
    df = df.fillna('')

    #transforms the float numbers in the columns as strings and delete the .0 at the end
    if 'Fax ou Cel' in df.columns:
        df['Fax ou Cel'] = df['Fax ou Cel'].astype(str).str.replace('.0', '', regex=False)
    
    if 'TelRes' in df.columns:
        df['TelRes'] = df['TelRes'].astype(str).str.replace('.0', '', regex=False)
    
    #creates the Status and Timestamp columns for internal control later 
    if 'Status' not in df.columns:
        df['Status'] = ''
    if 'Horario' not in df.columns:
        df['Horario'] = ''

    #creates variables for progress check
    total = len(df)
    sent_today = 0
    total_sent = len(df[df['Status'] == 'Enviado'])
    invalid = 0
    
    #lists of greetings and connectors to make the message seem more humane and not bot-like
    greetings = ['Ola', 'Oi', 'E ai']
    connectors = ["aqui e o", "e o","sou o"]
    
    #creating variables for error checking and taking out the year that is hardcoded
    error_detection = 0
    current_year = datetime.now().year
    tax_free = current_year - 15

    for index, row in df.iterrows():
        #checks if the model year of the car is 15 years old or greater, if it is the car doesnt pay taxes
        if row.iloc[3] < tax_free:
            df.at[index, 'Status'] = 'Isento'
            continue
        
        #the program is run a number of times so Meta doesnt block the number, so if the column Status is empty, thats where it has to begin from
        if row['Status'] != '':
            continue
        
        #breaks the loop if it reaches the daily load
        if sent_today >= MAX_DAILY_LOAD:
            break
        
        #makes the greeting and connector random
        greeting = random.choice(greetings)
        connector = random.choice(connectors)

        number = str(row['Fax ou Cel'])
        tel_res = str(row.get('TelRes',''))
        name = row['Nome'].split()[0]
        #sets up the message to be sent
        message = f"{greeting}, {name} {connector} Jorginho Miranda, tudo bem? Seu veiculo {row['Marca']} com placa {row['Placa']} e RENAVAM {row['Renavam']} tem o IPVA vencendo dia {placas[row['Placa'][-1]]}."

        sent = False
        timestamp = None

        if number and number.isdigit():
            if len(number) == 11:
                #if the number includes the DDD, the length will be 11, so it adds the DDI and sends the message
                print(f"Tentando: 55{number}")
                sent, timestamp = send_message(f"55{number}", message)
            
            elif len(number) == 9:
                #if it doesnt include the DDD, it tries filling with the most common DDD's the client works with
                for ddd in ["5524","5521","5532"]:
                    print(f"Tentando: {ddd}{number}")
                    sent, timestamp = send_message(f"{ddd}{number}", message)
                    if sent:
                        break
        
        #in case the number in the 'Fax ou Cel' column doesnt work, we go to the 'TelRes' column to try it, doing the same checks as before
        if not sent and tel_res and tel_res.isdigit():
            if len(tel_res) == 11:
                print(f"Tentando: 55{tel_res}")
                sent, timestamp = send_message(f"55{tel_res}", message)
            
            elif len(tel_res) == 9:
                for ddd in ["5524","5521","5532"]:
                    print(f"Tentando: {ddd}{tel_res}")
                    sent, timestamp = send_message(f"{ddd}{tel_res}", message)
                    if sent:
                        break
        if sent:
            #if the message is sent we put the Sent label in the Status column and the time it was sent in the Timestamp (Horario) column
            dt_brasilia = datetime.fromtimestamp(timestamp, tz=pytz.timezone('America/Sao_Paulo'))
            formatted_datetime = dt_brasilia.strftime("%d/%m/%Y %H:%M:%S")
            
            df.at[index,'Status'] = 'Enviado'
            df.at[index,'Horario'] = formatted_datetime
            sent_today+=1
            error_detection = 0

        else:
            #if the message is not sent we put the invalid number label in the status column so the client knows that this number wasnt notified
            df.at[index,'Status'] = 'Numero Invalido'
            invalid+=1
            error_detection+=1
        #puts a timer at every 65 numbers so that Meta wont see as a spamming bot
        if sent_today > 0 and sent_today % 65 == 0:
            time.sleep(300)

        #a timer between every message so Meta wont see it as a spamming bot
        time.sleep(random.randint(30,40))
        
        #if the API disconnects it will see every number as invalid, so we add this check so the program ends
        if error_detection >= 10:
            print("API desconectada")
            #creates a variable to check what is most likely the first occurrence after the API disconnects
            false_invalid = index - 10
            #erases all the "wrong" invalids, so it tries again the next time it runs
            for i in range(false_invalid + 1, index + 1):
                df.at[i, 'Status'] = ''

            break
    
    #at the end of the loop sends a report to the administrator so it knows how the program ran
    admin_message = f"REPORT:\nEnviados hoje: {sent_today};\nInvalidos: {invalid};\nRestantes:{total - (total_sent + sent_today + invalid)}"
    send_message(ADMIN, admin_message)
        

    #saves the changes made in the datasheet back into the file        
    df.to_csv(file, index = False, sep=';', encoding='ISO-8859-1')


if __name__ == "__main__":
    result_datasheet()