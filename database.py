from deta import Deta
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import os


try:
    load_dotenv(".env")
    DETA_KEY = os.getenv("DETA_KEY")
except:
    DETA_KEY = st.secrets["DETA_KEY"]
deta = Deta(DETA_KEY)

MetaData = deta.Base("MetaData")
AddressInfo = deta.Base("AddressInfo")
DataFiles = deta.Drive("DataFiles")


def _get_file(name):
    return DataFiles.get(name)

based_data = pd.read_csv(_get_file("Info.csv"))

def get_all_full_name():
    return based_data["Full_name"].values.tolist()

def get_address(family_code):
    return MetaData.fetch(query={"Family_code":family_code}).items
def uodate_db(table,keys,update_data):
    table.update(update_data,keys)
def calThienCan(BOY):
    thiencan = ["Canh","Tân","Nhâm","Quý","Giáp","Ất","Bính","Đinh","Mậu","Kỷ"]
    return thiencan[int(str(BOY)[-1])]
def calDiaChi(BOY):
    diachi=["Thân","Dậu","Tuất","Hợi","Tý","Sửu","Dẫn","Mão","Thìn","Tỵ","Ngọ","Mùi"]
    return diachi[BOY%12]

def get_info_person(query,include_address,include_family_code=False):
    data = MetaData.fetch(query=query)
    data = pd.DataFrame(data.items)
    check = data[(data["CanChi"].apply(lambda x: str(x)=="None"))&(data["BOY"].apply(lambda x: str(x)!="None"))][["key","BOY"]]
    if len(check.index.values)>0:
        d = check.values.tolist()
        for key,boy in d:
            update_data={
                "CanChi":calThienCan(int(boy)),
                "ConGiap": calDiaChi(int(boy))
            }
            uodate_db(MetaData,key,update_data)
        data = MetaData.fetch(query=query)
        data = pd.DataFrame(data.items)

    output_order = ["Họ và tên","Tuổi","Năm Sinh","Giới Tính"]
    new_data = data[["Full_name","Sex_code","BOY","CanChi","ConGiap"]].copy()
    new_data["Giới Tính"] = new_data["Sex_code"].apply(lambda x: "Nữ" if x==0 else "Nam")
    new_data["Năm Sinh"] = new_data["BOY"].apply(lambda x: int(x) if x!=None else None)
    new_data["Tuổi"] = new_data["CanChi"]+" "+new_data["ConGiap"]
    new_data["Họ và tên"] = new_data["Full_name"]
    if include_address:
        all_address = AddressInfo.fetch()
        all_address = pd.DataFrame(all_address.items)
        #print(all_address)
        new_data["Địa chỉ nhà"] = [all_address[all_address.Family_code==x]["Address"].values.tolist()[0] for x in data["Family_code"]]
        output_order+=["Địa chỉ nhà"]
    if include_family_code:
        new_data["Family_code"] = data["Family_code"]
        output_order+=["Family_code"]
    return new_data[output_order]
