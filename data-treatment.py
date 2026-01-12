import pandas as pd

#first step is to sort the datasheet using the final digit of the 'Placa' column
#in order to do that use an auxiliary column and use the RIGHTB()/RIGHT() function from Excel/Sheets
#select the whole datasheet and go to data > sort range > advanced range
#check data has header row box and sort ascending selecting the auxiliary column and sort
#delete column

#check path for datasheet

df = pd.read_csv("D:\Escritorio\planilha_update.csv",encoding = "ISO-8859-1", sep = ';')

#drops the 'Placa' column empty values, as you can't know when the client will need to be notified

df = df.dropna(subset=['Placa'])

#drop some content that isnt relevant in my case

df = pd.read_csv("IPVA 2026 - PROCESSO.csv",encoding = "ISO-8859-1", sep = ',')
df = df.dropna(subset=['Placa'])

special_values = ['AUTO ITALIA PETROPOLIS LTDA']
mask = ~df['Nome'].isin(special_values)

df_filtered = df[mask]

