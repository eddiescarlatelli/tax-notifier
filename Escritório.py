import pandas as pd

df = pd.read_csv("D:\Escritorio\FINAL 0.csv")

for telefone in df.columns['telefone']:
    telefone.split()


