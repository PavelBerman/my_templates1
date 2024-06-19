import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# load environment variables from file - relevant only for development environment.
# in production environment the file doesn't exist and this code section does nothing.
main_dir = os.path.dirname(os.path.abspath(__file__))
local_env_file = os.path.join(main_dir, '.env')
load_dotenv(local_env_file, verbose=True)

# load environment variables
MYSQL_CON_STR = os.environ.get("MYSQL_CON_STR")

# pool size 1 fits lammbda since it's a single thread
sql_db_engine = create_engine(MYSQL_CON_STR, pool_size=1, max_overflow=3)
Session = sessionmaker(bind=sql_db_engine)
