# cuckoo-droid
CuckooDroid - Automated Android Malware Analysis with Cuckoo Sandbox.

Installation - easy integration script::
    git clone --depth=1 https://github.com/cuckoobox/cuckoo.git cuckoo
    cd cuckoo
    git remote add droid https://github.com/idanr1986/cuckoo-droid
    git pull --no-edit -s recursive -X theirs droid master 
    cat conf-extra/processing.conf >> conf/processing.conf
    cat conf-extra/reporting.conf >> conf/reporting.conf
    rm -r conf-extra
    echo "protobuf" >> requirements.txt