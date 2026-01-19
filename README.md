## Automated message system to remind clients of their IPVA (Brazilian tax for vehicles) through WhatsApp, using the MyZap API

This project was developed to easy the mass sending of notifications about this tax to the vehicle owners. The system processes a datasheet,
verify numbers and sends personalized messages using WhatsApp

### Functionalities:
  - CSV/Excel datasheet reading with vehicle data;
  - Automatic validation of WhatsApp numbers;
  - Attempted verification with multiple DDD's;
  - Vehicle model verification (vehicles that are 15 years old or older don't pay);
  - Personalized messages with vehicle data;
  - Automatic saving;
  - Maximum load control;
  - WhatsApp report at the end of each run;
  - Timestamp registry in Brazilian time.

### Technologies:
  - Python 3;
  - Pandas - data manipulation;
  - Requests - for HTTP usage;
  - PyTZ - timezone conversion;
  - MyZap API - WhatsApp interface;

### Prerequisites:
  1. Library installation:
     - `pip install pandas requests pytz openpyxl`

  2. MyZap Api:
  - Install Node.js (https://nodejs.org)
  - Cloning the MyZap repository from Bill Barsch
  - Configuring .env file
  - ```
     PORT = 3333
     TOKEN = your_api_token
     ENGINE = 2
    ```
  3. Starting the server:
    - `npm start`

  4. Connect to Whatsapp using QR Code:
      ```
      curl -X POST http://127.0.0.1:3333/start -H "Content-Type: application/json" -H "apitoken: your_api_token" -H "sessionkey: your_session_key" -d "{\"session\":\"your_session\"}"   
      # Aguardar 20 segundos   
      curl "http://127.0.0.1:3333/getQrCode?session=your_session&sessionkey=your_session_key" -H "apitoken: your_api_token" --output qrcode.png   
      # Escanear o QR Code com o WhatsApp
      ```
Spreadsheet structure:
  The CSV spreadsheet must be like the following:

  | Nome (Owner's name) | Placa (Licensing Plate) | Renavam (Registry Number)| Modelo (Year of the model) | Marca (Maker) | Fax ou Cel (Main Phone Number)| TelRes (Alternative Phone Number)|
  |------|-------|---------|--------|-------|------------|--------|
  |John Smith|ABC1234|123456789|2015|FIAT/UNO|(24) 99999-9999|(24) 99999-9999|

### How to use:
  1. Initiate the MyZap server:
  - ```
       cd C:\your\path\myzap\
       npm start
       ```
  2. Execute the script:
  - `python tax-notifier.py`
      
  
  
    
  

      
