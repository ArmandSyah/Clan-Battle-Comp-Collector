import json
import os

class ConfigReader():
    def __init__(self, config_file_path) -> None:
        if not os.path.exists(config_file_path): 
            raise FileNotFoundError('config file cannot be found at current location, please double check again')
        
        self.config_file_path = config_file_path
        
    def read(self, *args):
        with open(self.config_file_path, 'r') as config_file:
            data = json.load(config_file)
        
        i = 0
        config_value = None    
        while i < len(args):
            if config_value is None:
                config_value = data[args[i]]
            else:
                config_value = config_value[args[i]]
            i += 1
            
        return config_value
    
    def write(self, value, *args) -> None:
        with open(self.config_file_path, 'r') as config_file:
            data = json.load(config_file)
            
        i = 0
        config_value = None    
        while i < len(args) - 1:
            if config_value is None:
                config_value = data[args[i]]
            else:
                config_value = config_value[args[i]]
            i += 1
        
        config_value[args[i]] = value
        
        with open("config.json", "w") as config_file:
            json.dump(data, config_file, indent=4)
        
        
        