from flask import jsonify, request
from flask_restful import Api, Resource
import json
import uuid
import psycopg2 as ps

class pimp_api( Resource ):
	def __init__(self, db_connection):
		self.conn = db_connection

	def get(self):
		sql = """SELECT _id, title, born, doc from cards;"""
		c = self.conn.cursor(cursor_factory=ps.extras.RealDictCursor)
		try:
			c.execute(sql)
			r = c.fetchall();
			c.close()
			return jsonify(r)
		except (Exception, ps.DatabaseError) as error:
			return jsonify(error)

	def post(self):
		j = json.loads(request.form['string'])
		if not j or not 'title' in j:
			abort(400)
		sql = """INSERT INTO cards(_id, title, born, doc) VALUES (%s, %s, %s, %s);"""
		c = self.conn.cursor() # cursor_factory=ps.extras.RealDictCursor)
		id = str(uuid.uuid4())
		print(id)
		seq = []
		seq.append(id)
		seq.append(j['title'])
		seq.append(j['born'])
		seq.append(json.dumps(j['doc']))
		try:
			c.execute(sql, seq)
			self.conn.commit()
			c.close()
			return id, 201
		except (Exception, ps.DatabaseError) as error:
			print("ERROR: "+str(error))
