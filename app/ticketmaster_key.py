import os
from dotenv import load_dotenv
load_dotenv() # look in the .env file for env vars
TICKETMASTER_KEY= os.getenv("TICKETMASTER_KEY")