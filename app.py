from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import psycopg2 as ps
import psycopg2.extras
import json
import uuid

import pimp_api

app = Flask(__name__, static_folder='../pimp-webclient/www', static_url_path='')
api = Api(app)

conn = ps.connect(
	host='localhost',
	database='pimp',
	user='pimp',
	password='pimp')

class pimp_api( Resource ):
	def __init__(self, db_connection):
		self.conn = db_connection

	def get(self):
		sql = """SELECT _id, title, born, doc from cards;"""
		c = conn.cursor(cursor_factory=ps.extras.RealDictCursor)
		try:
			c.execute(sql)
			c.close()
			return jsonify(c.fetchall())
		except (Exception, ps.DatabaseError) as error:
			return jsonify(error)

	def post(self):
		j = json.loads(request.form['string'])
		if not j or not 'title' in j:
			abort(400)
		sql = """INSERT INTO cards(_id, title, born, doc) VALUES (%s, %s, %s, %s);"""
		c = conn.cursor() # cursor_factory=ps.extras.RealDictCursor)
		id = str(uuid.uuid4())
		print(id)
		seq = []
		seq.append(id)
		seq.append(j['title'])
		seq.append(j['born'])
		seq.append(json.dumps(j['doc']))
		try:
			c.execute(sql, seq)
			conn.commit()
			c.close()
			return id, 201
		except (Exception, ps.DatabaseError) as error:
			print("ERROR: "+str(error))

class pimp_card_api( Resource ):
	def __init__(self, db_connection):
		self.conn = db_connection

	def get(self, id):
		sql = "SELECT _id, title, born, doc FROM cards WHERE _id = '"+id+"';"
		c = conn.cursor(cursor_factory=ps.extras.RealDictCursor)
		try:
			c.execute(sql)
			r = jsonify(c.fetchone())
			c.close()
			return r
		except (Exception, ps.DatabaseError) as error:
			print("ERROR: "+str(error))

	def put(self, id):
		sql = """UPDATE cards SET title=%s, doc=%s WHERE _id = %s"""
		c = conn.cursor()
		j = json.loads(request.json['string'])
		seq = []
		seq.append(j['title'])
		seq.append(json.dumps(j['doc']))
		seq.append(str(id))
		try:
			c.execute(sql, seq)
			conn.commit()
			c.close()
			return id, 201
		except( Exception, ps.DatabaseError) as error:
			print("ERROR: "+str(error))

	def delete(self, id):
		sql = "DELETE FROM cards WHERE _id = '"+id+"';"
		c = conn.cursor()
		try:
			c.execute(sql)
			conn.commit()
			c.close()
			return id, 201
		except( Exception, ps.DatabaseError) as error:
			print("ERROR: "+str(error))

api.add_resource(pimp_api, '/pimp/', endpoint = 'cards', resource_class_kwargs = {'db_connection':conn})
api.add_resource(pimp_card_api, '/pimp/<string:id>', endpoint = 'card', resource_class_kwargs = {'db_connection':conn})

if __name__ == '__main__':
	app.run(debug=True)
