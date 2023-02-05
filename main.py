from frontend import login_page
import streamlit as st

st.set_page_config(
    page_title="Website Tra Cứu Sao Hạn Của Đăng Nguyễn",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
login_page.login_selection()