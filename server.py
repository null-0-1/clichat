#!/usr/bin/env python3
class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clients = []
	
	def start(self):
		self.server_socket.bind((self.host, self.port))
		self.server_socket.listen(5)
		print(f"Server started on {self.host}:{self.port}")
		while True:
			client_socket, address = self.server_socket.accept()
			print(f"Connected by {address}")
			self.clients.append(client_socket)
			threading.Thread(target=self.handle_client, args=(client_socket,)).start()
 
	def handle_client(self, client_socket):
		while True:
			try:
				message = client_socket.recv(1024).decode('utf-8')
				print(f"Received: {message}")
				self.broadcast(message, client_socket)
			except (ConnectionResetError, ConnectionAbortedError) as e:
				print(f"Client disconnected: {e}")
				if client_socket in self.clients:
					self.clients.remove(client_socket)
					client_socket.close()
					break
			except Exception as e:
				print(f"Error: {e}")

	def broadcast(self, message, sender_socket):
		for client in self.clients:
			if client != sender_socket:
				client.send(message.encode('utf-8'))

if __name__ == "__main__":
	import argparse
	import socket
	import threading
	parser=argparse.ArgumentParser(description="host")
	parser.add_argument("-s","--server",help="ip add")
	parser.add_argument("-p","--port",help="port to listen to")
	args=parser.parse_args()
	server=args.server
	port=args.port
	server = Server(server,int(port))
	server.start()