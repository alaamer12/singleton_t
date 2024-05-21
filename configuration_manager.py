import threading
import configparser
from pprint import pprint
import os
import contextlib


class ConfigurationManager:
    __instance = None
    __lock = threading.Lock()
    __CONFIG_FILE = 'config.ini'

    def __new__(cls):
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = super().__new__(cls)
                cls.__instance.config = configparser.ConfigParser()
                if os.path.exists(cls.__CONFIG_FILE):
                    cls.__instance.config.read(cls.__CONFIG_FILE)
        return cls.__instance

    def save_to_file(self):
        with open(self.__CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def update(self, section, key, value):
        self.config.set(section, key, value)
        self.save_to_file()

    def read(self, section, key):
        if not os.path.exists(self.__CONFIG_FILE):
            raise FileNotFoundError(f"File '{self.__CONFIG_FILE}'"
                                    f" not found, Have you created it yet?")
        return self.config.get(section, key)

    def read_all(self):
        for section in self.config.sections():
            for key, value in self.config.items(section):
                pprint(f"{key}: {value}")

    def delete(self, section):
        self.config.remove_section(section)
        self.save_to_file()

    def add(self, section, key, value):
        with contextlib.suppress(Exception):
            self.config.add_section(section)
            self.config.set(section, key, value)
            self.save_to_file()

    def create_config(self):
        if not os.path.exists(self.__CONFIG_FILE):
            with open(self.__CONFIG_FILE, 'w') as configfile:
                self.config.write(configfile)


# Example usage
if __name__ == "__main__":
    config_manager = ConfigurationManager()
    config_manager.create_config()
    config_manager.add('Section4', 'Key1', 'Value1')
    config_manager.add('Section5', 'Key3', 'Value3')
    config_manager.add('Section6', 'Key3', 'Value3')
    config_manager.update('Section6', 'Key6', 'Value6')
    config_manager.delete('Section1')
    config_manager.read_all()
