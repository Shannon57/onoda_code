import socket
import queue
import json

CLOUD_IP = '127.0.0.1'
CLOUD_PORT = 32100

class Cloud:
	def __init__(self, ip, port):
		self.cloud_ip = ip
		self.cloud_port = port
		self.request_queue = queue.Queue(maxsize=1)
		self.serve_queue = queue.Queue(maxsize=1)

	def processing(self):
		receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		receiver_socket.bind((self.cloud_ip, self.cloud_port))
		receiver_socket.listen(10)
		while True:
			sock, _addr = receiver_socket.accept()
			print('接続しました')
			with sock:
				received_data = b''
				received_data = sock.recv(4096)

				# jsonに変更
				request_data = json.loads(received_data)
				send_data = json.dumps(self.process_data(request_data)).encode('utf-8')
				sock.sendall(send_data)


	def process_data(self, request_data):
		request_data['demand']['path'] = '0,1,2,3,-1'
		return request_data


	def forever(self):
		self.processing()


if __name__ == '__main__':
	cloud_server = Cloud(CLOUD_IP, CLOUD_PORT)
	cloud_server.forever()