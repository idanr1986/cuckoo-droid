import json
import logging
import os
from lib.cuckoo.common.abstracts import Processing
from lib.cuckoo.common.exceptions import CuckooProcessingError

log = logging.getLogger(__name__)


class Droidmon(Processing):
    """Extract Dynamic API calls Info From Droidmon logs."""

    def __init__(self):
        self.droidmon = {}

        self.droidmon["crypto_keys"] = []
        self.droidmon["reflection_calls"] = set()
        self.droidmon["SystemProperties"] = set()
        self.droidmon["started_activities"] = []
        self.droidmon["file_accessed"]=set()
        self.droidmon["fingerprint"]=set()
        self.droidmon["registered_receivers"]=set()
        self.droidmon["SharedPreferences"]=[]
        self.droidmon["ContentResolver_queries"]=set()
        self.droidmon["ContentValues"]=[]
        self.droidmon["encoded_base64"]=[]
        self.droidmon["decoded_base64"]=[]
        self.droidmon["commands"]=set()
        self.droidmon["ComponentEnabledSetting"]=[]
        self.droidmon["data_leak"]=set()
        self.droidmon["events"]=set()
        self.droidmon["crypto_data"]=[]
        self.droidmon["mac_data"]=[]
        self.droidmon["handleReceiver"]=[]
        self.droidmon["sms"]=[]
        self.droidmon["killed_process"]=[]
        self.droidmon["findResource"]=[]
        self.droidmon["findLibrary"]=[]
        self.droidmon["loadDex"]=set()
        self.droidmon["TelephonyManager_listen"]=set()
        self.droidmon["registerContentObserver"]=set()
        self.droidmon["accounts"]=set()
        self.droidmon["DexClassLoader"]=[]
        self.droidmon["DexFile"]=[]
        self.droidmon["PathClassLoader"]=[]
        self.droidmon["loadClass"]=set()
        self.droidmon["setMobileDataEnabled"]=set()
        self.droidmon["httpConnections"]=[]
        self.droidmon["error"]=[]
        self.droidmon["raw"]=[]

    def android_os_SystemProperties_get(self,api_call):
        self.droidmon["SystemProperties"].add(api_call["args"][0])

    def javax_crypto_spec_SecretKeySpec_javax_crypto_spec_SecretKeySpec(self,api_call):
        key = api_call["args"][0]
        exists=False
        for current_key in self.droidmon["crypto_keys"]:
            if key in current_key["key"]:
                exists=True
                break
        if not exists :
            new_key={}
            new_key["key"]=api_call["args"][0]
            new_key["type"]=api_call["args"][1]
            self.droidmon["crypto_keys"].append(new_key)

    def javax_crypto_Cipher_doFinal(self,api_call):
        if(api_call["this"]["mode"]== 1):
            self.droidmon["crypto_data"].append(api_call["args"][0])
        else:
            self.droidmon["crypto_data"].append(api_call["return"])

    def java_lang_reflect_Method_invoke(self,api_call):
        reflection=""
        if("hooked_class" in api_call ):
            reflection=api_call["hooked_class"]+"->"+api_call["hooked_method"]
        else:
            reflection=api_call["hooked_method"]
        self.droidmon["reflection_calls"].add(reflection)

    def dalvik_system_BaseDexClassLoader_findResource(self,api_call):
        self.lib_pairs(api_call,"findResource")

    def android_app_Activity_startActivity(self,api_call):
        self.droidmon["started_activities"].append(api_call["args"][0])

    def java_lang_Runtime_exec(self,api_call):
        command = api_call["args"][0]
        if type(command) is list:
            self.droidmon["commands"].add(' '.join(command))
        else:
            self.droidmon["commands"].add(command)

    def java_lang_ProcessBuilder_start(self,api_call):
        command = api_call["this"]["command"]
        self.droidmon["commands"].add(' '.join(command))

    def libcore_io_IoBridge_open(self,api_call):
        self.droidmon["file_accessed"].add(api_call["args"][0])

    def android_app_ActivityThread_handleReceiver(self,api_call):
        self.droidmon["handleReceiver"].append(api_call["args"][0])

    def android_app_ContextImpl_registerReceiver(self,api_call):
        for action in api_call["args"][1]["mActions"]:
            self.droidmon["registered_receivers"].add(action)

    def android_telephony_TelephonyManager_getDeviceId(self,api_call):
        self.droidmon["fingerprint"].add("getDeviceId")

    def android_telephony_TelephonyManager_getNetworkOperatorName(self,api_call):
        self.droidmon["fingerprint"].add("getNetworkOperatorName")

    def android_telephony_TelephonyManager_getSubscriberId(self,api_call):
        self.droidmon["fingerprint"].add("getSubscriberId")

    def android_telephony_TelephonyManager_getLine1Number(self,api_call):
        self.droidmon["fingerprint"].add("getLine1Number")

    def android_telephony_TelephonyManager_getNetworkOperator(self,api_call):
        self.droidmon["fingerprint"].add("getNetworkOperator")

    def android_telephony_TelephonyManager_getSimOperatorName(self,api_call):
        self.droidmon["fingerprint"].add("getSimOperatorName")

    def android_telephony_TelephonyManager_getSimCountryIso(self,api_call):
        self.droidmon["fingerprint"].add("getSimCountryIso")

    def android_telephony_TelephonyManager_getSimSerialNumber(self,api_call):
        self.droidmon["fingerprint"].add("getSimSerialNumber")

    def android_telephony_TelephonyManager_getNetworkCountryIso(self,api_call):
        self.droidmon["fingerprint"].add("getNetworkCountryIso")

    def android_telephony_TelephonyManager_getDeviceSoftwareVersion(self,api_call):
        self.droidmon["fingerprint"].add("getDeviceSoftwareVersion")

    def android_net_wifi_WifiInfo_getMacAddress(self,api_call):
        self.droidmon["fingerprint"].add("getMacAddress")

    def android_app_SharedPreferencesImpl_EditorImpl_putInt(self,api_call):
        self.droidmon["SharedPreferences"].append(self.get_pair(api_call))

    def android_app_SharedPreferencesImpl_EditorImpl_putString(self,api_call):
        self.droidmon["SharedPreferences"].append(self.get_pair(api_call))

    def android_app_SharedPreferencesImpl_EditorImpl_putFloat(self,api_call):
        self.droidmon["SharedPreferences"].append(self.get_pair(api_call))

    def android_app_SharedPreferencesImpl_EditorImpl_putBoolean(self,api_call):
        self.droidmon["SharedPreferences"].append(self.get_pair(api_call))

    def android_app_SharedPreferencesImpl_EditorImpl_putLong(self,api_call):
        self.droidmon["SharedPreferences"].append(self.get_pair(api_call))

    def android_content_ContentResolver_query(self,api_call):
        self.droidmon["ContentResolver_queries"].add(api_call["args"][0]["uriString"])

    def android_telephony_TelephonyManager_getSubscriberId(self,api_call):
        self.droidmon["fingerprint"].add("getSubscriberId")

    def android_content_ContentValues_put(self,api_call):
        self.droidmon["ContentValues"].append(self.get_pair(api_call))

    def android_telephony_TelephonyManager_getNetworkCountryIso(self,api_call):
        self.droidmon["fingerprint"].add("getNetworkCountryIso")

    def javax_crypto_Mac_doFinal(self,api_call):
        self.droidmon["mac_data"].append(api_call["args"][0])

    def android_util_Base64_encodeToString(self,api_call):
        self.droidmon["encoded_base64"].append(api_call["args"][0])

    def android_util_Base64_encode(self,api_call):
        self.droidmon["encoded_base64"].append(api_call["return"][0])

    def android_app_ApplicationPackageManager_setComponentEnabledSetting(self,api_call):
        new_pair={}
        component= api_call["args"][0]
        new_pair["component_name"]= component["mPackage"]+"/"+component["mClass"]
        new_state=api_call["args"][1]

        if (new_state in "2"):
            new_pair["component_new_state"] = "COMPONENT_ENABLED_STATE_DISABLED"
        elif (new_state in "1"):
            new_pair["component_new_state"] = "COMPONENT_ENABLED_STATE_ENABLED"
        elif (new_state in "0"):
            new_pair["component_new_state"] = "COMPONENT_ENABLED_STATE_DEFAULT"
        self.droidmon["ComponentEnabledSetting"].append(new_pair)

    def android_location_Location_getLatitude(self,api_call):
        self.droidmon["data_leak"].add("location")

    def android_location_Location_getLongitude(self,api_call):
        self.droidmon["data_leak"].add("location")

    def android_app_ApplicationPackageManager_getInstalledPackages(self,api_call):
        self.droidmon["data_leak"].add("getInstalledPackages")

    def dalvik_system_BaseDexClassLoader_findLibrary(self,api_call):
        self.lib_pairs(api_call,"findLibrary")

    def android_telephony_SmsManager_sendTextMessage(self,api_call):
        new_pair={}
        new_pair["dest_number"]=api_call["args"][0]
        new_pair["content"]=' '.join(api_call["args"][1])
        self.droidmon["sms"].append(new_pair)

    def android_util_Base64_decode(self,api_call):
        self.droidmon["decoded_base64"].append(api_call["return"])

    def android_telephony_TelephonyManager_listen(self,api_call):
        event =  api_call["args"][1];
        listen_enent=""
        if event==16:
            listen_enent="LISTEN_CELL_LOCATION"
        elif event==256:
            listen_enent="LISTEN_SIGNAL_STRENGTHS"
        elif event==32:
            listen_enent="LISTEN_CALL_STATE"
        elif event==64:
            listen_enent="LISTEN_DATA_CONNECTION_STATE"
        elif event==1:
            listen_enent="LISTEN_SERVICE_STATE"
        if "" not in listen_enent:
            self.droidmon["TelephonyManager_listen"].add(listen_enent)

    def android_content_ContentResolver_registerContentObserver(self,api_call):
        self.droidmon["registerContentObserver"].add(api_call["args"][0]["uriString"])

    def android_content_ContentResolver_insert(self,api_call):
        self.droidmon["ContentResolver_queries"].add(api_call["args"][0]["uriString"])

    def android_accounts_AccountManager_getAccountsByType(self,api_call):
        self.droidmon["accounts"].add(api_call["args"][0])
        self.droidmon["data_leak"].add("getAccounts")

    def dalvik_system_BaseDexClassLoader_findResources(self,api_call):
        self.lib_pairs(api_call,"findResource")

    def android_accounts_AccountManager_getAccounts(self,api_call):
       self.droidmon["data_leak"].add("getAccounts")

    def android_telephony_SmsManager_sendMultipartTextMessage(self,api_call):
        new_pair={}
        new_pair["dest_number"]=api_call["args"][0]
        new_pair["content"]=api_call["args"][2]
        self.droidmon["sms"].append(new_pair)

    def android_content_ContentResolver_delete(self,api_call):
        self.droidmon["ContentResolver_queries"].add(api_call["args"][0]["uriString"])

    def android_media_AudioRecord_startRecording(self,api_call):
        self.droidmon["events"].add("mediaRecorder")

    def android_media_MediaRecorder_start(self,api_call):
        self.droidmon["events"].add("mediaRecorder")

    def android_content_BroadcastReceiver_abortBroadcast(self,api_call):
        self.droidmon["events"].add("abortBroadcast")

    def dalvik_system_DexFile_loadDex(self,api_call):
        self.droidmon["loadDex"].add(api_call["args"][0])

    def dalvik_system_DexClass_dalvik_system_DexClassLoader(self,api_call):
       self.droidmon["DexClassLoader"].append(api_call["args"])

    def dalvik_system_DexFile_dalvik_system_DexFile(self,api_call):
       self.droidmon["DexFile"].append(api_call["args"])

    def dalvik_system_PathClassLoader_dalvik_system_PathClassLoader(self,api_call):
        self.droidmon["PathClassLoader"].append(api_call["args"])

    def android_app_ActivityManager_killBackgroundProcesses(self,api_call):
        self.droidmon["killed_process"].append(api_call["args"][0])

    def android_os_Process_killProcess(self,api_call):
        self.droidmon["killed_process"].append(api_call["args"][0])
    
    def android_net_ConnectivityManager_setMobileDataEnabled(self,api_call):
        self.droidmon["setMobileDataEnabled"].append(api_call["args"][0])

    def org_apache_http_impl_client_AbstractHttpClient_execute(self,api_call):
        json = {}
        if type(api_call["args"][0]) is dict:
            json["request"]=api_call["args"][1]
        else:
            json["request"]=api_call["args"][0]
        json["response"]=api_call["return"]
        self.droidmon["httpConnections"].append(json)

    def java_net_URL_openConnection(self,api_call):
        json = {}
        json["request"]=api_call["this"]
        json["response"]=api_call["return"]
        if("file:" in api_call["this"] or "jar:" in api_call["this"]):
            return
        self.droidmon["httpConnections"].append(json)

    def dalvik_system_DexFile_loadClass(self,api_call):
        self.droidmon["loadClass"].add(api_call["args"][0])

    def get_pair(self,api_call):
        new_pair={}
        new_pair["key"]=api_call["args"][0]
        if(api_call["args"].__len__()>1):
            new_pair["value"]=api_call["args"][1]
        return new_pair

    def lib_pairs(self,api_call,key):
        libname=api_call["args"][0]
        exists=False
        for current_key in self.droidmon[key]:
            if libname in current_key["libname"]:
                exists=True
                break
        if not exists :
            new_pair={}
            new_pair["libname"]=api_call["args"][0]
            if "return" in api_call:
                new_pair["result"]=api_call["return"]
            else:
                new_pair["result"]=""
            self.droidmon[key].append(new_pair)

    def keyCleaner(self,d):
        if type(d) is dict:
            for key, value in d.iteritems():
                d[key] = self.keyCleaner(value)
                if '.' in key:
                    d[key.replace('.', '_')] = value
                    del(d[key])
            return d
        if type(d) is list:
            return map(self.keyCleaner, d)
        if type(d) is tuple:
            return tuple(map(self.keyCleaner, d))
        return d

    def run(self):
        """Run extract of printable strings.
        @return: list of printable strings.
        """
        self.key = "droidmon"

        if ("file" not in self.task["category"]):
            return self.droidmon

        #if not("apk" in choose_package(File(self.task["target"]).get_type(),File(self.task["target"]).get_name())):
        #    return api_calls_map
        results={}

        log_path=self.logs_path+"/droidmon.log"
        if not os.path.exists(log_path):
            return results

        try :
            with open(log_path) as log_file:
                for line in log_file:
                    try:
                        api_call =json.loads(line)
                        self.droidmon["raw"].append(self.keyCleaner(api_call))
                        call = api_call["class"]+"_"+api_call["method"]
                        call = call.replace(".","_")
                        call = call.replace("$","_")
                        try:
                            func = getattr(self, call)
                            func(api_call)
                        except Exception as e:
                            self.droidmon["error"].append(e.message+" "+line)
                    except Exception as e:
                        log.error(CuckooProcessingError("error parsing json line: %s" % line + " error" +e.message))
        except Exception as e:
            raise CuckooProcessingError("Error opening file %s" % e)

        for key in self.droidmon.keys():
            if len(self.droidmon[key]) > 0:
                if type(self.droidmon[key]) is list:
                    results[key]=self.droidmon[key]
                else:
                    results[key]=list(self.droidmon[key])

        return results
