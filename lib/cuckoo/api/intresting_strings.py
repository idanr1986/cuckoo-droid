import re

#E-mail


re_email = re.compile(r'([\w.-]+)@([\w.-]+)', re.I)

#URL
re_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I)

#IP
re_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', re.I)

#Package
re_package = re.compile(r'([a-z_]{1}[a-z0-9_]*(\.[a-z_]{1}[a-z0-9_]*)+)')

#File
re_file_filter = re.compile(r'.*\.(xml|java|resource|php|html|apk|dex|zip|png|jpg|json|csv|icon|mp3|jsp)$')


re_list = {"e-mail": re_email, "url": re_url, "ip": re_ip, "package": re_package}

def find_strings(strings):

    intresting_strings = {}
    intresting_strings["e-mail"] = []
    intresting_strings["url"] = []
    intresting_strings["ip"] = []
    intresting_strings["package"] = []
    intresting_strings["google_play_packages"] = []
    for string in strings:
        for regex in re_list:
            result = re_list[regex].findall(string)
            if result:
                if regex == "package":
                    for res in result:
                        package_string = res[0]
                        if not re_file_filter.findall(package_string):
                            if package_string not in intresting_strings[regex]:
                                intresting_strings[regex].append(package_string)

                elif regex == "e-mail":
                    if string not in intresting_strings[regex]:
                        intresting_strings[regex].append(string)
                else:
                    for res in result:
                        if string not in intresting_strings[regex]:
                            intresting_strings[regex].append(res)
    return intresting_strings



