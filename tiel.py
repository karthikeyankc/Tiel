import sqlite3
import random

# Baby memories.
init_memory = {"question":['I do not know how to respond to this. Teach me and I will remember it!', 'How do I respond to this? Train me!', 'I have no idea how to respond to this! Teach me, will you?']}

# A simple cognitive(ish) structure for a robot(ish) program to listen, process, learn and speak.
class Robot(object):
	def __init__(self):
		global init_memory
		self.init_memory = init_memory
	
	def load_memory(self, user_voice):
		global conn
		conn = sqlite3.connect('memory.db')
		global c
		c = conn.cursor()
		c.execute ('CREATE TABLE IF NOT EXISTS response_memory (user_voice, response)')
		conn.commit()
		response_memory = c.execute('SELECT user_voice, response FROM response_memory WHERE user_voice=?', (user_voice,)).fetchall()
		return response_memory

	def listen(self):
		user_voice = raw_input("[You] ")
		self.process(user_voice)

	def process(self, user_voice):
		
		def remember(user_voice):
			thoughts = self.load_memory(user_voice)
			print thoughts
			if thoughts:
				for u, r in thoughts:
					user_data = u
					response_data = r
			else:
				user_data = None
				response_data = None

			return user_data, response_data

		def learn(user_voice):
			if user_voice != None:
				learned_response = raw_input("[Tiel] "+random.choice(init_memory['question'])+"\n")
				c.execute('INSERT INTO response_memory(user_voice, response) VALUES(?,?)', (user_voice, learned_response))
				conn.commit()
				self.listen()
			else:
				self.speak(response_data)

		user_data, response_data = remember(user_voice)
		if user_voice == user_data:
			self.speak(response_data)
		else:
			learn(user_voice)

	def speak(self, response_data):
		goodbye = ['bye', 'see you later', 'bubye', 'goodbye' ]
		print "[Tiel] %s" %response_data
		if response_data in goodbye:
			exit()
		else:
			self.listen()

tiel = Robot() # Tiel was a mascot I once designed for swyde. The name just sparked out of thin air.
tiel.listen()