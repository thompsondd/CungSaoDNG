#import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import streamlit as st
from frontend.frontend import main
import hashlib, time
from backend.main_backend import *

#def form_OTP():
#    #st.session_state["mutan"]+=1
#    with st.form("Xác thực"):
#        otp = st.text_input("Mã OTP")
#        clicked = st.form_submit_button("Xác thực")
#    if clicked:
#        print(f'otp {otp == st.session_state["OTP"]}')
#        if otp == st.session_state["OTP"]:
#            return True
#        else:
#            st.error("Mã OTP sai")
#            if st.button("Gửi lại mã OTP"):
#                st.success("Gửi lại mã thành công")
#                #if  st.session_state["mutan"]>0:
#                #time.sleep(1)
#                    #st.session_state["mutan"]-=1
#                #st.experimental_rerun()

def login():
    security = option_menu(
                menu_title=None,
                options=['Đăng nhập', 'Đăng ký', 'Quên mật khẩu'],
                icons=["person-circle","people-fill","person-lines-fill"],
                menu_icon= "eye",
                default_index=0,
                orientation="horizontal",key="login_selection")
    #print(f"security: {security}")
    if security == "Đăng nhập":

        with st.form("Đăng nhập"):
            username = st.text_input("Tài khoản")
            password = hashlib.sha256(hashlib.sha512(st.text_input("Mật khẩu",type="password").encode()).hexdigest().encode()).hexdigest()
            submitted = st.form_submit_button("Đăng nhập")
            print(f"username:{username}")
            print(f"password:{password}")
            print(f"submitted:{submitted}")
            if submitted:
                print(f"username in :{username}")
                print(f"password in :{password}")
                print(f"submitted in :{submitted}")
                if username in ["None",""]:
                    st.warning("Vui lòng điền thông tin đăng nhập")
                else:
                    key = auth(username,password)
                    if key!=None:
                        st.session_state["mutan"]=2
                        return True,key
                    else:
                        st.error("Thông tin đăng nhập bị sai")

    if security == "Đăng ký":
        with st.form("Đăng ký"):
            name = st.text_input("Họ và tên",key="full_name",value="Nguyễn Huỳnh Hải Vy")
            username = st.text_input("Tài khoản",key="uername",value="vy123")
            email = st.text_input("Email",key="email",value="dnng2002@gmail.com")
            password = st.text_input("Mật khẩu",type="password",key="password",value="vy123~")
            with st.expander("Câu hỏi xác thực danh tính"):
                p1 = st.text_input("Nhập họ và tên người thứ 1 trong gia đình mà bạn biết",key="p1",value="Nguyễn Huỳnh Hải Đăng")
                p2 = st.text_input("Nhập họ và tên người thứ 2 trong gia đình mà bạn biết",key="p2",value="Nguyễn Văn Vui")
            submitted = st.form_submit_button("Đăng ký")
        if submitted:
            print(f"username in :{username}")
            print(f"password in :{password}")
            print(f"submitted in :{submitted}")
            if "None" in [username,password,email] or "" in [username,password,email]:
                st.warning("Vui lòng điền thông tin đăng ký")
            elif "None" in [p1,p2] or "" in [p1,p2] :
                st.warning("Vui lòng điền thông tin xác thực")
            elif get_login_data("key",name):
                st.error(f"'{name}' đã được đăng ký tài khoản.")
                st.info("Nếu quên mật khẩu đăng nhập vui lòng chọn 'Quên mật khẩu' để khôi phục mật khẩu")
            elif not vertify_fp(p1,p2):
                st.error("Thông tin xác thực sai")
                st.info("Vui lòng nhập lại thông tin xác thực")
            elif not vertify_fp(name,"",1):
                st.error(f"{name} không nắm trong danh sách người được phép xem")
                st.info("Vui lòng nhập lại tên ")
            elif get_login_data("username",username):
                st.error(f"'{username}' đã được đăng ký tài khoản.")
                st.info("Vui lòng chọn tên tài khoản khác")
            else:
                st.session_state["OTP"] = generate_OTP()
                if True:#send_email_otp(st.session_state["OTP"],email,name):
                    #with st.form("Xác thực OTP"):
                    with st.container():
                        otp = st.text_input("Mã OTP")
                        clicked = st.button("Xác thực OTP",type="primary")
                        print(f"otp input:{otp}")
                        print(f"clicked:{clicked}")
                        if clicked:
                            print(f"otp input:{otp}")
                            print(f'otp {otp == st.session_state["OTP"]}')
                            if otp == st.session_state["OTP"]:
                                st.success("Xác thực thành công")
                                update_new_user(name,username,password,email)
                            else:
                                st.error("Mã OTP sai")
                        if st.button("Gửi lại mã OTP"):
                            st.success("Gửi lại mã thành công")
                        
    return False,None

def login_selection():
    if "has_login" not in st.session_state:
        st.session_state["has_login"] = False
    if "mutan" not in st.session_state:
        st.session_state["mutan"] =2

    print(f"has_login_reset_out:{st.session_state['has_login']}")
    if st.session_state["has_login"] == False:
        st.session_state["has_login"],st.session_state["login_name"] = login()
        if  st.session_state["mutan"]>0:
            st.session_state["mutan"]-=1
            st.experimental_rerun()

    print(f"has_login:{st.session_state['has_login']}")
    
    if st.session_state["has_login"]:
        main()
        with st.sidebar:
            if st.button("Đăng xuất",key="sign_out_button"):
                st.session_state["has_login"]=False
                st.session_state["login_name"]=None
                print(f"has_login_reset:{st.session_state['has_login']}")
                print(f'mutan remain: {st.session_state["mutan"]}')
                if  st.session_state["mutan"]>0:
                    st.session_state["mutan"]-=1
                    st.experimental_rerun()