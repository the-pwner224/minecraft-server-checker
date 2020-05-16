#!/usr/bin/env python3

import sys
#hostname, port = sys.argv[1], int(sys.argv[2])
hostname, port = '167.172.155.5', 25565

refresh_time = 60 # seconds





# https://gaming.stackexchange.com/a/166587

import json
import os
import platform
import socket as S
import time

is_mac = platform.system() == 'Darwin'

def fetch_status():
	s = S.socket(2,1)
	s.connect((hostname, port))

	def pop_int():
		a = 0
		b = s.recv(1)[0]
		while b & 0x80:
			a = (a<<7) + b&0x7f
			b = s.recv(1)[0]
		return (a<<7) + b&0x7f

	def pack_varint(d,b):
		return bytes([(0x40*(i!=b//7))+((d>>(7*(i)))%128)for i in range(1+b//7)])

	def pack_data(d):
		return pack_varint(len(d), len(d).bit_length()) + d

	s.send(pack_data(bytes(2)+pack_data(bytes(hostname,'utf-8'))+bytes([port >> 8, port % 256, 1]))+bytes([1,0]))

	pop_int() # packet length
	pop_int() # packet ID
	l = pop_int()
	d = bytes()

	while len(d) < l:
		d += s.recv(1024)

	s.close()
	j = json.loads(str(d, 'utf-8'))

	#{
	#	'description': { 'text': "Don't get corona!" },
	#	'players':     { 'max': 20, 'online': 0 },
	#	'version':     { 'name': 'Spigot 1.15.2', 'protocol': 578 }
	#}

	s_name = j['description']['text']
	s_players = j['players']['online']
	s_max_players = j['players']['max']
	return s_name, s_players, s_max_players



if len(sys.argv) == 2:
	# check status right now
	s_name, s_players, s_max_players = fetch_status()
	print(f'{s_name}: {s_players}/{s_max_players}')
else:
	# start polling and sending notifications
	last_numplayers = 0

	while True:
		s_name, s_players, s_max_players = fetch_status()

		if last_numplayers != s_players: # if there was a change in number of players
			last_numplayers = s_players

			not_title = s_name + ' status:'
			not_body = str(s_players) + '/' + str(s_max_players)

			if is_mac: # on mac, remove " and '
				not_title.replace('"', "")
				not_body.replace('"', "")
				not_title.replace("'", "")
				not_body.replace("'", "")
			else: # on linux, just remove " (actually replace it with ')
				not_title.replace('"', "'")
				not_body.replace('"', "'")

			if is_mac:
				not_cmd = f'osascript -e \'display notification "{not_body}" with title "{not_title}"\''
			else:
				not_cmd = f'notify-send "{not_title}" "{not_body}"'
			os.system(not_cmd)

		time.sleep(refresh_time)
