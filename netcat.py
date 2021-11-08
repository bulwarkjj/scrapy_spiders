import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    # receives commands, runs it, and returns output of command
	cmd = cmd.strip()
	if not cmd:
		return
	output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
	return output.decode()

class NetCat:
	# Initialize NetCat object with args form cmdline and the buffer
	def __init__(self, args, buffer=None):
		self.args = args
		self.buffer = buffer
		# Create the socket object
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Overcome the "Address already in use" my manipulating options at the socket level
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def run(self):
        # entry point for managing the NetCat object
        # delegeted to two methods: listen or send
		if self.args.listen:
			self.listen()
		else:
			self.send()

	def send(self):
		# Connect to target:port (Send data from stdin as bytes)
		self.socket.connect((self.args.target, self.args.port))
		# If we have a buffer, we send that to the target first
		if self.buffer:
			self.socket.send(self.buffer)

		# Try/cath block (connection can be closed with ctrl+c)
		try:
			# Loop to receive data from the target
			while True:
				recv_len = 1
				response = ''
				while recv_len:
					data = self.socket.recv(4096)
					recv_len = len(data)
					response += data.decode()

					# If there's no more data, break out of the loop
					if recv_len < 4096:
						break
				
				''' Print the response data and pause to get interactive input,
				send that input, continue the loop '''
				if response:
					print(response)
					buffer = input('> ')
					buffer += '\n'
					self.socket.send(buffer.encode())

		# The loop will continue until ctrl+c (keyboardinterrupt) occurs
		except KeyboardInterrupt:
			print('User terminated.')
			self.socket.close()
			sys.exit()

	def listen(self):
		# Bind to target:port
		self.socket.bind((self.args.target, self.args.port))
		self.socket.listen(5)

		# Loop, start listening
		while True:
			client_socket, _ = self.socket.accept()
			# Pass the connected socket to the handle method
			client_thread = threading.Thread(target=self.handle, args=(client_socket,))
			client_thread.start()

	def handle(self, client_socket):
		# Pass the command to execute function and send the output back on the socket
		if self.args.execute:
			output = execute(self.args.execute)
			client_socket.send(output.encode())

		# Set up a loop to listen for content on the listening socket
		elif self.args.upload:
			file_buffer = b''
			while True:
				# Receive data until there's no more coming in
				data = client_socket.recv(4096)
				if data:
					file_buffer += data
				else:
					break
				# Write accumulated content to the specified file
				with open(self.args.upload, 'wb') as file:
					file.write(file_buffer)
				message = "" # f'Saved file {self.args.upload}' <- invalid syntax
				client_socket.send(message.encode())
		
		# Set up a loop, send a prompt to the sender, wait for a command string
		elif self.args.command:
			cmd_buffer = b''
			while True:
				try:
					client_socket.send(b'BHP: #> ')
					# Search for newline chars to determine when to process a command
					while '\n' not in cmd_buffer.decode():
						cmd_buffer += client_socket.recv(64)
					response = execute(cmd_buffer.decode())
					# Return output of the command to the sender
					if response:
						client_socket.send(response.encode())
					cmd_buffer = b''
				except Exception as e:
					print("Server killed") #(f'Server killed {e}') <- invalid syntax
					self.socket.close()
					sys.exit()

# Main block
if __name__ == '__main__':
	# Usage & examples
	parser = argparse.ArgumentParser(description='BHP Net Tool',formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent
		('''Example:
		netcat.py -t 192.168.1.108 -p 5555 -c # command shell
		netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
		netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
		echo 'ABC' | /.netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
		netcat.py -t 192.168.1.108 -p 5555 # connect to server
		'''))
	
	# Setting up arguments
	parser.add_argument('-c', '--command', action='store_true', help='command shell')
	parser.add_argument('-e', '--execute', help='execute specified command')
	parser.add_argument('-l', '--listen', action='store_true', help='listen')
	parser.add_argument('-p', '--port', type=int,default=5555, help='specified port')
	parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
	parser.add_argument('-u', '--upload', help='upload file')
	args = parser.parse_args()

	# Listener with an empty buffer string
	if args.listen:
		buffer = ''

	# Send buffer from standard input
	else:
		buffer = sys.stdin.read()
	nc = NetCat(args, buffer.encode())
	nc.run()