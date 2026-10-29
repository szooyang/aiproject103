import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력해주세요!')
b=st.selectbox('좋아하는 음식을 선택하세요!',['마라탕','떡볶이','만두'])
if st.button('인사말 생성'):
  st.write('반갑습니다!')
