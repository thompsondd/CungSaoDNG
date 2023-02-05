import streamlit as st
from backend.main_backend import *
import streamlit_nested_layout
#import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

#https://extras.streamlit.app/Contribute

def main():
    c1,c2 = st.columns([1,5])
    with c1:
        watch_type = option_menu(
            menu_title="Chọn kiểu xem",
            options=['Xem cá nhân', 'Xem gia đình', 'Xem tất cả'],
            icons=["person-circle","people-fill","person-lines-fill"],
            menu_icon= "eye",
            default_index=0
            )
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
        if len(option)<1:
                st.error('Vui lòng chọn tên người muốn tra cứu', icon="🚨")
        else:
            if watch_type=='Xem cá nhân':
                data = search_one_person({"Full_name":option},year_now,home)
                st.table(data)
            elif  watch_type=='Xem tất cả':
                if len(option)<1:
                    st.error('Vui lòng chọn tên người muốn tra cứu', icon="🚨")
                data = search_family(get_all_full_name(),year_now,home)
                st.download_button(
                    label="Download Excel workbook",
                    data=export_excel(search_family(get_all_full_name(),year_now,True)).getvalue(),
                    file_name=f"Danh_sach_cung_sao_{year_now}.xlsx",
                    mime="application/vnd.ms-excel")
                for key,df in data.items():
                    with st.expander(key):
                        st.table(df.reset_index(drop=True))
            elif  watch_type=='Xem gia đình':
                data = search_family(option,year_now,home)
                st.download_button(
                    label="Download Excel workbook",
                    data=export_excel(search_family(option,year_now,True)).getvalue(),
                    file_name=f"Danh_sach_cung_sao_{year_now}.xlsx",
                    mime="application/vnd.ms-excel")
                for key,df in data.items():
                    with st.expander(key):
                        st.table(df.reset_index(drop=True))

#if authentication_status:
#    authenticator.logout("Đăng xuất","sidebar")
#    st.success(f"Đăng nhập thành công - {st.session_state['name']}")
#    main()
#elif authentication_status == False:
#    st.error('Tên tài khoản/Mật khẩu sai')
#elif authentication_status == None:
#    st.warning('Vui lòng điền thông tin đăng nhập')
