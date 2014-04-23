from flask import Flask, request, jsonify, render_template
import json
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def main_site(path):
    print(path)
    token = False;
    print(request.url)
    if request.method == 'POST':
        token = True;
        print(request.remote_addr)
    return render_template('toc.html', token = token)

if __name__ ==  "__main__":
    app.run(debug=True, host='0.0.0.0')
