# Load .env file variables
from dotenv import load_dotenv, dotenv_values

class Config:
    # Load variables from the specified .env file
    def load_env(self):
        load_dotenv()
        return dotenv_values()

    # Load environment variables and retrieve the value for the specified key
    def get(self, key, default=None):
        env_variables = self.load_env()
        return env_variables.get(key, default)

