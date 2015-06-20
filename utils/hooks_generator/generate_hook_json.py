import json
from pprint import pprint

#with open("/Users/guardianangel/Desktop/test.json") as data_file:
#    data = json.load(data_file)
#pprint(data)

array = []
json_file = {}
def make(classname,method,obj,type):
    json = {}
    json["class_name"]=classname
    json["method"]=method
    json["thisObject"]=obj
    json["type"]=type
    array.append(json)

# fingerprint
make("android.telephony.TelephonyManager","getDeviceId",False,"fingerprint")
make("android.telephony.TelephonyManager","getSubscriberId",False,"fingerprint")
make("android.telephony.TelephonyManager","getLine1Number",False,"fingerprint")
make("android.telephony.TelephonyManager","getNetworkOperator",False,"fingerprint")
make("android.telephony.TelephonyManager","getNetworkOperatorName",False,"fingerprint")
make("android.telephony.TelephonyManager","getSimOperatorName",False,"fingerprint")
make("android.net.wifi.WifiInfo","getMacAddress",False,"fingerprint")
make("android.telephony.TelephonyManager","getSimCountryIso",False,"fingerprint")
make("android.telephony.TelephonyManager","getSimSerialNumber",False,"fingerprint")
make("android.telephony.TelephonyManager","getNetworkCountryIso",False,"fingerprint")
make("android.telephony.TelephonyManager","getDeviceSoftwareVersion",False,"fingerprint")
make("android.os.Debug","isDebuggerConnected",False,"fingerprint")

# globals
make("android.app.SharedPreferencesImpl$EditorImpl","putString",False,"globals")
make("android.app.SharedPreferencesImpl$EditorImpl","putBoolean",False,"globals")
make("android.app.SharedPreferencesImpl$EditorImpl","putInt",False,"globals")
make("android.app.SharedPreferencesImpl$EditorImpl","putLong",False,"globals")
make("android.app.SharedPreferencesImpl$EditorImpl","putFloat",False,"globals")
make("android.content.ContentValues","put",False,"globals")

# network
make("java.net.URL","openConnection",True,"network")
make("org.apache.http.impl.client.AbstractHttpClient","execute",False,"network")

# binder
make("android.app.ContextImpl","registerReceiver",False,"binder")
make("android.app.ActivityThread","handleReceiver",False,"binder")
make("android.app.Activity","startActivity",False,"binder")

# dex
make("dalvik.system.BaseDexClassLoader","findResource",False,"dex")
make("dalvik.system.BaseDexClassLoader","findLibrary",False,"dex")
make("dalvik.system.DexFile","loadDex",False,"dex")
make("dalvik.system.DexClassLoader",None,False,"dex")
make("dalvik.system.BaseDexClassLoader","findResources",False,"dex")
make("dalvik.system.DexFile","loadClass",False,"dex")
make("dalvik.system.DexFile",None,False,"dex")
make("dalvik.system.PathClassLoader",None,False,"dex")

# reflection
make("java.lang.reflect.Method","invoke",False,"reflection")

# crypto
make("javax.crypto.spec.SecretKeySpec",None,False,"crypto")
make("javax.crypto.Cipher","doFinal",True,"crypto")
make("javax.crypto.Mac","doFinal",False,"crypto")

# generic
make("android.app.ApplicationPackageManager","setComponentEnabledSetting",False,"generic")
make("android.app.NotificationManager","notify",False,"generic")
make("android.util.Base64","decode",False,"generic")
make("android.telephony.TelephonyManager","listen",False,"generic")
make("android.util.Base64","encode",False,"generic")
make("android.util.Base64","encodeToString",False,"generic")
make("android.net.ConnectivityManager","setMobileDataEnabled",False,"generic")
make("android.content.BroadcastReceiver","abortBroadcast",False,"generic")

# sms
make("android.telephony.SmsManager","sendTextMessage",False,"sms")
make("android.telephony.SmsManager","sendMultipartTextMessage",False,"sms")

# runtime
make("java.lang.Runtime","exec",False,"runtime")
make("java.lang.ProcessBuilder","start",True,"runtime")
make("java.io.FileOutputStream","write",False,"runtime")
make("java.io.FileInputStream","read",False,"runtime")
make("android.app.ActivityManager","killBackgroundProcesses",False,"runtime")
make("android.os.Process","killProcess",False,"runtime")


# content
make("android.content.ContentResolver","query",False,"content")
make("android.content.ContentResolver","registerContentObserver",False,"content")
make("android.content.ContentResolver","insert",False,"content")
make("android.accounts.AccountManager","getAccountsByType",False,"content")
make("android.accounts.AccountManager","getAccounts",False,"content")
make("android.location.Location","getLatitude",False,"content")
make("android.location.Location","getLongitude",False,"content")
make("android.content.ContentResolver","delete",False,"content")
make("android.media.AudioRecord","startRecording",False,"content")
make("android.media.MediaRecorder","start",False,"content")
make("android.os.SystemProperties","get",False,"content")
make("android.app.ApplicationPackageManager","getInstalledPackages",False,"content")

# file
make("libcore.io.IoBridge","open",False,"file")





json_file["hookConfigs"]=array
json_file["trace"]=False
with open('hooks.json', 'w') as outfile:
    json.dump(json_file, outfile ,sort_keys = True, indent = 4,ensure_ascii=False)