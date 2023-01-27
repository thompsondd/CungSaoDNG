import streamlit as st
from backend import *
import streamlit_nested_layout

st.set_page_config(
    page_title="Website Tra Cứu Sao Hạn Của Đăng Nguyễn",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
c1,c2 = st.columns([1,5])
with c1:
    watch_type = st.radio(
        "Chọn kiểu xem",
        ('Xem cá nhân', 'Xem gia đình', 'Xem tất cả'))
with c2:
    with st.form("Search"):
        years_list, index_year = get_list_time()
        if watch_type=='Xem cá nhân':
            col1,col2 = st.columns(2)
            with col1:
                option = st.selectbox(  "Tên người cần tra sao hạn",
                                    tuple(get_all_full_name()))
                home = st.checkbox("Bao gồm địa chỉ nhà")
            with col2:
                year_now = st.selectbox("Năm hiện tại",
                                    tuple(years_list), index=index_year)
        elif watch_type=='Xem gia đình':
            col1,col2 = st.columns(2)
            with col1:
                option = st.multiselect(  "Tên người cần tra sao hạn",
                                    tuple(get_all_full_name()))
                home = st.checkbox("Bao gồm địa chỉ nhà")
            with col2:
                year_now = st.selectbox("Năm hiện tại",
                                    tuple(years_list), index=index_year)
        else:
            year_now = st.selectbox("Năm hiện tại",
                                    tuple(years_list), index=index_year)
            home = st.checkbox("Bao gồm địa chỉ nhà")
        submitted = st.form_submit_button("Tra cứu")


if submitted:
    if watch_type=='Xem cá nhân':
        data = search_one_person({"Full_name":option},year_now,home)
        st.table(data)
    elif  watch_type=='Xem tất cả':
        data = search_family(get_all_full_name(),year_now,home)
        st.download_button(
            label="Download Excel workbook",
            data=export_excel(search_family(get_all_full_name(),year_now,True)).getvalue(),
            file_name=f"Danh_sach_cung_sao_{year_now}.xlsx",
            mime="application/vnd.ms-excel")
        for key,df in data.items():
            with st.expander(key):
                st.table(df)
    elif  watch_type=='Xem gia đình':
        data = search_family(option,year_now,home)
        st.download_button(
            label="Download Excel workbook",
            data=export_excel(search_family(option,year_now,True)).getvalue(),
            file_name=f"Danh_sach_cung_sao_{year_now}.xlsx",
            mime="application/vnd.ms-excel")
        for key,df in data.items():
            with st.expander(key):
                st.table(df)
