from flask import jsonify, request
from flask_restful import Resource
import json
import psycopg2 as ps

class pimp_card_api( Resource ):
	def __init__(self, db_connection):
		self.conn = db_connection

	def get(self, id):
		sql = "SELECT _id, title, born, doc FROM cards WHERE _id = '"+id+"';"
		c = self.conn.cursor(cursor_factory=ps.extras.RealDictCursor)
		try:
			c.execute(sql)
			r = jsonify(c.fetchone())
			c.close()
			return r
		except (Exception, ps.DatabaseError) as error:
			print("ERROR: "+str(error))

	def put(self, id):
		sql = """UPDATE cards SET title=%s, doc=%s WHERE _id = %s"""
		c = self.conn.cursor()
		j = json.loads(request.json['string'])
		seq = []
		seq.append(j['title'])
		seq.append(json.dumps(j['doc']))
		seq.append(str(id))
		try:
			c.execute(sql, seq)
			self.conn.commit()
			c.close()
			return id, 201
		except( Exception, ps.DatabaseError) as error:
			print("ERROR: "+str(error))

	def delete(self, id):
		sql = "DELETE FROM cards WHERE _id = '"+id+"';"
		c = self.conn.cursor()
		try:
			c.execute(sql)
			self.conn.commit()
			c.close()
			return id, 201
		except( Exception, ps.DatabaseError) as error:
			print("ERROR: "+str(error))
