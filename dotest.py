# -*- coding: UTF-8 -*-
import requests as req
import json,sys,time,random,os
from datetime import datetime
from datetime import timedelta
from datetime import timezone
#先注册azure应用,确保应用有以下权限:
#files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
#user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
#mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
#注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用

clientId = os.environ["CLIENTID"]
clientSecret = os.environ["CLIENTSECRET"]

path = sys.path[0] + r'/refreshtoken.txt'
num1 = 0

def gettoken(refresh_token):
    headers={'Content-Type':'application/x-www-form-urlencoded'
            }
    data={'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id':clientId,
          'client_secret':clientSecret,
          'redirect_uri':'https://localhost:44326/'
         }
    tokenInfo = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
    refresh_token = tokenInfo.json()['refresh_token']
    access_token = tokenInfo.json()['access_token']
    with open(path, 'w+') as f:
        f.write(refresh_token)
    return access_token

def get_time_now():
    SHA_TZ = timezone(timedelta(hours=8),name = 'Asia/Shanghai')
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    time_now = utc_now.astimezone(SHA_TZ)
    return time_now

def get_time_unix():
	return round(get_time_now().timestamp()*1000)

def main():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()
    global num1
    access_token = gettoken(refresh_token)
    headers = {
        'Authorization':access_token,
        'Content-Type':'application/json'
    }
    print('此次运行开始时间为 :', get_time_now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        if req.get(r'https://graph.microsoft.com/v1.0/me/drive/root',headers=headers).status_code == 200:
            num1+=1
            print("1调用成功"+str(num1)+'次')
            time.sleep(2)
        if req.get(r'https://graph.microsoft.com/v1.0/me/drive',headers=headers).status_code == 200:
            num1+=1
            print("2调用成功"+str(num1)+'次')
            time.sleep(2)
        if req.get(r'https://graph.microsoft.com/v1.0/drive/root',headers=headers).status_code == 200:
            num1+=1
            print('3调用成功'+str(num1)+'次')
            time.sleep(2)
        if req.get(r'https://graph.microsoft.com/v1.0/users ',headers=headers).status_code == 200:
            num1+=1
            print('4调用成功'+str(num1)+'次')
            time.sleep(2)
        if req.get(r'https://graph.microsoft.com/v1.0/me/messages',headers=headers).status_code == 200:
            num1+=1
            print('5调用成功'+str(num1)+'次') 
            time.sleep(2)   
        if req.get(r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',headers=headers).status_code == 200:
            num1+=1
            print('6调用成功'+str(num1)+'次')
            time.sleep(2)
        if req.get(r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',headers=headers).status_code == 200:
            num1+=1
            print('7调用成功'+str(num1)+'次')
        if req.get(r'https://graph.microsoft.com/v1.0/me/drive/root/children',headers=headers).status_code == 200:
            num1+=1
            print('8调用成功'+str(num1)+'次')
            time.sleep(2)
        if req.get(r'https://api.powerbi.com/v1.0/myorg/apps',headers=headers).status_code == 200:
            num1+=1
            print('8调用成功'+str(num1)+'次')
            time.sleep(2)
        if req.get(r'https://graph.microsoft.com/v1.0/me/mailFolders',headers=headers).status_code == 200:
            num1+=1
            print('9调用成功'+str(num1)+'次')
            time.sleep(2)
        if req.get(r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',headers=headers).status_code == 200:
            num1+=1
            print('10调用成功'+str(num1)+'次')
            time.sleep(2)
    except:
        print("pass")
        pass
for _ in range(random.randint(1,3)):
    main()
