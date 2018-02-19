#!/usr/bin/env python
"""
Package containing all the classes and utilities to communicate with the Giscube
server.
"""


class BadCredentials(ConnectionError):
	"""
	The credentials or the token used are wrong or have expired.
	"""
	pass

# TODO do all the https requests
class GiscubeRequests:
	"""
	Handles all the requests to the Giscube server. May return a BadCredentials
	error.
	"""
	def __init__(self, server_ip, token_handler):
		self.__ip = server_ip
		self.__token_handler = token_handler

	def requestProjectsList(self):
		"""
		Returns a list with all the projects. May return a BadCredentials error.
		"""
		return []

	def requestProject(self, project_name):
		"""
		Downloads the project file and returns its path.
		"""
		return path

	def pushProject(self, path, project_name):
		"""
		Saves the project in a path to the server with project_name overriding
		it if exists. May return a BadCredentials error.
		"""
		pass
