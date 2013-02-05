import sqlite
import time

class botsqlite:
	def __init__(self, botdb):
		self.connection = sqlite.connect(botdb)
		self.cursor = self.connection.cursor()

	def add_connection(self, pid, nick_id, server_id):
		timestamp = time.time()
		self.cursor.execute('INSERT INTO connections VALUES ("%s","%s","%s","%s")', (pid,nick_id,server_id,timestamp))
		self.connection.commit()
		return True

	def del_connection(self, pid):
		pass

	def get_pid(self, server_id, nick_id):
		self.cursor.execute('SELECT pid FROM connections WHERE nick_id="%s" AND server_id="%s"', (nick_id,server_id))
		self.connection.commit()
		vals = self.cursor.fetchall()

		if vals is None:
			return False
		else:
			return vals[0]

	def get_server_id(self, server_name, port = None):
		if port is None:
			self.cursor.execute('SELECT server_id FROM servers WHERE host="%s" AND port="%s"', (server_name,port))
		else:
			self.cursor.execute('SELECT server_id FROM servers WHERE host="%s"', (server_name,))
			
		self.connection.commit()
		vals = self.cursor.fetchone()

		if vals is None:
			return False
		else:
			return vals[0]

	def get_nick_id(self,nickname):
		self.cursor.execute('SELECT nick_id FROM nicks WHERE nickname="%s"', (nickname,))
		self.connection.commit()
		vals = self.cursor.fetchone()

		if vals is None:
			return False
		else:
			return vals[0]

	def random_nick(self):
		self.cursor.execute('SELECT nickname FROM nicks ORDER BY RANDOM() LIMIT 1')
		self.connection.commit()
		vals = self.cursor.fetchone()

		if vals is None:
			return False
		else:
			return vals[0]

	def random_server(self):
		self.cursor.execute('SELECT host,port FROM servers WHERE covered="0" ORDER BY RANDOM() LIMIT 1')
		self.connection.commit()
		vals = self.cursor.fetchone()

		if vals is None:
			return False
		else:
			return vals

	def nick_is_exempt(self, nickname, server_id="all"):
		self.cursor.execute('SELECT COUNT(exempt_id) FROM exempt_users WHERE nickname="%s" AND server_id="%s"', (nickname,server_id))
		self.connection.commit()
		vals = self.cursor.fetchone()

		if (vals[0] < 1):
			return False
		else:
			return True

	def add_exemption(self, nickname, server_id):
		self.cursor.execute('INSERT INTO exempt_users VALUES(NULL,"%s","%s")', (nickname,server_id))
		self.connection.commit()
		is_exempt = self.nick_is_exempt(nickname,server_id)
		if (is_exempt):
			return True
		else:
			return False

	def remove_exemption(self, nickname, server_id=None):
		if (server_id is None):
			self.cursor.execute('DELETE FROM exempt_users WHERE nickname="%s"', (nickname,))
		else:
			self.cursor.execute('DELETE FROM exempt_users WHERE nickname="%s" AND server_id="%s"', (nickname,server_id))
		self.connection.commit()
		return True

	def get_the_who(self):
		vals = []
		self.cursor.execute('SELECT who FROM thewho')
		self.connection.commit()
		for row in self.cursor:
			vals.append(row[0])
		return vals

	def add_alert(self, nickname, channel, server):
		nick_id 	= self.get_nick_id(nickname)
		server_id	= self.get_server_id(server)
		timestamp 	= time.time()
		
		self.cursor.execute('INSERT INTO alerts VALUES(NULL,"%s","%s","%s","%s","%s")', (nick_id,server_id,timestamp,nickname,channel))
		self.connection.commit()
