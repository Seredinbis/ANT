import os
from dotenv import load_dotenv

load_dotenv()

ip_address: str = os.getenv('IP_ADDRESS')
port: int = int(os.getenv('PORT'))
logs_path: str = os.getenv('LOGS_PATH')
