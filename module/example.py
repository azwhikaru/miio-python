'''
This is just a sample to show how to build a controller module of your own;

The controller module should be placed in the 'modules' folder, then you can import it anywhere;

In the controller module, you can define any method like this to achieve your purpose:

Capture network packets sent/received by the 'Mi Home' application in the smartphone to find an Application Programming Interface;

Find out what data it sends/receives, cookies, and rewrite it into a method, it's that simple.

:-D
'''

import tools.utils_mi as xmutils

# JUST AN EXAMPLE ##############################################################

def getDeviceList(cookie):
    apiUrl = xmutils.getApi(xmutils.getUserRegion()) + "/home/device_list"
    data = {
        "data": '{"getVirtualModel":true,"getHuamiDevices":1,"get_split_device":false,"support_smart_home":true}'
    }
    return xmutils.sendPostRequest(apiUrl, data, cookie)

################################################################################