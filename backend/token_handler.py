#!/usr/bin/env python
"""Containes all the classes and constants required to request, refresh and handle the server tokens."""

class TokenHandler:
	"""Aquires (requests to the server), saves (safelly) and refreshes a token."""

	def __init__(self):
		"""Contructor. Loads the saved tokens."""
		self.__loadTokens()


	@property
	def token(self):
		"""Get the current token."""
		return self.__token



	def hasToken():
		"""Does it have a token?"""
		return self.__token != None



	def hasRefreshToken(self):
		"""Does it have a refresh token?"""
		return self.__refreshToken != None



	def refreshToken(self):
		"""Refreshes the token with the refresh token. Returns if it succeded."""
		if !self.hasRefreshToken():
			return False

		token = refreshToken = None
		# TODO do the refresh of the token

		self.__token = token
		self.__refreshToken = refreshToken
		self.__saveTokens()

		# TODO Return True when succeds
		return False



	def requestNewToken(self, user, password):
		"""Requests a new token to the server."""

		token = refreshToken = None

		# TODO make the actual request

		self.__token = token
		self.__refreshToken = refreshToken
		self.__saveTokens()



	def __loadTokens(self):
		"""Saves the tokens in a safe place."""
		token = refreshToken = None

		# TODO Load tokens from vault
		return token, refreshToken



	def __saveTokens(self):
		"""Saves the tokens in a safe place."""
		# TODO Remove old saved tokens
		# TODO Save new tokens
		pass
