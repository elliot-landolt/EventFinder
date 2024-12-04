import os
from dotenv import load_dotenv
load_dotenv() # look in the .env file for env vars
GEOAPIFY_KEY= os.getenv("GEOAPIFY_KEY")