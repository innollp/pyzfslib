#!/usr/bin/python

import subprocess as sp
import os

def _list_parse(line):
	parts = line.decode('utf-8').split('\t')
	"""
		{'mountpoint': '-', 'creation': '1433944122', 'refer': '19456', 'name': 'zroot/ROOT@os_install_done', 'avail': '-', 'used': '0'}
	"""
	vol = parts[0].split('@')[0]
	snapname = parts[0].split('@')[1]
	if parts[1] == '-':
		creation = None
	else:
		creation = int(parts[1])
	if parts[2] == '-':
		used = None
	else:
		used = int(parts[2])
	if parts[3] == '-':
		avail = None
	else:
		avail = int(parts[3])
	if parts[4] == '-':
		refer = None
	else:
		refer = int(parts[4])
	if parts[5] == '-':
		mountpoint = None
	else:
		mountpoint = parts[5]
	
	return {
		'vol':        vol,
		'snapname':   snapname,
		'creation':   creation,
		'used':       used,
		'avail':      avail,
		'refer':      refer,
		'mountpoint': mountpoint
		}

class PrivCommandException(Exception):
	pass

class ZfsCommandException(Exception):
	pass

class Snapshot:
	def __init__(self, priv_command=['sudo', '-n']):
		if priv_command != None:
			self.priv_command = priv_command
		else:
			self.priv_command = []	
		pass

	def create(self, vol, snapname):
		p = sp.Popen(self.priv_command + ['zfs', 'snapshot', '{}@{}'.format(vol, snapname)], stdout=sp.PIPE, stderr=sp.PIPE)
		(stdout,errout) = p.communicate()
		p_ret = p.wait()
		if p_ret == 0:
			return True
		else:
			raise ZfsCommandException(errout.decode('utf-8').strip())

	def list(self):
		p = sp.Popen(self.priv_command + ['zfs', 'list', '-Hp', '-t', 'snapshot', '-o', 'name,creation,used,avail,refer,mountpoint'], stdout=sp.PIPE, stderr=sp.PIPE)
		(stdout,errout) = p.communicate()
		p_ret = p.wait()
		if p_ret != 0:
			if p_ret == 1:
				raise PrivCommandException(errout.decode('utf-8').strip())
			else:
				raise ZfsCommandException('Generel command error')
		ret = list()
		for l in stdout.splitlines():
			ret.append(_list_parse(l))
		return ret

	def destroy(self, vol, snapname):
		"""
			sudo zfs destroy zroot/ROOT/tmp@test1
		"""
		p = sp.Popen(self.priv_command + ['zfs', 'destroy', '{}@{}'.format(vol, snapname)], stdout=sp.PIPE, stderr=sp.PIPE)
		(stdout,errout) = p.communicate()
		p_ret = p.wait()
		if p_ret == 0:
			return True
		else:
			raise ZfsCommandException(errout.decode('utf-8').strip())
	"""
		filters = [('used', 'lt', 500), ('vol', 'name', 'zroot/ROOT/tmp')]
	"""
	def list_sort(self, sort=None, filters=None):
		l = self.list()
		if filters != None:
			for fil in filters:
				if fil[1] == 'lt':
					l = [dictio for dictio in l if dictio[fil[0]] < fil[2]]
				elif fil[1] == 'gt':
					l = [dictio for dictio in l if dictio[fil[0]] > fil[2]]
				elif fil[1] == 'eq':
					l = [dictio for dictio in l if dictio[fil[0]] == fil[2]]
				elif fil[1] == 'le':
					l = [dictio for dictio in l if dictio[fil[0]] <= fil[2]]
				elif fil[1] == 'ge':
					l = [dictio for dictio in l if dictio[fil[0]] >= fil[2]]
				elif fil[1] == 'starts':
					l = [dictio for dictio in l if dictio[fil[0]].startswith(fil[2])]
		if sort != None:
			if sort.startswith('-'):
				l = sorted(l, key=lambda tup: tup[sort[1:]])
				l.reverse()
			else:
				l = sorted(l, key=lambda tup: tup[sort])
		return l





