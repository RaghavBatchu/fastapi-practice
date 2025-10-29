from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import urllib.parse

# NOTE: Password contains an '@' (Lakshmi@2005) which must be percent-encoded
# when used in a DB URL. Use urllib.parse.quote_plus to encode special chars.
DB_PASSWORD = "Lakshmi@2005"
db_url = f"postgresql://postgres:{urllib.parse.quote_plus(DB_PASSWORD)}@localhost:5432/Raghav"

# enable echo to surface the SQL and connection attempts in logs
engine = create_engine(db_url, echo=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)