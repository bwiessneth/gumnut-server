import os
from os import path
import argparse
import click

import logging
from logging.config import fileConfig
logger = logging.getLogger(__name__)

from gumnut_server import __version__


@click.version_option(prog_name='gumnut-server', version=__version__)
@click.group()
def server():
	# logger.add("gumnut_server.log", rotation="50 MB")    # Automatically rotate too big file
	log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.conf')
	logging.config.fileConfig(log_file_path, disable_existing_loggers=False)	
	logger.info(f"gumnut-server {__version__}")
	pass


@server.command()
@click.option('-h', '--host', default='127.0.0.1', type=str, help='Host for communication', show_default=True)
@click.option('-p', '--port', default=5000, type=int, help='Port for communication', show_default=True)
def websocket(host, port):
	"""Run server in websocket mode
	\f
	:param port: The port number for the server to listen on. Defaults to `5000`
	:type port: int, optional
	:param host: The hostname or IP address for the server to listen on. Defaults to `127.0.0.1`
	:type host: str, optional
	"""
	from gumnut_server import websocket
	try:
		websocket.run(host, port)
	except Exception as e:
		logging.error("Unhandled exception:")
		logging.error(e, exc_info=True)
		logger.critical("There was an unhandled exception. Stopping now!")		
		os._exit(1)