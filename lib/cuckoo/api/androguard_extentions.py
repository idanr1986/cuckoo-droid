from androguard.core.analysis.analysis import PathVar, TAINTED_PACKAGE_CALL
from androguard.core.bytecodes.dvm_permissions import DVM_PERMISSIONS


def get_methods(vmx):
    methods = []
    for i in vmx.get_methods():
        method = {}
        i.create_tags()
        if not i.tags.empty():
            proto = i.method.proto.replace("(", "").replace(";", "")
            protos = proto.split(")")
            params = protos[0].split(" ")
            method["class"] = i.method.get_class_name().replace(";", "")
            method["name"] = i.method.name
            if params and params[0]:
                method["params"] = params
            method["return"] = protos[1]
            methods.append(method)
    return methods

def get_permissions(apk):
    """
        Return permissions with details

        :rtype: list of string
    """
    permission_list = []

    for i in apk.get_permissions() :
        perm = i
        pos = i.rfind(".")

        if pos != -1 :
            perm = i[pos+1:]

        a={}

        try :
            temp = DVM_PERMISSIONS["MANIFEST_PERMISSION"][ perm ]
            a["name"]=i
            a["severity"]=temp[0]
            a["action"]=temp[1]
            a["description"]=temp[2]

        except KeyError :
            a["name"]=i
            a["severity"]="dangerous"
            a["action"]="Unknown permission from android reference"
            a["description"]="Unknown permission from android reference"

        permission_list.append(a)

    return permission_list

def get_extended_receivers(apk):
    """
    Return the android:name attribute of all receivers

    :rtype: a list of string
    """
    manifest =apk.get_AndroidManifest().getElementsByTagName("manifest")[0]
    receivers = []
    application = manifest.getElementsByTagName("application")[0]
    for receiver in application.getElementsByTagName("receiver"):
        intents = receiver.getElementsByTagName("intent-filter")
        for intent in intents:
            actions = intent.getElementsByTagName("action")
            for action in actions:
                receivers.append(action.attributes["android:name"].value)

    return receivers

def get_show_Permissions(dx):
    p = dx.get_permissions( [] )
    permissions = {}
    for i in p :
        paths=[]
        #print i, ":"
        for j in p[i] :
           paths.append(get_show_Path(dx.get_vm(), j))
        permissions[i.replace("android.permission.", "").replace(".", "_")] = paths
    return permissions

def get_show_Path(vm, path) :
  cm = vm.get_class_manager()

  if isinstance(path, PathVar) :
    dst_class_name, dst_method_name, dst_descriptor =  path.get_dst( cm )
    info_var = path.get_var_info()
    return "%s %s (0x%x) ---> %s->%s%s" % (path.get_access_flag(),
                                          info_var,
                                          path.get_idx(),
                                          dst_class_name,
                                          dst_method_name,
                                          dst_descriptor)
  else :
    if path.get_access_flag() == TAINTED_PACKAGE_CALL :
      src_class_name, src_method_name, src_descriptor =  path.get_src( cm )
      dst_class_name, dst_method_name, dst_descriptor =  path.get_dst( cm )

      return "%d %s->%s%s (0x%x) ---> %s->%s%s" % (path.get_access_flag(),
                                                  src_class_name,
                                                  src_method_name,
                                                  src_descriptor,
                                                  path.get_idx(),
                                                  dst_class_name,
                                                  dst_method_name,
                                                  dst_descriptor)
    else :
      src_class_name, src_method_name, src_descriptor =  path.get_src( cm )
      return "%d %s->%s%s (0x%x)" % (path.get_access_flag(),
                                    src_class_name,
                                    src_method_name,
                                    src_descriptor,
                                    path.get_idx() )

def get_show_DynCode(dx) :
    """
        Show where dynamic code is used
        :param dx : the analysis virtual machine
        :type dx: a :class:`VMAnalysis` object
    """
    paths = dx.get_tainted_packages().search_methods( "Ldalvik/system/DexClassLoader;", ".", ".")
    return get_show_Paths( dx.get_vm(), paths )

def get_show_NativeMethods(dx) :
    """
        Show the native methods
        :param dx : the analysis virtual machine
        :type dx: a :class:`VMAnalysis` object
    """
    native=[]
    d = dx.get_vm()
    for i in d.get_methods() :
        if i.get_access_flags() & 0x100 :
            native.append( i.get_class_name()+ i.get_name()+ i.get_descriptor())
            #native.append(get_show_Path(d,i))
    return native

def get_show_ReflectionCode(dx) :
    """
        Show the reflection code
        :param dx : the analysis virtual machine
        :type dx: a :class:`VMAnalysis` object
    """
    paths = dx.get_tainted_packages().search_methods( "Ljava/lang/reflect/Method;", ".", ".")
    return get_show_Paths( dx.get_vm(), paths )

def get_show_CryptoCode(dx) :
    """
        Show the reflection code
        :param dx : the analysis virtual machine
        :type dx: a :class:`VMAnalysis` object
    """
    paths = dx.get_tainted_packages().search_methods( "Ljavax/crypto/.", ".", ".")
    return get_show_Paths( dx.get_vm(), paths )

def get_show_Paths(vm, paths) :
    """
        Show paths of packages
        :param paths: a list of :class:`PathP` objects
    """
    list =[]
    for path in paths :
        list.append(get_show_Path( vm, path ))
    return list
