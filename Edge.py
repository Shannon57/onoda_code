#EdgeとCloudの間には遅延を発生させるためのTcコマンドなどを実装すること

import socket
import json
import queue
import threading
import time


EDGE_IP = '192.168.7.7'
EDGE_PORT = 12300

CLOUD_IP = '127.0.0.1'
CLOUD_PORT = 32100

class Edge:
	def __init__(self, ip, port):
		"""
		初期設定
		"""
		self.edge_ip = ip
		self.edge_port = port
		self.car_connection = 0
		self.cloud_connection = 0
		self.request_queue = queue.Queue(maxsize=1)
		self.serve_queue = queue.Queue(maxsize=1)

	def create_demand(self, org, dst):
		demand_data = {}
		demand_data['id'] = self.car_id
		demand_data['demand'] = {}
		demand_data['demand']['org'] = org
		demand_data['demand']['dst'] = dst
		demand_data['demand']['dpt'] = '' 
		demand_data['path'] = ''
		return demand_data

	def receive_from_car(self):
		receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		receiver_socket.bind((self.edge_ip, self.edge_port))
		receiver_socket.listen(10)
		while True:
			sock, _addr = receiver_socket.accept()
			print('車と接続しました')
			
			with sock:
				received_data = b''
				received_data = sock.recv(4096)
				# jsonに変更
				data = received_data.decode().split(',')
				print("車からの受信データ {}".format(data))
				reqest_data = json.dumps(self.create_demand(data[0], data[1])).encode()

				self.request_queue.put(reqest_data)
				print('車から受信完了しました')
				send_data = json.loads(self.serve_queue.get().decode())
				print(send_data)
				data= send_data['demand']['path'].encode('utf-8')
				print(data)
				sock.sendall(data)
				print('車へ送信完了しました')


	def request_to_cloud(self):
		while True:
			#getできるまで待つ
			request_data = self.request_queue.get()
			request_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			request_socket.connect((CLOUD_IP, CLOUD_PORT))#サーバー側のipと使用するポート(ポートはサーバーと同じにする。)
			request_socket.sendall(request_data)
			print('クラウドに送信しました')
			recv_data = request_socket.recv(4096)
			print('クラウドから受信しました')
			self.serve_queue.put(recv_data)
			request_socket.close()


	def forever(self):
		"""
		エッジサーバを起動
		やること
		クラウドからも車からも受信する

		受信したら返す

		コネクションは維持しておく
		"""
		#ここで車とのコネクションを待つ
		thread1 = threading.Thread(target=self.receive_from_car)
		thread2 = threading.Thread(target=self.request_to_cloud)
		thread1.start()
		thread2.start()


if __name__ == '__main__':
	edge_server = Edge(EDGE_IP, EDGE_PORT)
	edge_server.forever()



