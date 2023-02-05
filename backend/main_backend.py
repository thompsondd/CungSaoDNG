from .database import * #get_all_full_name
import time
import xlsxwriter
import numpy as np
from io import BytesIO
from dotenv import load_dotenv
import streamlit as st

sao=[   "Thái Âm", "Thái Dương", "Mộc Đức",
        "Thổ Tú", "Vân Hớn", "Thủy Diệu",
        "Kế Đô", "La Hầu", "Thái Bạch"
    ]

han=[   "Huỳnh Tiền","Tam Kheo","Ngũ Mộ",
        "Thiên Tinh","Tán Tận","Thiên La",
        "Địa Võng","Diêm Vương"
    ]

based_sao={ 1:[7,3,5,8,1,4,6,0,2],
            0:[6,4,2,0,3,7,1,8,5]
          }

based_han={ 1:[0,1,2,3,4,5,6,7],
            0:[4,3,2,1,0,7,6,5]
          }

decode_sao = {id:name for id,name in enumerate(sao)}
decode_han = {id:name for id,name in enumerate(han)}

def calSao(gioiTinh:int,tuoi:int):
    """
    gioiTinh:
        1 - Nam
        0 - Nu
    """
    if str(tuoi)=="nan": return None
    if tuoi<10 or tuoi>99: return None
    bs = based_sao[gioiTinh]
    return decode_sao[bs[int(tuoi)%len(bs)-1]]

def calHan(gioiTinh:int,tuoi:int):
    """
    gioiTinh:
        1 - Nam
        0 - Nu
    """
    if str(tuoi)=="nan": return None
    if tuoi<11 or tuoi>88: return None
    bs = based_han[gioiTinh]
    a = int(tuoi)//9
    b = int(tuoi)%9
    pos = b
    if a==b:
        pos = a-1
    elif b>a:
        pos = b-1
    return decode_han[bs[pos]]

def get_list_time(period=3):
    year_now = time.localtime().tm_year
    index = period
    return [year_now+i for i in range(-period,period+1)], index

def search_one_person(query,year_selected,include_address=False):
    output_order=["Họ và tên","Tuổi","Năm Sinh","Số Tuổi", "Giới Tính","Sao","Hạn"]
    dataframe = get_info_person(query,include_address)
    ages = (year_selected-dataframe["Năm Sinh"]+1).values.tolist()
    sex = dataframe["Giới Tính"].apply(lambda x: x=="Nam")
    dataframe["Sao"] = [calSao(sex[ind],ages[ind]) for ind in range(len(sex))]
    dataframe["Hạn"] = [calHan(sex[ind],ages[ind]) for ind in range(len(sex))]
    dataframe["Số Tuổi"] = ages
    if include_address:
        output_order+=["Địa chỉ nhà"]
    return dataframe[output_order]

def search_all_person(year_selected,include_address=False):
    output_order=["Họ và tên","Tuổi","Năm Sinh","Số Tuổi", "Giới Tính","Sao","Hạn"]
    dataframe = get_info_person(None,include_address)
    ages = (year_selected-dataframe["Năm Sinh"]+1).values.tolist()
    sex = dataframe["Giới Tính"].apply(lambda x: x=="Nam").values.tolist()
    dataframe["Sao"] = [calSao(sex[ind],ages[ind]) for ind in range(len(sex))]
    dataframe["Hạn"] = [calHan(sex[ind],ages[ind]) for ind in range(len(sex))]
    dataframe["Số Tuổi"] = ages
    dataframe["Năm Sinh"] =  dataframe["Năm Sinh"].apply(lambda x: str(int(x)) if str(x)!="nan" else None)
    dataframe["Số Tuổi"] =  dataframe["Số Tuổi"].apply(lambda x: str(int(x)) if str(x)!="nan" else None)
    dataframe.fillna("",inplace=True)
    if include_address:
        output_order+=["Địa chỉ nhà"]
    return dataframe[output_order]

