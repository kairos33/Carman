import streamlit as st
import pandas as pd

st.set_page_config(page_title='차계부', page_icon='🚗', layout='wide')

df = pd.read_csv('data.csv', encoding='utf-8')

menu = st.pills('차계부 메뉴선택',['입력','조회,편집','분석'], default='입력')

def save_data():
    li = [date, distance, cost, price, liter, com]
    df.loc[len(df)] = li
    df.to_csv('data.csv', index=False)
    df.to_csv('data_bak.csv', index=False)
    st.success("데이터가 저장되었습니다.")

def save_edited_data():
    df.to_csv('data.csv', index=False)
    df.to_csv('data_bak.csv', index=False)
    st.success("데이터가 저장되었습니다.")

def del_data():
    if len(df) > 0:
        df.drop([len(df)-1], axis=0, inplace=True)
        df.to_csv('data.csv', index=False)
        st.error("마지막 데이터가 삭제되었습니다.")
    else:
        st.warning("삭제할 데이터가 없습니다.")

if menu == '입력':
    date = st.date_input('주유일자', value='today')
    distance = st.number_input('누적운행거리', value=df.iloc[-1,1]+200)
    price = st.number_input('단가', value=df.iloc[-1,3])
    cost = st.number_input('주유금액', value=30000, step=5000)
    try:
        value=cost/price
    except:
        liter = st.number_input('주유량', value=0.00, format='%0.2f' )
    else:
        liter = st.number_input('주유량', value=cost/price, format='%0.2f' )
    com = st.selectbox('정유사', ['S-OIL', 'GS칼텍스', 'SK', '오일뱅크', 'NH농협', '알뜰'])

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    # 저장/삭제 버튼 UI
    save, erase = st.columns(2, gap='medium')

    with save:
        st.button('저장', type='primary', use_container_width=True, on_click=save_data)

    with erase:
        if not st.session_state.confirm_delete:
            if st.button('삭제', use_container_width=True):
                st.session_state.confirm_delete = True
        else:
            st.warning("정말 마지막 데이터를 삭제하시겠습니까?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button('✅ 예, 삭제합니다', use_container_width=True):
                    del_data()
                    st.session_state.confirm_delete = False
            with col2:
                if st.button('❌ 취소', use_container_width=True):
                    st.info("삭제가 취소되었습니다.")
                    st.session_state.confirm_delete = False

elif menu == '조회,편집':
    df = st.data_editor(df, hide_index=True, column_config={
        'DATE':'주유일자',
        'DISTANCE':st.column_config.NumberColumn('누적거리',format='localized'),
        'COST':st.column_config.NumberColumn('주유금액',format='localized'),
        'PRICE':st.column_config.NumberColumn('단가',format='localized'),
        'LITER':st.column_config.NumberColumn('주유량',format='%.2f'),
        'COM':'정유사',
        })
    st.button('저장', type='primary', use_container_width=True, on_click=save_edited_data)

elif menu == '분석':
    TOT_DISTANCE = df.iloc[-1,1]
    TOT_COST = df.iloc[0:-1, 2].sum()
    TOT_LITER = df.iloc[0:-1, 4].sum()    
    st.write(f'누적주유금액 : {df['COST'].sum():,}원')
    st.write(f'누적주유량 : {df['LITER'].sum():,.2f}L')
    st.write(f'평균주유단가 : {df['COST'].sum() / df['LITER'].sum():,.1f}원')
    st.write(f'평균연비 : {TOT_DISTANCE / TOT_LITER:.2f} km/L')
    st.write(f'이동비용 : {TOT_COST / TOT_DISTANCE:,.1f} 원/km')
    st.write('정유사별 주유금액')
    st.dataframe(df.groupby('COM')[['LITER','COST']].sum(), column_config={
        'COM':st.column_config.Column('정유사', width='small'),
        'LITER':st.column_config.NumberColumn('주유량(L)', width='small', format='%.2f'),
        'COST':st.column_config.NumberColumn('주유금액(원)', width='small', format='localized'),
        })