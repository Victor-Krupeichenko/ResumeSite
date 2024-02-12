from .url_database import connect_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(connect_url.connection_string)
session_maker = sessionmaker(engine)
