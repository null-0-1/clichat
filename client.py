#!/usr/bin/env python3
class Client:
	def __init__(self):
		self.online = True
		self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, server, port):
		try:
			with open("chat.txt", "w") as f:
				f.write("")
				self.con.connect((server, port))
				threading.Thread(target=self.receive_mes).start()
			self.send_mes()
		except ConnectionRefusedError:
			print("Connection refused.")
		except Exception as e:
			print(f"Error: {e}")

	def send_mes(self):
		while self.online:
			try:
				to_send = input("unfold/send/discon: ")
				if to_send == "unfold":
					self.unfold()
				elif to_send == "send":
					to_send = input("send: ")
					self.con.send(to_send.encode('utf-8'))
					with open("chat.txt", "a") as f:
						f.write(f"|{to_send}|")
						f.close()
				elif to_send == "discon":
					self.con.close()
					sys.exit(0)
			except Exception as e:
				print(f"Error: {e}")

	def receive_mes(self):
		while self.online:
			try:
				received = self.con.recv(1024).decode('utf-8')
				with open("chat.txt", "a") as f:
					f.write(f"|{received}|")
			except Exception as e:
				print(f"Error: {e}")
				self.con.close()
				self.online = False

	def unfold(self):
		with open("chat.txt", "r") as f:
			chats = f.read().split("|")
			for i in chats:
				print(i)


if __name__ == "__main__":
	import argparse
	import socket
	import threading
	import sys
	parser = argparse.ArgumentParser(description="client")
	parser.add_argument("-s", "--server", help="server to join")
	parser.add_argument("-p", "--port", help="port to connect to")
	args = parser.parse_args()
	client = Client()
	server=args.server
	port=args.port
	client.connect(server, int(port))