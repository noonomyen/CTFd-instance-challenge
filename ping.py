"""
Script for checking that a database server is available.
Essentially a cross-platform, database agnostic mysqladmin.
"""
import time

from os.path import exists

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url

from CTFd.config import Config

url = make_url(Config.DATABASE_URL)

# Ignore sqlite databases
if url.drivername.startswith("sqlite"):
    exit(0)

# Null out the database so raw_connection doesnt error if it doesnt exist
# CTFd will create the database if it doesnt exist
url = url._replace(database=None)

print("Waiting for db and cache unix socket")
while True:
    if exists("/ipc/db/sock") and exists("/ipc/cache/sock"):
        break
    print(".", end="", flush=True)
    time.sleep(1)

print(f" OK")

# Wait for the database server to be available
engine = create_engine(url)
print(f"Waiting for {url.host} to be ready")
while True:
    try:
        engine.raw_connection()
        break
    except Exception as e:
        print(e)
        print("Waiting 1s for database connection")
        time.sleep(1)

print(f"{url.host} is ready")
time.sleep(1)
