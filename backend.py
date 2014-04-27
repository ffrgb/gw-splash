from flask import Flask, request, jsonify, render_template, abort
import subprocess
import re
import db as database
from iptables import IPTables
from helper import Helper

app = Flask(__name__)

# create objects needed here
ipt = IPTables()
helper = Helper()
db = database.DB()

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def main_site(path):
    # set signal tokens for the webinterface
    token = False;
    iptoken = False
    dbtoken = False

    # try to get MAC (doesn't work on localhost connection)
    mac = helper.getMAC(request.remote_addr)
    # and send an 400 error if there is no client mac in arp table (like for localhost)
    if not mac:
        abort(400)
    # this is the code which runs if the client accepts the tos
    if request.method == 'POST':
        token = True
        try:
            if db.checkRecordExists(mac):
                db.addMAC(mac);
                if not ipt.unlockMAC(mac):
                    iptoken = True
                    token = False
            else:
                token = False
                dbtoken = True
        except:
            print("An unexpected error occurred!!! Please handle with it!")
            raise

    return render_template('toc.html', token = token, iptoken = iptoken, dbtoken = dbtoken)

if __name__ ==  "__main__":
    ipt.start()
    app.run(debug=True, host='0.0.0.0')
    ipt.shutdown()
