from dotenv import dotenv_values

class EnvReader:
    def __init__(self, env_file_path) -> None:
        self.env_file_path = env_file_path
        self.env_config = dotenv_values(self.env_file_path)
        
    def read(self, key):
        return self.env_config[key] 