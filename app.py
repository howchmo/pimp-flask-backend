from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import psycopg2 as ps
import psycopg2.extras
import json
import uuid
from pimp_api import pimp_api
from pimp_card_api import pimp_card_api
import base64

app = Flask(__name__, static_folder='../pimp-webclient/www/', static_url_path='/pimp/')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1920 * 1080
app.config['UPLOAD_FOLDER'] = '../pimp-webclient/www/files/'
api = Api(app)

@app.route('/pimp/')
def root():
	return app.send_static_file('index.html')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pimp/upload', methods=['POST'])
def upload_image():
	data = request.json
	id = str(uuid.uuid4())
	filepath = app.config['UPLOAD_FOLDER']+id+data['extension']
	with open(filepath, 'wb') as f:
		f.write(base64.b64decode(data['blob']))
	data['path'] = "files/"+id+data['extension']
	return data

conn = ps.connect(
	host='localhost',
	database='pimp',
	user='pimp',
	password='pimp')

api.add_resource(pimp_api, '/pimp/pimp/', endpoint = 'cards', resource_class_kwargs = {'db_connection':conn})
api.add_resource(pimp_card_api, '/pimp/pimp/<string:id>', endpoint = 'card', resource_class_kwargs = {'db_connection':conn})

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", port=5000 )
