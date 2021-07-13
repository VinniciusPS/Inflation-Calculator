import pandas as pd 

import datetime
import streamlit as st 

# raw data
raw = pd.read_html("http://www.ipeadata.gov.br/ExibeSerie.aspx?stub=1&serid37796=37796&serid36482=36482", attrs = {'class':'dxgvTable'})

# to dataframe
df = pd.DataFrame(raw[0])

# change columns names
df.columns = ['data', 'ipca', 'igpm']

# throw away useless row
df = df.drop(0)

# fill empty values with 0
df[['ipca', 'igpm']] = df[['ipca', 'igpm']].fillna(0)

# change date to datetime format
df['data'] = df['data'].astype('datetime64[ns]')

# cleaning data
df[['ipca', 'igpm']] = df[['ipca', 'igpm']].replace('\.', '', regex=True)
df[['ipca', 'igpm']] = df[['ipca', 'igpm']].replace(',', '', regex=True)

# changing type
df[['ipca', 'igpm']] = df[['ipca', 'igpm']].astype('float')

# changing numeric dimensions
df[['ipca', 'igpm']] = df[['ipca', 'igpm']].apply(lambda x: x/10000)

# today's date
d1 = datetime.datetime.now()

### STREAMLIT ###

st.header('Calculadora de Correção Monetária')

radio = st.radio('Escolha o índice: ', ('IPCA', 'IGP-M'))
init_date = st.date_input('Escolha a data inicial: ', min_value=datetime.date(1996,1,1), max_value=datetime.date(d1.year,d1.month-1,1))
final_date = st.date_input('Escolha a data final: ',min_value=datetime.date(1996,1,1), max_value=datetime.date(d1.year,d1.month-1,1))
money = st.number_input('Insira o montante em reais: ')

def calculate(df, radio, init_date, final_date, money):
    try:
        if radio == 'IGP-M':
            init_datetime = datetime.datetime.strptime(str(init_date)[:-3], '%Y-%m') - datetime.timedelta(days=31)
            final_datetime = datetime.datetime.strptime(str(final_date)[:-3], '%Y-%m')
            div = df[ df['data'] == final_datetime ]['igpm'].values / df[ df['data'] == init_datetime  ]['igpm'].values 
            results = money * div[0]
            str_results = 'Valor corrigido na data final: R$ {0:.2f}'.format(results)

            return ( st.write(str_results)  )
        else:
            init_datetime = datetime.datetime.strptime(str(init_date)[:-3], '%Y-%m') - datetime.timedelta(days=31)
            final_datetime = datetime.datetime.strptime(str(final_date)[:-3], '%Y-%m')
            div = df[ df['data'] == final_datetime ]['ipca'].values / df[ df['data'] == init_datetime  ]['ipca'].values
            results = money * div[0]
            str_results = 'Valor corrigido na data final: R$ {0:.2f}'.format(results)

            return ( st.write(str_results)  )
    except:
        st.write('insira uma data válida')
    
calculate(df, radio, init_date, final_date, money)
