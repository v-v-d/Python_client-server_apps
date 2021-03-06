"""Main script for server side messenger app."""
import os
import yaml
import logging

from argparse import ArgumentParser

from src.handlers import handle_default_request
from src.database import Base
from src.app import Application
from src.settings import INSTALLED_MODULES, BASE_DIR


class ConfigFromCLI:
    """Get config that passed through CLI."""
    def __init__(self):
        """Default settings that can be set up by passed through CLI commands."""
        self.is_db_migrated = False
        self._host = '127.0.0.1'
        self._port = 8000
        self._set_config()

    def _set_config(self):
        """Set up the default settings based on passed arguments."""
        config = self._get_config_from_file()
        if config:
            self._host = config.get('host')
            self._port = int(config.get('port'))

    def _get_config_from_file(self):
        """Check for passed arguments ans set up migration default settings."""
        args = self._get_args()
        if args.migrate:
            self.is_db_migrated = True
        if args.config:
            with open(args.config) as file:
                return yaml.load(file, Loader=yaml.Loader)

    @staticmethod
    def _get_args():
        """Define how a args should be parsed and return args as objects."""
        parser = ArgumentParser()
        parser.add_argument(
            '-c', '--config', type=str,
            required=False, help='Sets config file path'
        )
        parser.add_argument(
            '-m', '--migrate', action='store_true'
        )
        return parser.parse_args()

    @property
    def host(self):
        """Return app host."""
        return self._host

    @property
    def port(self):
        """Return app port."""
        return self._port


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../../src/server/server.log', encoding='UTF-8'),
        logging.StreamHandler(),
    ]
)

config = ConfigFromCLI()
if config.is_db_migrated:
    # Import all models from all modules for initialize DB migrations (Base.metadata.create_all() method).
    module_name_list = [f'{item}.models' for item in INSTALLED_MODULES]
    module_path_list = (os.path.join(BASE_DIR, item, 'models.py') for item in INSTALLED_MODULES)
    for index, path in enumerate(module_path_list):
        if os.path.exists(path):
            __import__(module_name_list[index])
    Base.metadata.create_all()
else:
    with Application(handle_default_request) as app:
        app.host, app.port = config.host, config.port
        app.run()
