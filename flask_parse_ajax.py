import db
import multiprocessing
import mysocket
import os
from functools import wraps
from flask import make_response
from flask import request, jsonify, Flask, send_file, send_from_directory

app = Flask(__name__,static_url_path='',static_folder='./')
app.config['UPLOAD_FOLDER'] = os.environ['HOME']


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json(force=True)
    print(data)
    if not data:
        return 'No data received'
    with open('./piclibinfo', 'r') as f:
        info = f.readlines()
        info = [line[:-1] for line in info]
    if 'path' in data and data['path']:
        paths = data['path'].split()
    else:
        paths = info
    keyword = data['keyword']
    print('search in ', paths, ' for keyword: ', keyword)
    dbid = [info.index(lib[:-1] if lib[-1] == '/' else lib) for lib in paths]
    print('database id are ', dbid)
    picinfo = [urls.split() for urls in db.fuzzy_match(keyword, dbid)]
    response = {'data': [{'smallURL':urls[0], 'largeURL':urls[1], 'largePATH':urls[2]} for urls in picinfo]}
    print(response)
    return jsonify(response)

@app.route('/addlib', methods=['POST'])
def addlib():
    path = request.form.get('path') ######################### TODO ##########################
    dbid = 0
    print('adding index of files in %s...' % path)
    if os.path.exists('./piclibinfo'):
        with open('./piclibinfo', 'r') as f:
            liblist = [line[:-1] for line in f.readlines()]
            if path in liblist: return 'this lib had been added'
            dbid = len(liblist)
    addindex = multiprocessing.Process(target = mysocket.recvData, args = (dbid, 8888))
    addindex.start()
    try:
        os.system(os.getcwd() + '/communication_linux_amd64 ' + path + ' localhost:8888')
        addindex.join()
    except:
        addindex.terminate()
        return 'error'
    else:
        with open('./piclibinfo', 'a') as f:
            if path[-1] == '/': path = path[:-1]
            f.write(path + '\n')
    return 'ok'



@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


if __name__ == '__main__':
    dbserver = multiprocessing.Process(target = os.system, args = ('redis-server', ))
    dbserver.start()
    try:
        app.run()
        # app.run(host='0.0.0.0',port=80,debug=False)
    except:
        dbserver.terminate()
