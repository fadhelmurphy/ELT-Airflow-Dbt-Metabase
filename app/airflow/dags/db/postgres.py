
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

engine = create_engine(os.getenv('ENGINE_CONNECT'))

