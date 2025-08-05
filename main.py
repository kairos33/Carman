import streamlit as st
import pandas as pd
# from datetime import date
# today = date.today()

st.set_page_config(page_title='차계부', page_icon='🏗️', layout='wide')

df = pd.read_csv('data.csv', encoding=utf-8)
df_comma = df.style.format(thousands=',')
# pd.to_datetime(df['DATE'])

st.dataframe(df.iloc[-5:], hide_index=True, column_config={
    'DATE':st.column_config.DateColumn('주유일자'),
    'DISTANCE':st.column_config.NumberColumn('누적거리',format='localized'),
    'COST':st.column_config.NumberColumn('주유금액',format='localized'),
    'PRICE':st.column_config.NumberColumn('단가',format='localized'),
    'LITER':st.column_config.NumberColumn('주유량',format='%.2f'),
    })

date = st.date_input('주유일자', value='today')
distance = st.number_input('누적운행거리', min_value=df.iloc[-1,1])
cost = st.number_input('주유금액', value=30000, step=5000 )
price = st.number_input('단가', value=None )
try:
    value=cost/price
except:
    liter = st.number_input('주유량', value=0.00, format='%0.2f' )
else:
    liter = st.number_input('주유량', value=cost/price, format='%0.2f' )
com = st.selectbox('정유사', ['S-OIL', 'GS', 'SK', '오일뱅크', 'NH농협', '알뜰'])

def save_data():
    li = [date, distance, cost, price, liter, com]
    df.loc[len(df)] = li
    df.to_csv('data.csv', index=False)
    df.to_csv('data_bak.csv', index=False)

def del_data():
    # li = [date, distance, cost, price, liter, com]
    # df.loc[len(df)] = li
    df.drop([len(df)-1], axis=0, inplace=True)
    df.to_csv('data.csv', index=False)

save, erase = st.columns(2, gap='medium')

with save:
    st.button('저장', type='primary', use_container_width=True, on_click=save_data)
with erase:
    st.button('삭제', use_container_width=True, on_click=del_data)
