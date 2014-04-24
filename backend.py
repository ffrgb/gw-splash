from flask import Flask, request, jsonify, render_template, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
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
    if request.method == 'POST':
        session.add(mac = mac, time = time.time())
        session.commit()
        token = True;
    return render_template('toc.html', token = token)

if __name__ ==  "__main__":
    app.run(debug=True, host='0.0.0.0')
