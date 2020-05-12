import os
import yaml
import logging.config
import logging
import coloredlogs

from packages.main import app


def setup_logging(default_path='logging.yml', default_level=logging.INFO):
    if not os.path.exists(default_path):
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')
    else:
        with open(default_path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print('Error in Logging Configuration. Using default configs', e)
                logging.basicConfig(level=default_level)
                coloredlogs.install()


setup_logging()

if __name__ == "__main__":
    app.run()
