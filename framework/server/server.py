import json
import os
import datetime
from time import sleep
import socket
import hashlib
import threading
from connection_handler import handle_connection

def initializeListener():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('192.168.1.125', 3344))
		s.listen(10)
		while True:
			print("[i] Waiting for connections..")
			conn, addr = s.accept()
			new_conn_handler = threading.Thread(target=handle_connection, args=(conn,addr))
			new_conn_handler.start()

	except KeyboardInterrupt:
		s.close()
	except Exception:
		s.close()
		raise

initializeListener()