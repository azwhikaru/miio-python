import tools.utils_mi as xmutils 

def getRouterInfo(deviceId, cookie):
    apiUrl = xmutils.getApi(xmutils.getUserRegion()) + "/appgateway/third/miwifi/app/r/api/xqsystem/init_info"
    
    data = {
        "data": r'{"method":"POST","params":{"deviceId":"' + deviceId + '"}}'
    }

    return xmutils.sendPostRequest(apiUrl, data, cookie)