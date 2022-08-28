import requests
import hashlib

import tools.utils_mi as xmutils

########################################## PREDEFINED ##########################################
userAgent = "APP/com.xiaomi.mihome APPV/6.0.103 iosPassportSDK/3.9.0 iOS/14.4 miHSTS" # iOS APP
################################################################################################

def loginMiAccount(username, password):

    # 1
    url = "https://account.xiaomi.com/pass/serviceLogin?sid=xiaomiio&_json=true"
    headers = {
        "User-Agent": userAgent,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    cookies = {
        "userId": username
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    if(response.status_code != 200):
        return "Error (10000)"
    else:
        _sign = xmutils.ojsonToDict(response.text)["_sign"]
    
    # 2
    url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
    headers = {
        "User-Agent": userAgent,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    fields = {
        "sid": "xiaomiio",
        "hash": hashlib.md5(str.encode(password)).hexdigest().upper(),
        "callback": "https://sts.api.io.mi.com/sts",
        "qs": "%3Fsid%3Dxiaomiio%26_json%3Dtrue",
        "user": username,
        "_sign": _sign,
        "_json": "true"
    }
    response = requests.post(url, headers=headers, params=fields)
    if(response.status_code != 200):
        return "Error (10001)"
    else:
        jsonData = xmutils.ojsonToDict(response.text)
        location = jsonData["location"]
        ssecurity = jsonData["ssecurity"]
        userId = jsonData["userId"]
        cUserId = jsonData["cUserId"]
        passToken = jsonData["passToken"]
    
    # 3
    headers = {
        "User-Agent": userAgent,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(location, headers=headers)
    if response.status_code == 200:
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
    else:
        return "Error (10002)"

    cookies_dict["ssecurity"] = ssecurity
    cookies_dict["userId"] = userId
    cookies_dict["cUserId"] = cUserId
    cookies_dict["passToken"] = passToken

    return cookies_dict