# 1) pip install deta
from deta import Deta

# 2) initialize with a project key
deta = Deta("c0ftz0tu_yquSxJ21EWTHa6SeAkpkKDLajejNnUCz")

# 3) create and use as many DBs as you want!
MetaData = deta.Base("MetaData")
AddressInfo = deta.Base("AddressInfo")
#users.insert({
#    "name": "Geordi",
#    "title": "Chief Engineer"
#})
#
#fetch_res = users.fetch({"name": "Geordi"})
#
#for item in fetch_res.items:
#    users.delete(item["key"])