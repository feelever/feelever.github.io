import requests
headers={}
#headers["Authorization"]="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdGltZSI6MTU2Mzc4NzAwMTU3MCwiZXhwIjoxNTYzNzk0MjAxNTcwLCJqdGkiOiIzNmJhMTY4Y2NkMjA0NzM1YjE3ZjUxMzEzNGNlMjgyYSIsIm5hbWUiOiJwYW54aWFvcWluMSIsInBhcmVudElkIjowLCJyZWdpb24iOiJuZmpkIiwic3ViIjoiSlB1c2giLCJ0aW1lcyI6MSwidWlkIjoyNzM1Mzd9.nrBP0HyAwnPHkH4qrzjnkQlOk9CnnN59ntJbkbyIXcE"
url="https://bj-api.srv.jpush.cn/v1/sms/apps/3fcf3400b3a6869a4683a76b/sending/list?etime=201907222359&pageIndex=1&pageSize=10&stime=201907150000"
r= requests.get(url,headers=headers)
print(r.text)