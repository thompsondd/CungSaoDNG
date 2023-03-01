import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from backend.main_backend import *
import pandas as pd

#names = ['John Smith','Rebecca Briggs']
#usernames = ['jsmith','rbriggs']
#passwords = ['123','456']

#hashed_passwords = stauth.Hasher(passwords).generate()

try:
    load_dotenv(".env")
    DETA_KEY = os.getenv("DETA_KEY")
except:
    DETA_KEY = st.secrets["DETA_KEY"]
deta = Deta(DETA_KEY)

MetaData = deta.Base("MetaData")
AddressInfo = deta.Base("AddressInfo")
DataFiles = deta.Drive("DataFiles")
LoginData = deta.Base("LoginData")

def process(data):
    d={}
    for i in data.keys():
        d.update({i:list(data[i].values())})
    return d

emails, names, usernames, hashed_passwords = list(process(pd.DataFrame(LoginData.fetch().items).to_dict()).values())

def generate(usernames,names,passwords):
    a ={ "credentials":{"usernames":{}},
         "cookie":{
                    "expiry_days": 0,
                    "key": "some_signature_key", # Must be string
                    "name": "some_cookie_name"
                },
        "preauthorized":{
                             "emails":""
                        }
        }
    for id,username in enumerate(usernames):
        a['credentials']["usernames"].update({username:{"name":names[id],"password":{passwords[id]}}})
    return a


security = option_menu(
                menu_title=None,
                options=['Đăng nhập', 'Đăng ký', 'Quên mật khẩu'],
                icons=["person-circle","people-fill","person-lines-fill"],
                menu_icon= "eye",
                default_index=0,
                orientation="horizontal",key="login_selection")
config = generate(names,usernames,hashed_passwords)
authenticator = stauth.Authenticate(config['credentials'],
                                    config['cookie']['name'],
                                    config['cookie']['key'],
                                    config['cookie']['expiry_days'],
                                    config['preauthorized'])

if security=="Đăng nhập":
    name, authentication_status, username = authenticator.login('Đăng nhập','main')

    if authentication_status:
        st.write('Welcome *%s*' % (name))
        st.title('Some content')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

    if st.session_state['authentication_status']:
        st.write('Welcome *%s*' % (st.session_state['name']))
        st.title('Some content')
    elif st.session_state['authentication_status'] == False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] == None:
        st.warning('Please enter your username and password')

elif security=='Đăng ký':
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)