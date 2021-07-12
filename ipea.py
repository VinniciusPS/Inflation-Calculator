import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import html5lib
import re 

import datetime
import streamlit as st 


raw = pd.read_html("http://www.ipeadata.gov.br/ExibeSerie.aspx?stub=1&serid37796=37796&serid36482=36482", attrs = {'class':'dxgvTable'})

df = pd.DataFrame(raw[0])

df.columns = ['data', 'ipca', 'igpm']
df = df.drop(0)

df['igpm'] = df['igpm'].fillna(0)
df['data'] = df['data'].astype('datetime64[ns]')

df1 = df.copy()

df1['igpm'] = df1['igpm'].replace('\.', '', regex=True)
df1['igpm'] = df1['igpm'].replace(',', '', regex=True).astype('float')

df1['ipca'] = df1['ipca'].replace('\.', '', regex=True)
df1['ipca'] = df1['ipca'].replace(',', '', regex=True).astype('float')

df1['igpm'] = df1['igpm'].fillna(0)
df1['igpm'] = df1['igpm'].apply(lambda x: x/10000)

df1['ipca'] = df1['ipca'].fillna(0)
df1['ipca'] = df1['ipca'].apply(lambda x: x/10000) 

d1 = datetime.datetime.now()

### STREAMLIT ###

st.header('Calculadora de Correção Monetária')


radio = st.radio('Escolha o índice: ', ('IPCA', 'IGP-M'))
init_date = st.date_input('Escolha a data inicial: ', min_value=datetime.date(1996,1,1), max_value=datetime.date(d1.year,d1.month-1,1))
final_date = st.date_input('Escolha a data final: ',min_value=datetime.date(1996,1,1), max_value=datetime.date(d1.year,d1.month-1,1))
money = st.number_input("insira o montate em reais: ")

def calculate(df1, radio, init_date, final_date, money):
    try:
        if radio == 'IGP-M':
            init_datetime = datetime.datetime.strptime(str(init_date)[:-3], '%Y-%m') - datetime.timedelta(days=31)
            final_datetime = datetime.datetime.strptime(str(final_date)[:-3], '%Y-%m')
            div = df1[ df1['data'] == final_datetime ]['igpm'].values / df1[ df1['data'] == init_datetime  ]['igpm'].values     

            return ( st.write(money * div[0])  )
        else:
            init_datetime = datetime.datetime.strptime(str(init_date)[:-3], '%Y-%m') - datetime.timedelta(days=31)
            final_datetime = datetime.datetime.strptime(str(final_date)[:-3], '%Y-%m')
            div = df1[ df1['data'] == final_datetime ]['ipca'].values / df1[ df1['data'] == init_datetime  ]['ipca'].values

            return ( st.write(money * div[0])  )
    except:
        st.write('insira uma data válida')
    
calculate(df1, radio, init_date, final_date, money)

    
    



    


    





