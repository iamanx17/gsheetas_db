import json 
import requests

url="https://credsapi.herokuapp.com/credsapi/?search=gsheetas_db"

headers={ "Authorization" : "Token 700468c84e4e14acbc47a1a277b66cc653f430bb" }

r=requests.get(url=url,headers=headers)

data=r.json()

for i in data:
    secret_key=i['secret_key']
    host=i['database_host']
    user=i['database_user']
    password=i['database_password']
    name=i['database_name']

