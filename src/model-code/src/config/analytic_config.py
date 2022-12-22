import json
import os

import yaml


class AnalyticConfig:
    INSTANCE = None

    def __init__(self, config_yml_path='../src/config/config.yaml', verbose=False):
        self.config_yml_path = config_yml_path
        self.verbose = verbose

    def get_config(self):
        if self.INSTANCE is None:
            self.INSTANCE = self._load_config()
        return self.INSTANCE

    class Config:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key.lower(), value)

        def __str__(self):
            dct = self.__dict__
            dct_temp = dct.copy()
            for key, fields_meta in dct_temp.pop('__fields').items():
                if fields_meta['is_secret']:
                    dct_temp.pop(key.lower())
            return json.dumps(dct_temp, indent=4)

    def _load_config(self):
        # If yml path exists, read from it. Else, from env
        config_dict = {}
        if os.path.exists(self.config_yml_path):
            if self.verbose:
                print('Loading config from: {}'.format(self.config_yml_path))
            with open(self.config_yml_path, 'r', encoding="utf-8") as stream:
                config_dict = yaml.safe_load(stream)

        return config_dict
