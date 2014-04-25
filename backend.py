from flask import Flask, request, jsonify, render_template, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
import subprocess
import sqlalchemy.exc
import time
import json
import re
import db

app = Flask(__name__)

Session = sessionmaker(bind=db.engine)
session = Session()

def getMAC(ip):
    with open('/proc/net/arp') as arp:
        for line in arp:
            if re.search(ip, line):
                return line.split()[3]

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def main_site(path):
    mac = getMAC(request.remote_addr)
    if not mac:
        abort(400)
    token = False;
    iptoken = False
    dbtoken = False
    if request.method == 'POST':
        token = True
        try:
            if (session.query(db.Clients).filter(db.Clients.mac == mac).first() == None):
                session.add(db.Clients(mac = mac, time = time.time()))
                session.commit()
                if subprocess.call(['iptables', '-t', 'mangle', '-I', 'internet', '-m', 'mac', '--mac-source', mac, '-j','RETURN']) == 3:
                    iptoken = True
                    token = False
            else:
                token = False
                dbtoken = True
        except:
            raise

    return render_template('toc.html', token = token, iptoken = iptoken, dbtoken = dbtoken)

if __name__ ==  "__main__":
    app.run(debug=True, host='0.0.0.0')
