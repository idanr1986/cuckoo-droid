# Copyright (C) Check Point Software Technologies LTD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.
import base64
import hashlib
import os
import logging
from zipfile import BadZipfile, ZipFile
import zipfile
from lib.cuckoo.api.DexDumper.DexDumper import string_dumper
from lib.cuckoo.api.androguard_extentions import get_show_NativeMethods, get_show_CryptoCode, get_show_Permissions, \
    get_show_ReflectionCode, get_show_DynCode, get_methods, get_extended_receivers, get_permissions
from lib.cuckoo.api.certificate import get_certificate
from lib.cuckoo.api.intresting_strings import find_strings

try:
    from androguard.core.bytecodes.apk import APK
    from androguard.core.bytecodes.dvm import DalvikVMFormat
    from androguard.core.analysis.analysis import Analysis
    from androguard.core.analysis import analysis
    HAVE_ANDROGUARD = True
except ImportError:
    HAVE_ANDROGUARD = False

from lib.cuckoo.common.objects import File
from lib.cuckoo.common.abstracts import Processing
from lib.cuckoo.common.exceptions import CuckooProcessingError

def get_apk_icon(filepath):
    zfile = zipfile.ZipFile(filepath)
    for finfo in zfile.infolist():
        if "ic_launcher.png" in finfo.filename or "icon.png" in finfo.filename:
            ifile = zfile.open(finfo).read()
            return base64.encodestring(ifile)

    return None

log = logging.getLogger(__name__)


