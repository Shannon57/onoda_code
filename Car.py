import socket
import json

EDGE_IP = '127.0.0.1'
EDGE_PORT = 12300

class Car:
	def __init__(self, num):
		self.car_id = num

	def create_demand(self, org, dst):
		demand_data = {}
		demand_data['id'] = self.car_id
		demand_data['demand'] = {}
		demand_data['demand']['org'] = org
		demand_data['demand']['dst'] = dst
		demand_data['demand']['dpt'] = '' 
		demand_data['path'] = ''
		return demand_data

	def reqest_to_edge(self):
		request_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		request_socket.connect((EDGE_IP, EDGE_PORT))#サーバー側のipと使用するポート(ポートはサーバーと同じにする。)
		request_data = self.create_demand(1, 5)
		request_socket.sendall(json.dumps(request_data).encode())
		print('送信しました')
		recv_data = request_socket.recv(4096)
		data = json.loads(recv_data)
		print(data)
		request_socket.close()

if __name__ == '__main__':
	m5 = Car(57)
	m5.reqest_to_edge()
