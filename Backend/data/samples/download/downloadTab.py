import glob, os, re, urllib2
from subprocess import call

for root, dirs, files in os.walk("tabs.ultimate-guitar.com"):
    for filePath in files:
        if filePath.endswith(".htm"):
            with open(os.path.join(root, filePath)) as htmlFile:
                html = htmlFile.read()
                id = re.findall("<input type='hidden' name='id' value='([0-9]*)' id=\"tab_id\">", html, re.MULTILINE)[0]
                session_id = re.findall("<input type='hidden' name='session_id' value='(.*)'>", html, re.MULTILINE)[0]
                #https://tabs.ultimate-guitar.com/tabs/download?id=1075776&session_id=db94fdb48da60323ad6c10b63c8a1c73
                url = 'https://tabs.ultimate-guitar.com/tabs/download?id='+id+'&session_id='+session_id
                call(["curl", "-o", "download/" + filePath ,  url])