class ApkInfo(Processing):
    """Static android information about analysis session."""


    def __init__(self):
        self.key = "apkinfo"

        self.files_name_map={}
        self.files_name_map["apk"] = []
        self.files_name_map["jar"] = []
        self.files_name_map["so"] = []
        self.files_name_map["ko"] = []
        self.files_name_map["dex"] = []
        self.files_name_map["exe"] = []
        self.files_name_map["arm_exe"] = []

    def file_type_check(self, file):
        name = file["name"]
        fileName, fileExtension = os.path.splitext(name)
        type = file["type"]

        if "Java Jar" in type:
            self.files_name_map["jar"].append(file)
            if "apk" not in fileExtension and "jar" not in fileExtension:
                return True
        elif "Android" in type:
            self.files_name_map["apk"].append(file)
            if "apk" not in fileExtension and "jar" not in fileExtension:
                return True
        elif "shared object, ARM" in type:
            self.files_name_map["so"].append(file)
            if "so" not in fileExtension and "art" not in fileExtension:
                return True
        elif "executable, ARM" in type:
            self.files_name_map["arm_exe"].append(file)
            if "" != fileExtension:
                return True
        elif "relocatable, ARM" in type:
            self.files_name_map["ko"].append(file)
            if "ko" not in fileExtension:
                return True
        elif "Dalvik" in type:
            if file["name"] != "classes.dex":
                self.files_name_map["dex"].append(file)
            if "dex" not in fileExtension:
                return True
        elif "8086" in type or "PE32" in type:
            self.files_name_map["exe"].append(file)
            if "exe" not in fileExtension:
                return True
        else:
            if ".apk" == fileExtension:
                self.files_name_map["apk"].append(file)
            elif ".jar" == fileExtension:
                self.files_name_map["jar"].append(file)
            elif ".so" == fileExtension:
                self.files_name_map["so"].append(file)
            elif ".ko" == fileExtension:
                self.files_name_map["ko"].append(file)
            elif ".exe" == fileExtension:
                self.files_name_map["exe"].append(file)
            elif ".dex" == fileExtension:
                if file["name"] != "classes.dex":
                    self.files_name_map["dex"].append(file)

        return False

    def check_size(self, file_list):
        for file in file_list:
            if "classes.dex" in file["name"]:
                if("decompilation_threshold" in self.options):
                    if file["size"] < self.options.decompilation_threshold:
                        return True
                    else:
                        log.warning("Dex size bigger than decompilation_threshold " + str(file["size"]) + " > " + str(self.options.decompilation_threshold))
                        return False
                else:
                    log.warning("decompilation_threshold not defined, decompiling")
                    return True
        return False

    def _apk_files(self, apk):
        """Returns a list of files in the APK."""
        ret = []
        for fname, filetype in apk.get_files_types().items():
            buf = apk.zip.read(fname)
            ret.append({
                "name": fname,
                "md5": hashlib.md5(buf).hexdigest(),
                "size": len(buf),
                "type": filetype,
            })
        return ret

    def _get_strings(self, apk_path):
        list_string = []
        for string in string_dumper(apk_path):
            try:
                list_string.append(str.decode(string, "utf-8"))
            except:
                pass

        return list_string

    def run(self):
        """Run androguard to extract static android information
                @return: list of static features
        """
        self.key = "apkinfo"
        apkinfo = {}

        if "file" not in self.task["category"] or not HAVE_ANDROGUARD:
            return

        f = File(self.task["target"])
        #if f.get_name().endswith((".zip", ".apk")) or "zip" in f.get_type():
        if not os.path.exists(self.file_path):
            raise CuckooProcessingError("Sample file doesn't exist: \"%s\"" % self.file_path)

        try:
            a = APK(self.file_path)
            if a.is_valid_APK():
                manifest = {}

                apkinfo["files"] = self._apk_files(a)
                manifest["package"] = a.get_package()
                apkinfo["hidden_payload"] = []

                for file in apkinfo["files"]:
                    if self.file_type_check(file):
                       apkinfo["hidden_payload"].append(file)

                apkinfo["files_flaged"] = self.files_name_map

                manifest["permissions"]= get_permissions(a)
                manifest["main_activity"] = a.get_main_activity()
                manifest["activities"] = a.get_activities()
                manifest["services"] = a.get_services()
                manifest["receivers"] = a.get_receivers()
                manifest["receivers_actions"] = get_extended_receivers(a)
                manifest["providers"] = a.get_providers()
                manifest["libraries"] = list(a.get_libraries())
                apkinfo["manifest"] = manifest

                apkinfo["icon"] = get_apk_icon(self.file_path)
                certificate = get_certificate(self.file_path)
                if certificate:
                    apkinfo["certificate"] = certificate


                #vm = DalvikVMFormat(a.get_dex())
                #strings = vm.get_strings()
                strings = self._get_strings(self.file_path)
                apkinfo["interesting_strings"] = find_strings(strings)
                apkinfo["dex_strings"] = strings

                static_calls = {}
                if self.options.decompilation:
                    if self.check_size(apkinfo["files"]):
                        vm = DalvikVMFormat(a.get_dex())
                        vmx = Analysis(vm)
                        vmx.create_xref()

                        static_calls["all_methods"] = get_methods(vmx)
                        static_calls["permissions_method_calls"] = get_show_Permissions(vmx)

                        static_calls["native_method_calls"] = get_show_NativeMethods(vmx)
                        static_calls["is_native_code"] = bool(static_calls["native_method_calls"]) # True if not empty, False if empty

                        static_calls["dynamic_method_calls"] = get_show_DynCode(vmx)
                        static_calls["is_dynamic_code"] = bool(static_calls["dynamic_method_calls"])

                        static_calls["reflection_method_calls"] = get_show_ReflectionCode(vmx)
                        static_calls["is_reflection_code"] = bool(static_calls["reflection_method_calls"])

                        static_calls["crypto_method_calls"] = get_show_CryptoCode(vmx)
                        static_calls["is_crypto_code"] = bool(static_calls["crypto_method_calls"])



                        classes = list()
                        for cls in vm.get_classes():
                            classes.append(cls.name)

                        static_calls["classes"] = classes

                    else:
                        log.warning("Aborted decompilation, static extraction of calls not perforemd",)

                apkinfo["static_method_calls"] = static_calls

        except (IOError, OSError, BadZipfile) as e:
            raise CuckooProcessingError("Error opening file %s" % e)
        return apkinfo

