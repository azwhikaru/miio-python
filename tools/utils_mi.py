import json
import time
import requests
import ast
import os

import tools.rc4_mi as xmcreypt

def getUserRegion():
    fileName = os.path.dirname(os.path.dirname(__file__)) + "/config.txt"

    if(os.path.isfile(fileName) == False):
        print("config.txt is not exist.")
        exit()
    configFile = open(fileName)
    configDict = ast.literal_eval(configFile.read())
    userRegion = configDict["region"]
    return userRegion

def getApi(region):
    return "https://" + ("" if region == "cn" else (region + ".")) + "api.io.mi.com/app"

def ojsonToDict(str):
    return json.loads(str.replace("&&&START&&&", ""))

def sendPostRequest(url, data, cookie):
    headers = {
        "Accept-Encoding": "identity",
        "User-Agent": "APP/com.xiaomi.mihome APPV/6.0.103 iosPassportSDK/3.9.0 iOS/14.4 miHSTS", # iOS APP
        "Content-Type": "application/x-www-form-urlencoded",
        "x-xiaomi-protocal-flag-cli": "PROTOCAL-HTTP2",
        "MIOT-ENCRYPT-ALGORITHM": "ENCRYPT-RC4",
    }
    reCookies = {
        # "cUserId": str(cookie["cUserId"]),
        "userId": str(cookie["userId"]),
        "yetAnotherServiceToken": str(cookie["serviceToken"]),
        "serviceToken": str(cookie["serviceToken"]),
        "locale": "zh_CN",
        "timezone": "GMT+08:00",
        "is_daylight": "1",
        "dst_offset": "3600000",
        "channel": "MI_APP_STORE"
    }
    millis = round(time.time() * 1000)
    ssecurity = cookie["ssecurity"]
    nonce = xmcreypt.mkNonce(millis)
    signed_nonce = xmcreypt.mkSignedNonce(nonce, ssecurity)
    encData = xmcreypt.mkEncData(url, "POST", signed_nonce, nonce, ssecurity, data)

    reqData = requests.post(url, params=encData, headers=headers, cookies=reCookies)

    if(reqData.status_code != 200):
        print("Error (" + reqData.text + ")")
        return ""
    else:
        reqDataText = xmcreypt.uncryptText(nonce, ssecurity, reqData.text)
        return ojsonToDict(reqDataText)