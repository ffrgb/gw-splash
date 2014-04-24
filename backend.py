from flask import Flask, request, jsonify, render_template
import json
import re

app = Flask(__name__)

def getMAC(ip):
    with open('/proc/net/arp') as arp:
        for line in arp:
            if re.search(ip, line):
                return line.split()[3]

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def main_site(path):
    mac = getMAC(request.remote_addr)
    token = False;
    print(request.url)
    if request.method == 'POST':
        token = True;
        print(mac)
    return render_template('toc.html', token = token)

if __name__ ==  "__main__":
    app.run(debug=True, host='0.0.0.0')
