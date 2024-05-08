import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

postgres = psycopg.connect(os.environ["POSTGRES_URI"])