def search_family(list_name,year_selected,include_address=False):
    odataframe = get_info_person(None,include_address,include_family_code=True)
    output_order=["Họ và tên","Tuổi","Năm Sinh","Số Tuổi", "Giới Tính","Sao","Hạn"]
    t = odataframe[odataframe["Họ và tên"].apply(lambda x: x in list_name)]["Family_code"].unique().tolist()
    output = {}
    if include_address:
        output_order+=["Địa chỉ nhà"]
    for i in t:
        dataframe=odataframe[odataframe["Family_code"]==i].reset_index(drop = True)
        ages = (year_selected-dataframe["Năm Sinh"]+1).values.tolist()
        #print(ages)
        sex = dataframe["Giới Tính"].apply(lambda x: x=="Nam").values.tolist()
        dataframe["Sao"] = [calSao(sex[ind],ages[ind]) for ind in range(len(sex))]
        dataframe["Hạn"] = [calHan(sex[ind],ages[ind]) for ind in range(len(sex))]
        dataframe["Số Tuổi"] = ages
        dataframe=dataframe.sort_values("Số Tuổi",ascending=False)
        dataframe["Năm Sinh"] =  dataframe["Năm Sinh"].apply(lambda x: str(int(x)) if str(x)!="nan" else None)
        dataframe.fillna("",inplace=True)
        
        key = dataframe[dataframe["Họ và tên"].apply(lambda x: x in list_name)].sort_values("Số Tuổi",ascending=False)["Họ và tên"].values[0]
        dataframe["Số Tuổi"] =  dataframe["Số Tuổi"].apply(lambda x: str(int(x)) if str(x)!="nan" else None)
        output.update({key:dataframe[output_order].copy()})
    return  output

def get_col_widths(tables):
    # First we find the maximum length of the index column
    import numpy as np
    #
    t = list(map(lambda x: len(x),tables[0].columns.values[:-1]))
    for table in tables:
        for index,i in enumerate(table.columns.values.tolist()[:-1]):
            t[index]=max(t[index],max(table[i].apply(lambda x:len(x)).values.tolist()))
    return t

def export_excel(data):
    output = BytesIO()
    data_excel = data
    workbook = xlsxwriter.Workbook(output,{'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.set_landscape()
    worksheet.center_vertically()
    worksheet.set_paper(9)

    keys = list(data_excel.keys())
    values = list(data_excel.values())
    cols = values[0].columns.values.tolist()

    bold = workbook.add_format({'bold': True,"border":True,'valign':"center"})
    bold.set_font_name('Times New Roman')
    bold.set_font_size(14)
    for col_index, col_name in enumerate(cols[:-1]):
        worksheet.write(f"{chr(65+col_index)}1",col_name,bold)
    
    border = workbook.add_format({"border":True,'valign':"center"})
    border.set_font_name('Times New Roman')
    border.set_font_size(14)

    merge_cell = workbook.add_format({'bold': True,'valign':"center","border":True})
    merge_cell.set_font_name('Times New Roman')
    merge_cell.set_font_size(13)

    new_start_row=1
    for table in values:
        address = table[cols[-1]]
        #new_start_row+=1
        c = 0
        for row, entity in enumerate(table[cols[:-1]].values):
            #print(f"row:{row+new_start_row}")
            for col, data in enumerate(entity):
                worksheet.write(row+new_start_row,col,data,border)
            c+=1
        new_start_row+=c
        #worksheet.merge_range(new_start_row,0,new_start_row,len(cols)-2,"")
        worksheet.merge_range(new_start_row,0,new_start_row,len(cols)-2,address.values[0],merge_cell)
        new_start_row+=1
        worksheet.merge_range(new_start_row,0,new_start_row,len(cols)-2,"")
        new_start_row+=1

    for i, width in enumerate(get_col_widths(values)):
        worksheet.set_column(i, i, width+7)
    workbook.close()
    return output

def send_email_otp(otp,reciver,name_reciver):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        load_dotenv(".env")
        gusername = os.getenv("gmail_username")
        gpassword = os.getenv("gmail_password")
        app_pass = os.getenv("gmail_app_pass")
    except:
        gusername = st.secrets["gmail_username"]
        gpassword = st.secrets["gmail_password"]
        app_pass = st.secrets["gmail_app_pass"]

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = gusername
    password = app_pass
    print(f"sender_email:{sender_email}")
    print(f"password:{app_pass}")
    receiver_email = reciver

    message = MIMEMultipart("alternative")
    message["Subject"] = "[DNG Tra Sao Hạn] Mã OTP xác thực"
    message["From"] = sender_email
    message["To"] = receiver_email
    # Create a secure SSL context
    context = ssl.create_default_context()
    html = """\
    <html>
    <body>
        <p>Xin chào,{name}
        Đây là mã OTP của bạn: <b>{OTP}</b><br>
        <a href="http://www.realpython.com">Real Python</a>
        has many great tutorials
        </p>
    </body>
    </html>
    """.format(OTP=otp, name=name_reciver)
    part2 = MIMEText(html, "html")
    message.attach(part2)
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        #server.quit() 
        return False
    finally:
        server.quit() 
        
