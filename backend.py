sao=[   "Thái Âm", "Thái Dương", "Mộc Đức",
        "Thổ Tú", "Vân Hớn", "Thủy Diệu",
        "Kế Đô", "La Hầu", "Thái Bạch"
    ]

han=[   "Huỳnh Tiền","Tam Kheo","Ngũ Mộ",
        "Thiên Tinh","Tán Tận","Thiên La",
        "Địa Võng","Diêm Vương"
    ]

based_sao={ 0:[7,3,5,8,1,4,6,0,2],
            1:[6,4,2,0,3,7,1,8,5]
          }

based_han={ 0:[0,1,2,3,4,5,6,7],
            1:[4,3,2,1,0,7,6,5]
          }

decode_sao = {id:name for id,name in enumerate(sao)}
decode_han = {id:name for id,name in enumerate(han)}

def calSao(gioiTinh:int,tuoi:int):
    """
    gioiTinh:
        0 - Nam
        1 - Nu
    """
    bs = based_sao[gioiTinh]
    return decode_sao[bs[tuoi%len(bs)-1]]

def calHan(gioiTinh:int,tuoi:int):
    """
    gioiTinh:
        0 - Nam
        1 - Nu
    """
    bs = based_han[gioiTinh]
    a = tuoi//9
    b = tuoi%9
    pos = b
    if a==b:
        pos = a-1
    elif b>a:
        pos = b-1
    return decode_han[bs[pos]]