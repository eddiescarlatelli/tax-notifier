import pandas as pd
import re

#first step is to sort the datasheet using the final digit of the 'Placa' column
#in order to do that use an auxiliary column and use the RIGHTB()/RIGHT() function from Excel/Sheets
#select the whole datasheet and go to data > sort range > advanced range
#check data has header row box and sort ascending selecting the auxiliary column and sort
#delete column

#check path for datasheet

df = pd.read_csv("/Users/eduardoscarlatelli/Documents/DespachanteMiranda/IPVA 2026.csv",encoding = "ISO-8859-1", sep = ';')

#drops the 'Placa' column empty values, as you can't know when the client will need to be notified
df = df.dropna(subset=['Placa'])

#drop some content that isnt relevant in my case

special_values = ['AUTO ITALIA PETROPOLIS LTDA', 'EXPRESSO BRASILEIRO TRANSPORTES LTDA', 'A W ROSSI CIA LTDA', 'IMPERIAL COMERCIO E TRANSPORTE DE GAS LTDA', 'MOVEIS PEDRO II LTDA', 'INDUSTRIA E COMERCIO SAMOVEIS LTDA', 'TURP TRANSPORTE URBANO DE PETROPOLIS LTDA']
mask = ~df['Nome'].isin(special_values)

#create a copy to avoid Pandas indexing errors
df_filtered = df[mask].copy()

#fills the empty nan columns in 'TelRes' and 'Fax ou Cel' with empty strings to simplify conversion next
df_filtered[['TelRes', 'Fax ou Cel']] = df_filtered[['TelRes', 'Fax ou Cel']].fillna('')

#turns every phone number in the datasheet into a single string with no separations
df_filtered['TelRes'] = df_filtered['TelRes'].apply(lambda x: re.sub(r'[()-]', '', str(x)))
df_filtered['Fax ou Cel'] = df_filtered['Fax ou Cel'].apply(lambda x: re.sub(r'[()-]', '', str(x)))

#drops repeated rows, with no paramater, because the same name can have different cars and the same plate can have different owners
df_filtered = df_filtered.drop_duplicates(keep='last')

#saves the final result in a excel file
df_filtered = df_filtered.fillna('')
df_filtered.to_csv('/Users/eduardoscarlatelli/Documents/DespachanteMiranda/IPVA_2026_filtered.csv', index=False, sep=';', encoding='ISO-8859-1')
