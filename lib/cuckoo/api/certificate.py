import logging
import os
from zipfile import ZipFile

log = logging.getLogger(__name__)


def get_certificate_filename(apk_path):
    with ZipFile(apk_path, 'r') as f:
        for name in f.namelist():
            if ".RSA" in name:
                return name
        return None


def get_certificate_info(apk_path, filename):
        cmd = "unzip -p " + apk_path + " " + filename + " |openssl pkcs7 -inform DER -noout -print_certs -text"
        try:
            return os.popen(cmd).read()
        except Exception as e:
            log.debug(e.message())
            return None


def get_certificate_info_flag(apk_path, filename, flag):
        cmd = "unzip -p " + apk_path + " " + filename + " |openssl pkcs7 -inform DER -print_certs |openssl x509 -noout -" + flag
        try:
            return os.popen(cmd).read()
        except Exception as e:
            log.debug(e.message())
            return None


def get_certificate_issuer(apk_path, filename):
    issuers_return = {}
    issuers = get_certificate_info_flag(apk_path, filename, "issuer").replace("issuer= /", "").split("/")
    for issuer in issuers:
        issuer_split = issuer.split("=")
        issuers_return[issuer_split[0]] = issuer_split[1].strip()
    return issuers_return


def get_certificate(apk_path):
    filename = get_certificate_filename(apk_path)
    if filename:
        certificate_info = {}
        certificate_info["text"] = get_certificate_info(apk_path, filename)
        certificate_info["fingerprint"] = get_certificate_info_flag(apk_path, filename, "fingerprint").split('=')[1].replace(':','').strip()
        certificate_info["issuer"] = get_certificate_issuer(apk_path, filename)
        return certificate_info
    else:
        log.debug("no Certificate Found!")
        return None
