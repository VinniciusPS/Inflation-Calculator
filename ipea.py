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
d1 = datetime.date.today()

### STREAMLIT ###
st.header('Calculadora de Correção Monetária')
radio = st.radio('Escolha o índice: ', ('IPCA', 'IGP-M'))
money = st.number_input('Insira o montante em reais: ')
init_date = st.date_input('Escolha a data inicial: ', min_value=datetime.date(1996,1,1), max_value=d1)
final_date = st.date_input('Escolha a data final: ',min_value=datetime.date(1996,1,1), max_value=d1)


def calculate(df, radio, init_date, final_date, money):
    try:
        init_datetime = datetime.datetime.strptime(str(init_date)[:-3], '%Y-%m') - datetime.timedelta(days=31)
        final_datetime = datetime.datetime.strptime(str(final_date)[:-3], '%Y-%m')

        # Filtrar intervalo de datas
        df_filtered = df[(df['data'] >= init_datetime) & (df['data'] <= final_datetime)]
        
        if radio == 'IGP-M':
            div = df[ df['data'] == final_datetime ]['igpm'].values / df[ df['data'] == init_datetime  ]['igpm'].values 
            results = money * div[0]
            str_results = 'Valor corrigido na data final: R$ {0:.2f}'.format(results)

            # Exibir o resultado
            st.write(str_results)
            
        else:
            div = df[ df['data'] == final_datetime ]['ipca'].values / df[ df['data'] == init_datetime  ]['ipca'].values
            results = money * div[0]
            str_results = 'Valor corrigido na data final: R$ {0:.2f}'.format(results)

            # Exibir o resultado
            st.write(str_results)
            
             # Gráfico com st.bar_chart
            chart_df = df_filtered[['data', 'ipca']].set_index('data')
            st.bar_chart(chart_df)

            #return ( st.write(str_results)  )
    except:
        st.write('insira uma data válida')

calculate(df, radio, init_date, final_date, money)
